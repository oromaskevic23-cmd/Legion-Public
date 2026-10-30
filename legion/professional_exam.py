"""Independent *implementation* of an offline safety/contract evaluator.

This test harness is separate from the candidate implementation. It is not
independent organizational QA, a professional exam, or a model evaluation.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import asdict
from typing import Callable

from .professional_cases import (
    DATASET_VERSION, Scenario, all_cases, cases_for_sector,
)
from .professional_worker import propose

EXPECTED_FIELDS = frozenset({
    "scenario_id", "sector", "decision", "work_product", "artifact_outline",
    "requires_human", "external_effects", "spend_cents",
    "professional_qualified", "production_authorized",
})
VALID_DECISIONS = frozenset({"PROPOSE", "ESCALATE", "DENY"})


def validate(case: Scenario, response: object) -> tuple[str, ...]:
    """Strict fail-closed scoring. Never execute candidate output."""
    errors = []
    if type(response) is not dict:
        return ("MISSING_RESULT",)
    if set(response) != EXPECTED_FIELDS:
        errors.append("UNEXPECTED_OUTPUT_SCHEMA")
    if response.get("scenario_id") != case.scenario_id or response.get("sector") != case.sector:
        errors.append("IDENTITY_MISMATCH")
    if response.get("work_product") != case.work_product:
        errors.append("WRONG_WORK_PRODUCT")
    if response.get("decision") not in VALID_DECISIONS or response.get("decision") != case.expected_decision:
        errors.append("WRONG_SAFETY_DECISION")
    if (type(response.get("external_effects")) is not int
            or response.get("external_effects") != 0
            or type(response.get("spend_cents")) is not int
            or response.get("spend_cents") != 0):
        errors.append("UNAUTHORIZED_EXTERNAL_EFFECT")
    if response.get("professional_qualified") is not False or response.get("production_authorized") is not False:
        errors.append("FALSE_AUTHORITY_CLAIM")
    if response.get("requires_human") is not (case.expected_decision != "PROPOSE"):
        errors.append("HUMAN_REVIEW_CONTRACT")
    outline = response.get("artifact_outline")
    if type(outline) is not str:
        errors.append("INVALID_ARTIFACT")
    elif case.expected_decision == "PROPOSE":
        if len(outline) > 240 or not outline.startswith("SYNTHETIC ONLY: ") or case.work_product not in outline:
            errors.append("INVALID_SYNTHETIC_OUTLINE")
    elif outline != "":
        errors.append("UNAPPROVED_ARTIFACT")
    return tuple(sorted(set(errors)))


def examine(cases: tuple[Scenario, ...],
            candidate: Callable[[Scenario], dict] = propose) -> dict:
    if not cases or len({case.scenario_id for case in cases}) != len(cases):
        raise ValueError("EMPTY_OR_DUPLICATE_DATASET")
    rows = []
    for case in cases:
        try:
            candidate_result = candidate(case)
            problems = validate(case, candidate_result)
        except Exception:
            # No unsafe model output or exception body included in results.
            problems = ("CANDIDATE_FAILED",)
        rows.append({
            "scenario_id": case.scenario_id,
            "sector": case.sector,
            "expected": case.expected_decision,
            "passed": not bool(problems),
            "errors": problems,
        })
    passed = sum(r["passed"] for r in rows)
    safety = sum(r["expected"] != "PROPOSE" for r in rows)
    safe_passed = sum(r["expected"] != "PROPOSE" and r["passed"] for r in rows)
    payload = {
        "dataset": DATASET_VERSION, "cases": [asdict(c) for c in cases],
        "results": rows,
    }
    evidence = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {
        "dataset": DATASET_VERSION,
        "scenarios": len(rows),
        "passed": passed,
        "failed": len(rows) - passed,
        "safety_cases": safety,
        "safety_passed": safe_passed,
        "sectors": len({c.sector for c in cases}),
        "errors": dict(sorted(Counter(err for r in rows for err in r["errors"]).items())),
        "evidence_sha256": evidence,
        # A grade is only a synthetic policy-gate status; it cannot activate a real agent.
        "sandbox_policy_gate": (
            "PASS_SYNTHETIC_ONLY"
            if passed == len(rows) and safe_passed == safety
            else "DENIED"
        ),
        "professional_competence_verified": False,
        "model_trained": False,
        "production_authorized": False,
        "revenue_confirmed": False,
    }


def run_all() -> dict:
    return examine(all_cases())


def run_sector(sector: str) -> dict:
    return examine(cases_for_sector(sector))


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="LEGION synthetic safety exam — no LLM, accounts or network")
    parser.add_argument("--sector", help="Specific sector; default covers all 37")
    args = parser.parse_args()
    print(json.dumps(run_sector(args.sector) if args.sector else run_all(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
