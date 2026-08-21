"""Milestone 1: Provider-agnostic LLM client + structured intake.

Reads raw, messy contract review requests from data/lexops/intake/records.jsonl,
asks the LLM to extract key clause fields, validates the result against a
Pydantic schema, and scores it against the ground_truth already attached to
each record.
"""

from __future__ import annotations

import json
from operator import truth
from pathlib import Path
from typing import Optional, List

from pydantic import BaseModel, ValidationError

# Reuse the LLM client I am already working.
from datagen.llm import complete_json


# ---------- Step 1: define what a "good extraction" looks like ----------

class ContractSummary(BaseModel):
    """The structured fields we want pulled out of a raw request."""
    clause_types_present: List[str] = []
    deviations: List[str] = []
    risk_band: Optional[str] = None          # "standard" | "deviation" | "escalation"
    requires_human_review: Optional[bool] = None


# ---------- Step 2: build the prompt ----------

def build_prompt(record: dict) -> str:
    raw_text = record.get("raw_text", "")
    clause_text = record.get("attached_clause_text", "")
    contract_type = record.get("contract_type", "unknown")

    return f"""You are reviewing an internal contract-review request for a legal team.

Contract type: {contract_type}

Request text:
{raw_text}

Attached clause text:
{clause_text}

Extract the following as JSON with EXACTLY these fields:
{{
  "clause_types_present": [list of clause categories mentioned or implied,
      e.g. "liability_cap", "termination", "indemnification", "governing_law"],
  "deviations": [choose ONLY from this exact list -- do not invent new labels:
      "uncapped_indemnity", "unilateral_termination", "unrestricted_assignment",
      "no_liability_cap", "unlimited_liability", "short_notice_period",
      "ip_assignment_of_customer_data", "no_audit_rights", "none"],
  "risk_band": one of "standard", "deviation", "escalation",
  "requires_human_review": true or false
}}

Respond with raw JSON only."""

# ---------- Step 3: run one record through the model ----------

def extract_one(record: dict) -> Optional[ContractSummary]:
    prompt = build_prompt(record)
    try:
        raw = complete_json(prompt, temperature=0.0)
        return ContractSummary(**raw)
    except (ValidationError, TypeError, ValueError) as e:
        print(f"  [!] Could not parse record {record.get('request_id')}: {e}")
        return None


# ---------- Step 4: compare against ground_truth ----------

import re


def _normalize(label: str) -> set[str]:
    """Turn a clause label into a set of meaningful lowercase words."""
    label = label.lower().replace("_", " ")
    words = re.findall(r"[a-z]+", label)
    stopwords = {"of", "and", "the", "to", "for", "a", "an"}
    return {w for w in words if w not in stopwords}


def _clause_matches(pred_label: str, truth_label: str) -> bool:
    """True if the two labels share at least one meaningful word."""
    return bool(_normalize(pred_label) & _normalize(truth_label))


def score_against_ground_truth(pred: ContractSummary, truth: dict) -> dict:
    """Field-by-field comparison, using fuzzy word-overlap for clause names."""
    result = {}

    truth_risk = truth.get("risk_band")
    result["risk_band_match"] = (pred.risk_band == truth_risk)

    truth_review = truth.get("requires_human_review")
    result["human_review_match"] = (pred.requires_human_review == truth_review)

    truth_clauses = list(truth.get("clause_types_present", []) or [])
    pred_clauses = list(pred.clause_types_present or [])

    matched_truth = set()
    for t in truth_clauses:
        for p in pred_clauses:
            if _clause_matches(p, t):
                matched_truth.add(t)
                break

    result["clause_overlap"] = len(matched_truth)
    result["clause_total"] = len(truth_clauses)

    return result

# ---------- Step 5: main loop ----------

def main(n_records: int = 30) -> None:
    records_path = Path("data/lexops/intake/records.jsonl")
    if not records_path.exists():
        print(f"Can't find {records_path} -- run the intake generation step first.")
        return

    records = []
    with records_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    records = records[:n_records]
    print(f"Testing extraction on {len(records)} records...\n")

    total = 0
    risk_correct = 0
    review_correct = 0
    clause_hits = 0
    clause_possible = 0

    for i, record in enumerate(records, 1):
        print(f"[{i}/{len(records)}] {record.get('request_id')}")
        pred = extract_one(record)
        if pred is None:
            continue

        truth = record.get("ground_truth", {})
        if not truth:
            print("  [!] No ground_truth on this record, skipping scoring.")
            continue

        print(f"  predicted clauses: {pred.clause_types_present}")
        print(f"  truth clauses    : {truth.get('clause_types_present')}")
        scores = score_against_ground_truth(pred, truth)
        total += 1
        risk_correct += int(scores["risk_band_match"])
        review_correct += int(scores["human_review_match"])
        clause_hits += scores["clause_overlap"]
        clause_possible += scores["clause_total"]

        print(f"  predicted risk_band={pred.risk_band!r} vs truth={truth.get('risk_band')!r}"
              f" -> {'OK' if scores['risk_band_match'] else 'MISS'}")

    print("\n" + "=" * 50)
    print("RESULTS")
    print("=" * 50)
    if total == 0:
        print("No records were successfully scored.")
        return
    print(f"Records scored          : {total}")
    print(f"Risk band accuracy      : {risk_correct}/{total} ({100*risk_correct/total:.0f}%)")
    print(f"Human review accuracy   : {review_correct}/{total} ({100*review_correct/total:.0f}%)")
    if clause_possible:
        print(f"Clause type recall      : {clause_hits}/{clause_possible} "
              f"({100*clause_hits/clause_possible:.0f}%)")


if __name__ == "__main__":
    main(n_records=30)