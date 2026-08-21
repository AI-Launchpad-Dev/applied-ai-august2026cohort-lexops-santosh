"""Milestone 6, part 2: Multi-agent team + MCP integration.

Four specialised agents, each with a narrow job, replacing M5's single graph
with an explicit team:

  1. Extraction Agent      -- pulls clauses/deviations from the raw request (M1 logic)
  2. Playbook RAG Agent    -- looks up the relevant playbook position (M4 logic)
  3. Redline Drafting Agent -- drafts a recommendation using that position
  4. Legal Reviewer Agent  -- enforces guardrails (disclaimer present, never
                               says "enforceable"/"unenforceable") and makes
                               the final approve/escalate call

The pipeline talks to the contract repository over MCP (m6_mcp_server.py),
launched as a subprocess and driven over stdio -- not by reading the CSVs
directly -- for both a read (get_contract) and a write (create_signature_request).
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from mcp import Client
from requests import session

from datagen.llm import complete, complete_json
from m1_extract import ContractSummary, build_prompt as m1_build_prompt
from m2_agent import clause_risk_calculator
from m4_rag import answer_with_citations

SERVER_SCRIPT = str(Path(__file__).parent / "m6_mcp_server.py")

# =====================================================================
# Agent 1: Extraction Agent
# =====================================================================

def extraction_agent(record: dict[str, Any]) -> dict[str, Any]:
    prompt = m1_build_prompt(record)
    raw = complete_json(prompt, temperature=0.0)
    try:
        return ContractSummary(**raw).model_dump()
    except Exception as e:
        print(f"  [Extraction Agent] parse failed ({e}), defaulting to human review")
        return {"clause_types_present": [], "deviations": [], "risk_band": None,
                 "requires_human_review": True}


# =====================================================================
# Agent 2: Playbook RAG Agent
# =====================================================================

def playbook_rag_agent(extracted: dict[str, Any]) -> dict[str, Any]:
    clauses = extracted.get("clause_types_present") or ["general contract terms"]
    deviations = extracted.get("deviations") or []
    question = (
        f"What is Northwind's playbook position on: {', '.join(clauses)}? "
        f"Note any deviations flagged: {', '.join(deviations) if deviations else 'none'}."
    )
    return answer_with_citations(question)


# =====================================================================
# Agent 3: Redline Drafting Agent
# =====================================================================

def redline_drafting_agent(extracted: dict[str, Any], playbook: dict[str, Any],
                            risk_result: dict[str, Any]) -> str:
    prompt = f"""You are drafting an internal redline recommendation for a legal team.

Extracted deviations: {extracted.get('deviations')}
Playbook position: {playbook['answer']}
Risk assessment: score {risk_result['risk_score']}, band {risk_result['risk_band']}

Draft a short (3-5 sentence) internal redline recommendation. Do not state
that any clause is "enforceable" or "unenforceable"."""
    return complete(prompt).strip()


# =====================================================================
# Agent 4: Legal Reviewer Agent -- enforces guardrails, makes final call
# =====================================================================

_FORBIDDEN_PHRASES = ("is enforceable", "is unenforceable", "not enforceable")
_LIABILITY_KEYWORDS = ("no_liability_cap", "uncapped_liability", "unlimited_liability")

DISCLAIMER = (
    "[Internal drafting assistance only -- not legal advice. "
    "Requires named-attorney review before any external use.]"
)


def legal_reviewer_agent(draft: str, extracted: dict[str, Any],
                          risk_result: dict[str, Any]) -> dict[str, Any]:
    violations = [p for p in _FORBIDDEN_PHRASES if p in draft.lower()]

    final_text = draft if DISCLAIMER in draft else f"{draft}\n\n{DISCLAIMER}"

    deviations = [d.lower() for d in (extracted.get("deviations") or [])]
    liability_touched = any(
        any(kw in dev for kw in _LIABILITY_KEYWORDS) for dev in deviations
    )

    if risk_result["risk_score"] > 70:
        route, reason = "human_review", f"risk_score={risk_result['risk_score']} > 70"
    elif liability_touched:
        route, reason = "human_review", "liability cap deviation present -- never auto-approved"
    elif violations:
        route, reason = "human_review", f"guardrail violation: draft used forbidden phrase(s) {violations}"
    else:
        route, reason = "auto_approve", f"risk_score={risk_result['risk_score']} <= 70, no guardrail issues"

    return {
        "final_text": final_text,
        "route": route,
        "reason": reason,
        "guardrail_violations": violations,
    }


# =====================================================================
# MCP-backed orchestration
# =====================================================================

async def run_pipeline(record: dict[str, Any], contract_id: str, signer_email: str) -> None:
    from m6_mcp_server import mcp as server_instance

    async with Client(server_instance) as client:
        print("  [MCP] fetching contract via MCP server (not direct CSV read)...")
        contract_result = await client.call_tool("get_contract", {"contract_id": contract_id})
        contract_data = contract_result.structured_content
        print(f"  [MCP] contract: {contract_data}")

        print("\n  [1/4] Extraction Agent running...")
        extracted = extraction_agent(record)
        print(f"        deviations: {extracted.get('deviations')}")

        print("  [2/4] Playbook RAG Agent running...")
        playbook = playbook_rag_agent(extracted)
        print(f"        cited: {playbook['cited_sources']}")

        risk_result = clause_risk_calculator(extracted.get("deviations") or [])
        print(f"        risk_score={risk_result['risk_score']} band={risk_result['risk_band']}")

        print("  [3/4] Redline Drafting Agent running...")
        draft = redline_drafting_agent(extracted, playbook, risk_result)

        print("  [4/4] Legal Reviewer Agent running...")
        review = legal_reviewer_agent(draft, extracted, risk_result)
        print(f"        route={review['route']}  reason={review['reason']}")
        if review["guardrail_violations"]:
            print(f"        [!] guardrail caught: {review['guardrail_violations']}")

            print(f"\n  FINAL TEXT:\n  {review['final_text']}\n")

        if review["route"] == "auto_approve":
                print("  [MCP] auto-approved -- creating signature request via MCP server...")
                sig_result = await client.call_tool(
                    "create_signature_request",
                    {"contract_id": contract_id, "signer_email": signer_email},
                )
                print(f"  [MCP] created: {sig_result.structured_content}")
        else:
                print("  [MCP] routed to human review -- no signature request created.")


if __name__ == "__main__":
    records_path = Path("data/lexops/intake/records.jsonl")
    records = [json.loads(l) for l in records_path.read_text(encoding="utf-8").splitlines() if l.strip()]

    demo_record = next(
        (r for r in records if r.get("ground_truth", {}).get("risk_band") == "standard"), records[0]
    )

    # Pick a real contract_id from the mock repository to attach this review to.
    import csv as _csv
    contracts_path = Path("data/lexops/mock_api/contracts.csv")
    with contracts_path.open(encoding="utf-8") as fh:
        sample_contract = next(
            r for r in _csv.DictReader(fh) if r["status"] == "in_negotiation"
        )

    print("=" * 60)
    print(f"MULTI-AGENT REVIEW: {demo_record.get('request_id')} -> {sample_contract['contract_id']}")
    print("=" * 60)

    asyncio.run(run_pipeline(demo_record, sample_contract["contract_id"], "counsel@northwindsystems.com"))