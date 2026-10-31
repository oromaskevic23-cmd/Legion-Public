"""Independent-oracle 12-case Playwright exam; real Chromium is mandatory.

A correct match to frozen synthetic labels is NOT professional accreditation.
"""
from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from pathlib import Path

from .browser_qa import BrowserQADenied, CATEGORIES, MAX_HTML_CHARS, probe

FIXTURES = Path(__file__).parent / "exams" / "browser_qa_12_v1.json"
VERSION = "legion-browser-qa-independent-oracle-v1"


def load_cases() -> tuple[dict, ...]:
    data = json.loads(FIXTURES.read_bytes())
    if (type(data) is not dict or set(data) != {"version", "cases"}
            or data["version"] != VERSION or type(data["cases"]) is not list
            or len(data["cases"]) != 12):
        raise BrowserQADenied("INVALID_BROWSER_EXAM_CORPUS")
    counts = Counter()
    seen = set()
    for item in data["cases"]:
        if (type(item) is not dict or set(item) != {
            "id", "category", "html", "expected_pass", "synthetic_only"
        } or type(item["id"]) is not str or item["id"] in seen
                or type(item["category"]) is not str or item["category"] not in CATEGORIES
                or type(item["html"]) is not str or not 0 < len(item["html"]) <= MAX_HTML_CHARS
                or type(item["expected_pass"]) is not bool
                or item["synthetic_only"] is not True):
            raise BrowserQADenied("INVALID_BROWSER_EXAM_CASE")
        seen.add(item["id"])
        counts[item["category"]] += 1
    if set(counts) != CATEGORIES or any(count != 2 for count in counts.values()):
        raise BrowserQADenied("INVALID_BROWSER_EXAM_COVERAGE")
    if sum(item["expected_pass"] for item in data["cases"]) != 6:
        raise BrowserQADenied("INVALID_BROWSER_EXAM_ORACLE_BALANCE")
    return tuple(data["cases"])


def evaluate(*, candidate=probe, executable_path: str | None = None) -> dict:
    # Import and browser launch exceptions must propagate; missing browsers are
    # infrastructure FAIL, never a reported passing or skipped exam.
    from playwright.sync_api import sync_playwright
    cases = load_cases()
    rows = []
    with sync_playwright() as pw:
        launch = {"headless": True}
        if executable_path is not None:
            launch["executable_path"] = executable_path
        browser = pw.chromium.launch(**launch)
        try:
            for item in cases:
                try:
                    observation = candidate(browser, item["html"], item["category"])
                    if (type(observation) is not dict
                            or type(observation.get("observed_pass")) is not bool
                            or observation.get("browser_executed") is not True
                            or observation.get("network_attempts") != 0
                            or observation.get("commercial_platform_access") is not False
                            or observation.get("production_authorized") is not False):
                        raise BrowserQADenied("INVALID_CANDIDATE_EVIDENCE")
                    actual = observation["observed_pass"]
                    matched = actual is item["expected_pass"]
                    error = None if matched else "INDEPENDENT_ORACLE_MISMATCH"
                except Exception:
                    actual = None
                    matched = False
                    error = "CANDIDATE_ERROR_OR_UNSAFE"
                rows.append({"id": item["id"], "category":item["category"],
                             "expected":item["expected_pass"], "observed":actual,
                             "matched":matched, "error":error})
            version = browser.version
        finally:
            browser.close()
    passed = sum(row["matched"] for row in rows)
    fingerprint = hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(",", ":")).encode()).hexdigest()
    return {
        "exam": VERSION,
        "cases": len(rows), "matched":passed, "mismatched":len(rows)-passed,
        "result":"PASS_SYNTHETIC_BROWSER_CORPUS" if passed == len(rows) else "FAIL_BROWSER_EXAM",
        "browser_engine":"Chromium", "browser_version":version,
        "corpus_sha256":hashlib.sha256(FIXTURES.read_bytes()).hexdigest(),
        "results_sha256":fingerprint,
        "rows":rows,
        "browser_executed":True, "synthetic_only":True,
        "wcag_conformance_proven":False, "professional_qualified":False,
        "independent_human_qa_complete":False, "production_authorized":False,
        "commercial_platform_access":False, "client_website_access":False,
    }


def main() -> None:
    path = os.environ.get("LEGION_BROWSER_EXECUTABLE")
    report = evaluate(executable_path=path)
    print(json.dumps(report, indent=2,sort_keys=True))
    if report["matched"] != report["cases"]:
        raise SystemExit("BROWSER_QA_EXAM_FAILED")


if __name__ == "__main__":
    main()
