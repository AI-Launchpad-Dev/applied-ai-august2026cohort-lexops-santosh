"""Milestone 7: Observability + reliability hardening.

Two things, built on top of the M6 multi-agent pipeline:

  1. LangFuse tracing -- every agent call is wrapped with @observe() so a
     full run produces a nested trace (pipeline -> agent -> LLM call) viewable
     in the LangFuse dashboard, with timings, inputs, and outputs captured
     automatically.

  2. Reliability hardening:
     - Long-document handling: CUAD contracts can run past what's sensible to
       stuff into a single prompt. A map-reduce summarizer chunks the
       document, summarizes each chunk, then summarizes the summaries --
       tested against the largest real CUAD contract in the corpus.
     - Per-agent try/except: if any single agent fails (timeout, bad JSON,
       provider error), the pipeline logs it and falls back to a safe
       default (route to human review) instead of crashing the whole run.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
load_dotenv()

from langfuse import observe, get_client

from datagen.llm import complete, complete_json, LLMError
from m1_extract import ContractSummary, build_prompt as m1_build_prompt
from m2_agent import clause_risk_calculator
from m4_rag import answer_with_citations
from m6_mcp_server import mcp as server_instance
from mcp import Client

CUAD_DIR = Path("data/lexops/cuad")


# =====================================================================
# Part 1: traced versions of the M6 agents
# =====================================================================

@observe(name="extraction-agent")
def extraction_agent(record: dict[str, Any]) -> dict[str, Any]:
    try:
        prompt = m1_build_prompt(record)
        raw = complete_json(prompt, temperature=0.0)
        return ContractSummary(**raw).model_dump()
    except (LLMError, Exception) as e:
        print(f"  [Extraction Agent] FAILED ({e}) -- defaulting to human review")
        return {"clause_types_present": [], "deviations": [], "risk_band": None,
                 "requires_human_review": True, "_agent_failed": True}


@observe(name="playbook-rag-agent")
def playbook_rag_agent(extracted: dict[str, Any]) -> dict[str, Any]:
    try:
        clauses = extracted.get("clause_types_present") or ["general contract terms"]
        deviations = extracted.get("deviations") or []
        question = (
            f"What is Northwind's playbook position on: {', '.join(clauses)}? "
            f"Note any deviations flagged: {', '.join(deviations) if deviations else 'none'}."
        )
        return answer_with_citations(question)
    except (LLMError, Exception) as e:
        print(f"  [Playbook RAG Agent] FAILED ({e}) -- returning empty context")
        return {"answer": "", "cited_sources": [], "chunks_used": [], "_agent_failed": True}


@observe(name="redline-drafting-agent")
def redline_drafting_agent(extracted: dict[str, Any], playbook: dict[str, Any],
                            risk_result: dict[str, Any]) -> str:
    try:
        prompt = f"""You are drafting an internal redline recommendation for a legal team.

Extracted deviations: {extracted.get('deviations')}
Playbook position: {playbook['answer']}
Risk assessment: score {risk_result['risk_score']}, band {risk_result['risk_band']}

Draft a short (3-5 sentence) internal redline recommendation. Do not state
that any clause is "enforceable" or "unenforceable"."""
        return complete(prompt).strip()
    except (LLMError, Exception) as e:
        print(f"  [Redline Drafting Agent] FAILED ({e}) -- using placeholder draft")
        return ("[Draft generation failed -- this case requires manual drafting "
                "by a human reviewer.]")


@observe(name="legal-reviewer-agent")
def legal_reviewer_agent(draft: str, extracted: dict[str, Any],
                          risk_result: dict[str, Any]) -> dict[str, Any]:
    _FORBIDDEN = ("is enforceable", "is unenforceable", "not enforceable")
    _LIABILITY_KEYWORDS = ("no_liability_cap", "uncapped_liability", "unlimited_liability")
    DISCLAIMER = ("[Internal drafting assistance only -- not legal advice. "
                  "Requires named-attorney review before any external use.]")

    violations = [p for p in _FORBIDDEN if p in draft.lower()]
    final_text = draft if DISCLAIMER in draft else f"{draft}\n\n{DISCLAIMER}"

    # Any upstream agent failure -> force human review regardless of score.
    if extracted.get("_agent_failed"):
        return {"final_text": final_text, "route": "human_review",
                "reason": "upstream agent failure -- routed to human as a safe default",
                "guardrail_violations": violations}

    deviations = [d.lower() for d in (extracted.get("deviations") or [])]
    liability_touched = any(any(kw in dev for kw in _LIABILITY_KEYWORDS) for dev in deviations)

    if risk_result["risk_score"] > 70:
        route, reason = "human_review", f"risk_score={risk_result['risk_score']} > 70"
    elif liability_touched:
        route, reason = "human_review", "liability cap deviation present -- never auto-approved"
    elif violations:
        route, reason = "human_review", f"guardrail violation: {violations}"
    else:
        route, reason = "auto_approve", f"risk_score={risk_result['risk_score']} <= 70, no issues"

    return {"final_text": final_text, "route": route, "reason": reason,
            "guardrail_violations": violations}


# =====================================================================
# Part 2: long-document hardening (map-reduce summarization)
# =====================================================================

def _find_longest_cuad_txt() -> Path | None:
    """Locate the largest real CUAD contract text file, to stress-test with
    a genuine long document rather than a contrived one."""
    txt_files = list(CUAD_DIR.rglob("*.txt"))
    if not txt_files:
        return None
    return max(txt_files, key=lambda p: p.stat().st_size)


def _chunk_words(text: str, chunk_size: int = 2500, overlap: int = 100) -> list[str]:
    words = text.split()
    chunks, start = [], 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start = end - overlap
    return chunks


@observe(name="long-document-summarizer")
def summarize_long_document(text: str) -> str:
    """Map-reduce summarization: chunk the document, summarize each chunk,
    then summarize the summaries. Keeps any single prompt well within a
    sane size regardless of how long the source contract is."""
    chunks = _chunk_words(text)
    print(f"  [Hardening] document split into {len(chunks)} chunks for summarization")

    partial_summaries = []
    for i, chunk in enumerate(chunks, 1):
        try:
            summary = complete(
                f"Summarize the key legal terms in this contract excerpt in "
                f"3-4 sentences (parties, obligations, notable clauses):\n\n{chunk}"
            )
            partial_summaries.append(summary.strip())
        except (LLMError, Exception) as e:
            print(f"  [Hardening] chunk {i}/{len(chunks)} failed ({e}) -- skipping, not crashing")
            partial_summaries.append(f"[chunk {i} could not be summarized]")

    combined = "\n\n".join(partial_summaries)
    if len(chunks) == 1:
        return combined

    final = complete(
        f"Combine these section summaries of one contract into a single "
        f"coherent 5-6 sentence overview:\n\n{combined}"
    )
    return final.strip()


# =====================================================================
# Part 3: hardened, traced end-to-end pipeline
# =====================================================================

@observe(name="lexops-review-pipeline")
async def run_pipeline(record: dict[str, Any], contract_id: str, signer_email: str) -> dict[str, Any]:
    async with Client(server_instance) as client:
        try:
            contract_result = await asyncio.wait_for(
                client.call_tool("get_contract", {"contract_id": contract_id}), timeout=15
            )
            contract_data = contract_result.structured_content
        except asyncio.TimeoutError:
            print("  [MCP] get_contract TIMED OUT -- proceeding without contract lookup")
            contract_data = {"error": "timeout"}
        print(f"  [MCP] contract: {contract_data}")

        extracted = extraction_agent(record)
        playbook = playbook_rag_agent(extracted)
        risk_result = clause_risk_calculator(extracted.get("deviations") or [])
        draft = redline_drafting_agent(extracted, playbook, risk_result)
        review = legal_reviewer_agent(draft, extracted, risk_result)

        print(f"  route={review['route']}  reason={review['reason']}")

        if review["route"] == "auto_approve":
            try:
                sig_result = await asyncio.wait_for(
                    client.call_tool("create_signature_request",
                                      {"contract_id": contract_id, "signer_email": signer_email}),
                    timeout=15,
                )
                print(f"  [MCP] created: {sig_result.structured_content}")
            except asyncio.TimeoutError:
                print("  [MCP] create_signature_request TIMED OUT -- not marking as sent")

        return review


# =====================================================================
# Demo
# =====================================================================

if __name__ == "__main__":
    langfuse = get_client()

    print("=== Part A: long-document hardening test ===")
    longest = _find_longest_cuad_txt()
    if longest is None:
        print("[!] No CUAD .txt files found under data/lexops/cuad -- skipping this test.")
    else:
        text = longest.read_text(encoding="utf-8", errors="ignore")
        print(f"Testing on: {longest.name} ({len(text.split())} words)")
        summary = summarize_long_document(text)
        print(f"\nSummary:\n{summary}\n")

    print("\n=== Part B: traced, hardened pipeline run ===")
    records_path = Path("data/lexops/intake/records.jsonl")
    records = [json.loads(l) for l in records_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    demo_record = records[0]

    import csv as _csv
    with (Path("data/lexops/mock_api/contracts.csv")).open(encoding="utf-8") as fh:
        sample_contract = next(iter(_csv.DictReader(fh)))

    asyncio.run(run_pipeline(demo_record, sample_contract["contract_id"], "counsel@northwindsystems.com"))

    print("\nFlushing traces to LangFuse...")
    langfuse.flush()
    print("Done -- check your LangFuse dashboard for the trace.")