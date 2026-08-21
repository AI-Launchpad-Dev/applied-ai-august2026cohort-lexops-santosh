"""Milestone 5: Orchestrated LangGraph workflow with checkpointing.

Wires M1 (extraction), M2 (risk calculator), and M4 (playbook RAG) into an
explicit state machine:

    extract -> compare_to_playbook -> draft_redline -> [conditional]
                                                          |-> auto_approve
                                                          |-> human_review

Routing rule (from the generated playbook): a clause may never be
auto-approved if its risk score exceeds 70, OR if the liability cap itself
has been redlined/rejected by the counterparty -- regardless of score.

A checkpointer persists state after every node, so a run that dies partway
through can resume from the last completed step instead of starting over.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional, TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from datagen.llm import complete_json
from m1_extract import ContractSummary, build_prompt as m1_build_prompt
from m2_agent import clause_risk_calculator
from m4_rag import answer_with_citations


# =====================================================================
# State definition
# =====================================================================

class ReviewState(TypedDict):
    request: dict[str, Any]                 # the raw intake record
    extracted: Optional[dict[str, Any]]      # ContractSummary as dict
    playbook_answer: Optional[str]           # RAG answer on the relevant position
    playbook_sources: list[str]              # which docs the RAG cited
    risk_result: Optional[dict[str, Any]]    # output of clause_risk_calculator
    redline_draft: Optional[str]
    route: Optional[str]                     # "auto_approve" | "human_review"
    route_reason: Optional[str]
    log: list[str]                           # human-readable trace of what happened


# =====================================================================
# Node 1: extract
# =====================================================================

def extract_node(state: ReviewState) -> dict[str, Any]:
    record = state["request"]
    prompt = m1_build_prompt(record)
    raw = complete_json(prompt, temperature=0.0)
    try:
        summary = ContractSummary(**raw)
        extracted = summary.model_dump()
    except Exception as e:
        extracted = {
            "clause_types_present": [], "deviations": [],
            "risk_band": None, "requires_human_review": True,
        }
        state["log"].append(f"extract: FAILED to parse ({e}), defaulting to human review")

    return {
        "extracted": extracted,
        "log": state["log"] + [f"extract: found deviations={extracted.get('deviations')}"],
    }


# =====================================================================
# Node 2: compare to playbook (RAG lookup + risk score)
# =====================================================================

def compare_node(state: ReviewState) -> dict[str, Any]:
    extracted = state["extracted"]
    clauses = extracted.get("clause_types_present") or ["general contract terms"]
    deviations = extracted.get("deviations") or []

    question = (
        f"What is Northwind's playbook position on: {', '.join(clauses)}? "
        f"Note any deviations flagged: {', '.join(deviations) if deviations else 'none'}."
    )
    rag_result = answer_with_citations(question)

    risk_result = clause_risk_calculator(deviations)

    return {
        "playbook_answer": rag_result["answer"],
        "playbook_sources": rag_result["cited_sources"],
        "risk_result": risk_result,
        "log": state["log"] + [
            f"compare: risk_score={risk_result['risk_score']} "
            f"band={risk_result['risk_band']} sources={rag_result['cited_sources']}"
        ],
    }


# =====================================================================
# Node 3: draft redline
# =====================================================================

def draft_node(state: ReviewState) -> dict[str, Any]:
    prompt = f"""You are drafting an internal redline recommendation for a legal team.

Extracted deviations: {state['extracted'].get('deviations')}
Playbook position: {state['playbook_answer']}
Risk assessment: score {state['risk_result']['risk_score']}, band {state['risk_result']['risk_band']}

Draft a short (3-5 sentence) internal redline recommendation. This is
drafting assistance, not legal advice, and must not be sent to a
counterparty without attorney review. Do not state that any clause is
"enforceable" or "unenforceable"."""

    from datagen.llm import complete as _complete
    draft = _complete(prompt)

    disclaimer = (
        "\n\n[Internal drafting assistance only -- not legal advice. "
        "Requires named-attorney review before any external use.]"
    )
    return {
        "redline_draft": draft.strip() + disclaimer,
        "log": state["log"] + ["draft: redline generated"],
    }


# =====================================================================
# Conditional routing
# =====================================================================

_LIABILITY_DEVIATION_KEYWORDS = ("no_liability_cap", "uncapped", "liability_cap")


def route_decision(state: ReviewState) -> str:
    """Return the name of the next node: 'auto_approve' or 'human_review'."""
    risk = state["risk_result"]
    deviations = [d.lower() for d in (state["extracted"].get("deviations") or [])]

    liability_touched = any(
        any(kw in dev for kw in _LIABILITY_DEVIATION_KEYWORDS) for dev in deviations
    )

    if risk["risk_score"] > 70:
        return "human_review"
    if liability_touched:
        return "human_review"
    return "auto_approve"


def auto_approve_node(state: ReviewState) -> dict[str, Any]:
    return {
        "route": "auto_approve",
        "route_reason": f"risk_score={state['risk_result']['risk_score']} <= 70, "
                         f"liability cap not touched",
        "log": state["log"] + ["route: AUTO-APPROVED"],
    }


def human_review_node(state: ReviewState) -> dict[str, Any]:
    risk = state["risk_result"]
    reason = (
        f"risk_score={risk['risk_score']} > 70" if risk["risk_score"] > 70
        else "liability cap deviation present -- playbook prohibits auto-approval "
             "of any liability cap redline regardless of score"
    )
    return {
        "route": "human_review",
        "route_reason": reason,
        "log": state["log"] + [f"route: ROUTED TO HUMAN REVIEW ({reason})"],
    }


# =====================================================================
# Build the graph
# =====================================================================

def build_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("extract", extract_node)
    graph.add_node("compare_to_playbook", compare_node)
    graph.add_node("draft_redline", draft_node)
    graph.add_node("auto_approve", auto_approve_node)
    graph.add_node("human_review", human_review_node)

    graph.add_edge(START, "extract")
    graph.add_edge("extract", "compare_to_playbook")
    graph.add_edge("compare_to_playbook", "draft_redline")
    graph.add_conditional_edges(
        "draft_redline",
        route_decision,
        {"auto_approve": "auto_approve", "human_review": "human_review"},
    )
    graph.add_edge("auto_approve", END)
    graph.add_edge("human_review", END)

    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)


# =====================================================================
# Demo: run on two records with contrasting outcomes
# =====================================================================

def run_one(app, record: dict[str, Any], thread_id: str) -> ReviewState:
    initial_state: ReviewState = {
        "request": record,
        "extracted": None,
        "playbook_answer": None,
        "playbook_sources": [],
        "risk_result": None,
        "redline_draft": None,
        "route": None,
        "route_reason": None,
        "log": [],
    }
    config = {"configurable": {"thread_id": thread_id}}
    final_state = app.invoke(initial_state, config=config)
    return final_state


if __name__ == "__main__":
    records_path = Path("data/lexops/intake/records.jsonl")
    records = [json.loads(l) for l in records_path.read_text(encoding="utf-8").splitlines() if l.strip()]

    # Pick one record whose ground_truth suggests standard, and one escalation,
    # so the demo actually exercises both branches of the conditional edge.
    standard_record = next(
        (r for r in records if r.get("ground_truth", {}).get("risk_band") == "standard"), records[0]
    )
    escalation_record = next(
        (r for r in records if r.get("ground_truth", {}).get("risk_band") == "escalation"), records[1]
    )

    app = build_graph()

    for label, record in [("STANDARD CASE", standard_record), ("ESCALATION CASE", escalation_record)]:
        print("=" * 60)
        print(f"{label}: {record.get('request_id')}")
        print("=" * 60)
        result = run_one(app, record, thread_id=record.get("request_id", "demo"))

        for line in result["log"]:
            print(f"  {line}")
        print(f"\n  FINAL ROUTE: {result['route']}")
        print(f"  REASON     : {result['route_reason']}")
        print(f"  REDLINE DRAFT:\n  {result['redline_draft']}\n")