"""An independently implemented numeric scorer for synthetic LEGION work.

The evaluator neither prompts the model nor grants a certificate. It
computes its own arithmetic references from the task manifests. No LLM
response can issue a signed AI Passport, approve work or call customer tools.
"""
from __future__ import annotations

from collections import Counter
from decimal import Decimal, InvalidOperation
import hashlib
import json
from typing import Callable

from .data_analyst_cases import (
    AnalyticCase, VERSION, build_cases, dataset_sha256, prompt_for,
)

MAX_RESPONSE = 3200
ALLOWED_FIELDS = frozenset({"answer", "unit"})


def score_case(case: AnalyticCase, raw: str) -> dict:
    errors = []
    result = None
    if type(raw) is not str or not 0 < len(raw) <= MAX_RESPONSE:
        errors.append("MISSING_OR_OVERSIZED_OUTPUT")
    else:
        try:
            result = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            errors.append("INVALID_JSON")
    if result is not None:
        if type(result) is not dict or set(result) != ALLOWED_FIELDS:
            errors.append("INVALID_RESULT_SCHEMA")
        else:
            unit = result["unit"]
            number = result["answer"]
            if type(unit) is not str or unit != case.unit:
                errors.append("WRONG_UNIT")
            if type(number) not in (int, float):
                errors.append("INVALID_NUMBER")
            else:
                try:
                    actual = Decimal(str(number))
                    if not actual.is_finite() or abs(actual - case.expected) > Decimal("0.005"):
                        errors.append("ARITHMETIC_ERROR")
                except (ValueError, InvalidOperation):
                    errors.append("INVALID_NUMBER")
    errors = sorted(set(errors))
    return {
        "case_id": case.id,
        "category": case.category,
        "passed": not errors,
        "errors": errors,
        "output_sha256": hashlib.sha256(
            raw.encode() if type(raw) is str else b"INVALID_CANDIDATE_OUTPUT"
        ).hexdigest(),
    }


def evaluate(candidate: Callable[[str], str]) -> dict:
    cases = build_cases()
    rows = []
    attempted = 0
    completed = 0
    for case in cases:
        attempted += 1
        try:
            result = candidate(prompt_for(case))
            completed += 1
            rows.append(score_case(case, result))
        except Exception:
            # Never emit a model exception string; it may contain private data.
            rows.append({
                "case_id": case.id,
                "category": case.category,
                "passed": False,
                "errors": ["CANDIDATE_UNAVAILABLE"],
                "output_sha256": "0" * 64,
            })
    good = sum(row["passed"] for row in rows)
    group = {}
    for category in ("conversion", "total", "mean"):
        relevant = [row for row in rows if row["category"] == category]
        group[category] = {
            "passed": sum(r["passed"] for r in relevant),
            "total": len(relevant),
        }
    report_sha = hashlib.sha256(
        json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "benchmark_version": VERSION,
        "dataset_sha256": dataset_sha256(cases),
        "evidence_sha256": report_sha,
        "exam_cases": len(rows),
        "attempted_model_calls": attempted,
        "completed_model_calls": completed,
        "passed": good,
        "failed": len(rows) - good,
        "exact_arithmetic_pass_rate": round(good / len(rows), 4),
        "categories": group,
        "failure_reasons": dict(sorted(
            Counter(err for row in rows for err in row["errors"]).items()
        )),
        "results": rows,
        "exam_result": "RUBRIC_ONLY_PASS" if good == len(rows) else "NEEDS_IMPROVEMENT",
        "rubric_scope": "small public synthetic arithmetic benchmark",
        "independent_implementation_qa": True,
        "independently_operated_qa": False,
        "training_weights_modified": False,
        "professionally_qualified": False,
        "production_authorized": False,
        "external_effects": 0,
        "commercial_platform_access": False,
        "payment_confirmed": False,
    }


def main() -> None:
    import argparse
    import os
    from .llm_adapter import MODEL, generate

    p = argparse.ArgumentParser(description="LEGION 30-case real local model exam")
    p.add_argument("--live", action="store_true")
    args = p.parse_args()
    if not args.live or os.getenv("LEGION_LOCAL_MODEL_PROBE") != "I_APPROVE_SYNTHETIC_LOCAL_INFERENCE":
        p.error("Explicit --live and LEGION_LOCAL_MODEL_PROBE required")
    result = evaluate(lambda prompt: generate(prompt, keep_alive="3m"))
    result["model"] = MODEL
    print(json.dumps(result, indent=2, sort_keys=True))
    # A successful process means the benchmark ran, NOT that the model passed.
    if result["completed_model_calls"] != result["exam_cases"]:
        raise SystemExit("INCOMPLETE_REAL_LLM_BENCHMARK")


if __name__ == "__main__":
    main()
