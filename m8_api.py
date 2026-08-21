"""Milestone 8, part 2: FastAPI deployment package.

Wraps the M6/M7 multi-agent pipeline (extraction -> playbook RAG -> risk
score -> redline draft -> legal review) as a REST API.

Run with:
    pip install fastapi uvicorn
    uvicorn m8_api:app --reload

Then open http://127.0.0.1:8000/docs for interactive API docs, or POST to
http://127.0.0.1:8000/review directly.
"""

from __future__ import annotations

from typing import Any, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from m1_extract import ContractSummary, build_prompt as m1_build_prompt
from m2_agent import clause_risk_calculator
from m4_rag import answer_with_citations
from datagen.llm import complete, complete_json

app = FastAPI(
    title="LexOps Contract Review API",
    description=(
        "Contract intelligence & compliance copilot. Drafting assistance "
        "only -- not legal advice. All output requires named-attorney "
        "review before any external use."
    ),
    version="1.0.0",
)

DISCLAIMER = ("[Internal drafting assistance only -- not legal advice. "
              "Requires named-attorney review before any external use.]")
_FORBIDDEN = ("is enforceable", "is unenforceable", "not enforceable")
_LIABILITY_KEYWORDS = ("no_liability_cap", "uncapped_liability", "unlimited_liability")


class ReviewRequest(BaseModel):
    request_id: str
    raw_text: str
    attached_clause_text: Optional[str] = ""
    contract_type: Optional[str] = "unknown"


class ReviewResponse(BaseModel):
    request_id: str
    extracted: dict[str, Any]
    playbook_position: str
    playbook_sources: list[str]
    risk_score: int
    risk_band: str
    route: str
    route_reason: str
    redline_draft: str
    disclaimer: str = DISCLAIMER


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/review", response_model=ReviewResponse)
def review_contract(req: ReviewRequest) -> ReviewResponse:
    record = {
        "request_id": req.request_id,
        "raw_text": req.raw_text,
        "attached_clause_text": req.attached_clause_text,
        "contract_type": req.contract_type,
    }

    # 1. Extraction
    try:
        raw = complete_json(m1_build_prompt(record), temperature=0.0)
        extracted = ContractSummary(**raw).model_dump()
    except Exception:
        extracted = {"clause_types_present": [], "deviations": [],
                      "risk_band": None, "requires_human_review": True}

    # 2. Playbook RAG
    clauses = extracted.get("clause_types_present") or ["general contract terms"]
    deviations = extracted.get("deviations") or []
    question = (
        f"What is Northwind's playbook position on: {', '.join(clauses)}? "
        f"Note any deviations flagged: {', '.join(deviations) if deviations else 'none'}."
    )
    rag = answer_with_citations(question)

    # 3. Risk score
    risk = clause_risk_calculator(deviations)

    # 4. Redline draft
    draft_prompt = f"""Draft a short (3-5 sentence) internal redline recommendation.

Extracted deviations: {deviations}
Playbook position: {rag['answer']}
Risk assessment: score {risk['risk_score']}, band {risk['risk_band']}

Do not state that any clause is "enforceable" or "unenforceable"."""
    draft = complete(draft_prompt).strip()

    # 5. Legal Reviewer guardrails -- enforced in code, not just prompted
    violations = [p for p in _FORBIDDEN if p in draft.lower()]
    final_draft = draft if DISCLAIMER in draft else f"{draft}\n\n{DISCLAIMER}"

    liability_touched = any(
        any(kw in d.lower() for kw in _LIABILITY_KEYWORDS) for d in deviations
    )
    if risk["risk_score"] > 70:
        route, reason = "human_review", f"risk_score={risk['risk_score']} > 70"
    elif liability_touched:
        route, reason = "human_review", "liability cap deviation present -- never auto-approved"
    elif violations:
        route, reason = "human_review", f"guardrail violation: {violations}"
    else:
        route, reason = "auto_approve", f"risk_score={risk['risk_score']} <= 70, no issues"

    return ReviewResponse(
        request_id=req.request_id,
        extracted=extracted,
        playbook_position=rag["answer"],
        playbook_sources=rag["cited_sources"],
        risk_score=risk["risk_score"],
        risk_band=risk["risk_band"],
        route=route,
        route_reason=reason,
        redline_draft=final_draft,
    )
