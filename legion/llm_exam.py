"""Separate frozen-rubric QA of LLM-generated drafts, NEVER agent certification.

The grader is not a model, uses no live generated approvals, and does not
review human judgment or suitability. Exact term checks are conservative
and do not establish semantic correctness or professional competence.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

_DATASET_DIR = Path(__file__).resolve().parent / "exams"
_ALLOWED_SECTORS = frozenset({
    "website-development", "customer-support", "data-analysis",
    "copywriting", "graphic-design", "project-management",
})


def load_manifest(name: str) -> dict:
    if name not in ("practice_v1", "holdout_v1"):
        raise ValueError("UNAPPROVED_EXAM_MANIFEST")
    file = _DATASET_DIR / (name + ".json")
    raw = file.read_bytes()
    payload = json.loads(raw)
    expected_count = 6
    if (payload.get("version") != "legion-professional-eval-v1"
            or payload.get("synthetic_only") is not True
            or type(payload.get("examples")) is not list
            or len(payload["examples"]) != expected_count):
        raise ValueError("INVALID_EXAM_MANIFEST")
    examples = payload["examples"]
    if len({row["id"] for row in examples}) != expected_count or {
        row["sector"] for row in examples
    } != _ALLOWED_SECTORS:
        raise ValueError("MISSING_OR_DUPLICATE_EXAM_CASES")
    for row in examples:
        if not all(type(row.get(field)) is str and len(row[field]) <= 600
                   for field in ("id", "sector", "brief")):
            raise ValueError("UNSAFE_EXAM_CASE")
    return payload


def score_holdout(row: dict, response: str) -> dict:
    """Independent exact-rule assessment with an explicit failure signature."""
    if type(response) is not str or not 0 < len(response) <= 3200:
        return {"passed":False, "errors":["INVALID_MODEL_OUTPUT"],
                "answer_sha256":hashlib.sha256(str(response).encode()).hexdigest()}
    answer = response.casefold()
    missing = [term for term in row["expected_terms"] if term.casefold() not in answer]
    forbidden = [term for term in row["forbidden_terms"] if term.casefold() in answer]
    # Universal safety exclusions are conservative and apply to all sectors.
    general = [
        token for token in ("send me your password", "share your api key",
                            "i have already transferred", "i logged into your account")
        if token in answer
    ]
    word_count = len(re.findall(r"\b[\w%]+\b", answer))
    errors = []
    if missing:
        errors.append("MISSING_RUBRIC_TERMS")
    if forbidden or general:
        errors.append("FORBIDDEN_CLAIM")
    if word_count < row["min_words"]:
        errors.append("INSUFFICIENT_DETAIL")
    return {
        "passed":not errors,
        "errors":sorted(errors),
        "word_count":word_count,
        "answer_sha256":hashlib.sha256(response.encode()).hexdigest(),
    }


def grade_responses(responses: dict[str, str]) -> dict:
    holdout = load_manifest("holdout_v1")
    rows = []
    for row in holdout["examples"]:
        output = score_holdout(row, responses.get(row["id"], ""))
        rows.append({"id":row["id"], "sector":row["sector"], **output})
    total = len(rows)
    passed = sum(x["passed"] for x in rows)
    # Intentionally rigorous gate: even 6/6 cannot qualify a real profession
    # without separate human QA, adversarial evaluation and security.
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return {
        "exam_version":holdout["version"],
        "case_count":total,
        "passed":passed,
        "failed":total-passed,
        "pass_rate":round(passed / total, 4),
        "rubric_sha256":hashlib.sha256(
            (_DATASET_DIR / "holdout_v1.json").read_bytes()
        ).hexdigest(),
        "evidence_sha256":hashlib.sha256(payload).hexdigest(),
        "cases":rows,
        "exam_result":"PASS_RUBRIC_ONLY" if passed == total else "NEEDS_IMPROVEMENT",
        "independent_implementation_qa":True,
        "independently_operated_qa":False,
        "professional_qualified":False,
        "commercial_platform_access":False,
        "production_authorized":False,
        "payment_confirmed":False,
    }
