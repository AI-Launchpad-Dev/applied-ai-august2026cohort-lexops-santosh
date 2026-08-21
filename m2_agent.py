"""Milestone 2: Tool-enabled single agent.

The agent can call three tools -- a clause-risk calculator, a renewal-date
calendar, and a file-writing tool -- to answer legal-team requests. Since our
llm.py client is single-shot (no native multi-turn tool calling), we build a
simple ReAct-style loop: ask the model to choose a tool or give a final
answer, run the tool, feed the result back, repeat.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from datagen.llm import complete_json

# Same frozen "now" the generator used, so renewal dates line up with your data.
REFERENCE_NOW = datetime(2026, 8, 19, 9, 0)

MOCK_API_DIR = Path("data/lexops/mock_api")
MEMOS_DIR = Path("data/lexops/memos")


# ---------- Tool 1: clause-risk calculator ----------

# Point deductions taken from the risk-scoring methodology your generator
# produced (data/lexops/corpus/markdown/risk-scoring.md). Hardcoded here so
# the tool is deterministic -- an LLM re-deriving math from prose each call
# would be slower and less reliable than reading it once and coding the rule.
_DEVIATION_PENALTIES = {
    "uncapped_indemnity": 35,
    "unilateral_termination": 25,
    "unrestricted_assignment": 15,
    "no_liability_cap": 30,
    "unlimited_liability": 30,
    "short_notice_period": 15,
    "ip_assignment_of_customer_data": 30,
    "no_audit_rights": 10,
}

_BASE_SCORE = 20  # a clean, standard clause still carries some baseline risk


def clause_risk_calculator(deviations: list[str]) -> dict[str, Any]:
    """Score a clause 0-100 based on which known deviations are present."""
    score = _BASE_SCORE
    matched = []
    for dev in deviations:
        key = dev.strip().lower().replace(" ", "_").replace("-", "_")
        for known, penalty in _DEVIATION_PENALTIES.items():
            if known in key or key in known:
                score += penalty
                matched.append(known)
                break

    score = min(score, 100)
    if score > 70:
        band = "escalation"
    elif score > 40:
        band = "deviation"
    else:
        band = "standard"

    return {
        "risk_score": score,
        "risk_band": band,
        "matched_deviations": matched,
        "requires_gc_signoff": score > 70,
    }


# ---------- Tool 2: renewal-date calendar ----------

def renewal_calendar(days_ahead: int = 60) -> dict[str, Any]:
    """Find contracts renewing within `days_ahead` days of REFERENCE_NOW."""
    contracts_path = MOCK_API_DIR / "contracts.csv"
    if not contracts_path.exists():
        return {"error": f"{contracts_path} not found -- generate mock_api tables first."}

    upcoming = []
    with contracts_path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row.get("status") != "executed":
                continue
            try:
                effective = datetime.fromisoformat(row["effective_date"])
                term_months = int(row["term_months"])
            except (KeyError, ValueError):
                continue

            renewal_date = effective + timedelta(days=30 * term_months)
            days_out = (renewal_date - REFERENCE_NOW).days
            if 0 <= days_out <= days_ahead:
                upcoming.append({
                    "contract_id": row["contract_id"],
                    "counterparty_id": row["counterparty_id"],
                    "renewal_date": renewal_date.date().isoformat(),
                    "days_out": days_out,
                    "auto_renew": row.get("auto_renew"),
                })

    upcoming.sort(key=lambda r: r["days_out"])
    return {"count": len(upcoming), "contracts": upcoming[:20]}


# ---------- Tool 3: file-writing tool ----------

def write_memo(contract_id: str, summary_text: str) -> dict[str, Any]:
    """Write a summary memo to disk for a given contract."""
    MEMOS_DIR.mkdir(parents=True, exist_ok=True)
    path = MEMOS_DIR / f"{contract_id}_memo.md"
    path.write_text(f"# Memo: {contract_id}\n\n{summary_text}\n", encoding="utf-8")
    return {"written_to": str(path)}


# ---------- Tool registry ----------

TOOLS = {
    "clause_risk_calculator": {
        "fn": clause_risk_calculator,
        "description": (
            "Score a clause's risk 0-100 given a list of deviations, e.g. "
            '["uncapped_indemnity"]. Args: {"deviations": [list of strings]}'
        ),
    },
    "renewal_calendar": {
        "fn": renewal_calendar,
        "description": (
            "List executed contracts renewing within N days. "
            'Args: {"days_ahead": integer, default 60}'
        ),
    },
    "write_memo": {
        "fn": write_memo,
        "description": (
            "Save a summary memo to disk. "
            'Args: {"contract_id": string, "summary_text": string}'
        ),
    },
}


# ---------- The agent loop ----------

def _tool_menu() -> str:
    lines = [f"- {name}: {spec['description']}" for name, spec in TOOLS.items()]
    return "\n".join(lines)


def run_agent(question: str, max_steps: int = 5) -> str:
    scratchpad = ""

    for step in range(1, max_steps + 1):
        prompt = f"""You are a legal-ops assistant with access to these tools:

{_tool_menu()}

User request: {question}

{scratchpad}
Respond with JSON only, one of these two shapes:
{{"action": "tool_name", "action_input": {{...}}}}
{{"action": "final_answer", "answer": "..."}}

Use a tool if you need data you don't already have. Give a final_answer once
you have enough information to fully answer the user."""

        decision = complete_json(prompt)
        action = decision.get("action")

        print(f"  [step {step}] action = {action}")

        if action == "final_answer":
            return decision.get("answer", "(no answer given)")

        if action in TOOLS:
            tool_input = decision.get("action_input", {}) or {}
            try:
                result = TOOLS[action]["fn"](**tool_input)
            except Exception as e:
                result = {"error": str(e)}
            print(f"  [step {step}] tool result = {json.dumps(result)[:300]}")
            scratchpad += (
                f"\nYou called {action} with {tool_input} and got: "
                f"{json.dumps(result)}\n"
            )
            continue

        # Model returned something we don't recognise -- stop rather than loop.
        return f"(agent gave an unrecognised action: {decision})"

    return "(agent did not reach a final answer within the step limit)"


if __name__ == "__main__":
    questions = [
        "What's the risk score if a clause has uncapped indemnity and unilateral termination?",
        "Which contracts are renewing in the next 45 days?",
        "Write a memo for contract NW-K-00020 summarizing that it's a standard MSA renewing soon with no auto-renew, no red flags.",
    ]
    for q in questions:
        print(f"\nQUESTION: {q}")
        answer = run_agent(q)
        print(f"ANSWER: {answer}")