"""LEGION Website QA frozen synthetic defect exam (manual oracle labeling).

The oracle is kept in the fixture file, separate from the inspector code.
A pass validates these 30 examples, not browser behavior or WCAG conformity.
"""
from __future__ import annotations
import hashlib
import json
from collections import Counter
from pathlib import Path

from .website_qa import CHECKS, LocalReviewDenied, scan_html

FIXTURES = Path(__file__).parent / "exams" / "website_qa_30_v1.json"
VERSION = "legion-website-qa-hand-labeled-v1"
GROUPS = frozenset({"language", "title", "images", "links", "inputs", "headings"})


def load_cases() -> tuple[dict, ...]:
    manifest = json.loads(FIXTURES.read_bytes())
    if (type(manifest) is not dict or manifest.get("version") != VERSION
            or type(manifest.get("cases")) is not list or len(manifest["cases"]) != 30):
        raise ValueError("INVALID_WEBSITE_QA_CORPUS")
    seen = set()
    groups = Counter()
    for row in manifest["cases"]:
        if type(row) is not dict or set(row) != {
            "id", "category", "html", "expected_codes", "synthetic_only"
        }:
            raise ValueError("INVALID_CASE_SCHEMA")
        if (type(row["id"]) is not str or row["id"] in seen
                or type(row["category"]) is not str or row["category"] not in GROUPS
                or type(row["html"]) is not str or type(row["expected_codes"]) is not list
                or row["synthetic_only"] is not True
                or len(row["html"]) > 40_000):
            raise ValueError("INVALID_CASE_METADATA")
        if (len(set(row["expected_codes"])) != len(row["expected_codes"])
                or any(x not in CHECKS for x in row["expected_codes"])):
            raise ValueError("INVALID_CASE_ORACLE")
        seen.add(row["id"])
        groups[row["category"]] += 1
    if set(groups) != GROUPS or any(v != 5 for v in groups.values()):
        raise ValueError("INCOMPLETE_WEBSITE_QA_COVERAGE")
    return tuple(manifest["cases"])


def evaluate(*, candidate=scan_html) -> dict:
    rows = []
    for case in load_cases():
        try:
            output = candidate(case["html"])
            if type(output) is not dict:
                raise ValueError("MALFORMED_CANDIDATE")
            actual = output.get("finding_codes")
            if (type(actual) is not list or len(set(actual)) != len(actual)
                    or any(code not in CHECKS for code in actual)):
                raise ValueError("INVALID_FINDINGS_SCHEMA")
            if output.get("production_authorized") is not False:
                raise ValueError("UNSAFE_AUTHORITY_CLAIM")
            expected = sorted(case["expected_codes"])
            errors = [] if sorted(actual) == expected else ["DEFECT_ORACLE_MISMATCH"]
        except Exception:
            actual = []
            errors = ["CANDIDATE_UNAVAILABLE_OR_UNSAFE"]
        rows.append({
            "id":case["id"],
            "category":case["category"],
            "expected":sorted(case["expected_codes"]),
            "actual":actual,
            "passed":not errors,
            "errors":errors,
        })
    counts={}
    for group in sorted(GROUPS):
        subset=[r for r in rows if r["category"]==group]
        counts[group]={"passed":sum(x["passed"] for x in subset), "cases":len(subset)}
    passed=sum(x["passed"] for x in rows)
    evidence=hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return {
        "dataset":VERSION,
        "dataset_sha256":hashlib.sha256(FIXTURES.read_bytes()).hexdigest(),
        "evidence_sha256":evidence,
        "total_cases":len(rows),
        "passed":passed,
        "failed":len(rows)-passed,
        "groups":counts,
        "results":rows,
        "exam_result":"PASS_SYNTHETIC_CORPUS" if passed==len(rows) else "NEEDS_REMEDIATION",
        "browser_tested":False,
        "fully_wcag_tested":False,
        "professionally_qualified":False,
        "independently_operated_qa":False,
        "real_client_access":False,
        "production_authorized":False,
        "commercial_platform_access":False,
    }


def main() -> None:
    report=evaluate()
    print(json.dumps(report,sort_keys=True,indent=2))
    if report["passed"] != 30:
        raise SystemExit("WEBSITE_QA_CORPUS_FAILED")


if __name__=="__main__":
    main()
