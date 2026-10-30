"""LEGION deterministic simulator, not LLM fine-tuning or professional certification.

Fixture checks model the pathway to later domain-specific training/evaluation.
Only owned synthetic text enters these exercises; no external services exist.
"""
from __future__ import annotations

import hashlib
import json
import re

SAMPLES = tuple(
    f"Mission {i}: Example report has {i} records. "
    f"Test flag {'risk' if i % 2 else 'clear'}; all data synthetic."
    for i in range(1, 13)
)


def perform_local_skill(skill: str, text: str) -> dict:
    if skill == "SHA256_TEXT":
        return {"digest": hashlib.sha256(text.encode()).hexdigest(),
                "input_bytes": len(text.encode())}
    if skill == "TEXT_METRICS":
        return {"characters": len(text), "words": len(text.split()),
                "lines": len(text.splitlines())}
    if skill == "RISK_MARKERS":
        # A literal marker search in a toy fixture, NOT security analysis.
        return {"literal_risk_marker_count": len(re.findall(r"\brisk\b", text.lower()))}
    raise ValueError("UNSUPPORTED_SYNTHETIC_SKILL")


def _reference(skill: str, text: str) -> dict:
    """Independent arithmetic path: not a formal third-party QA process."""
    encoded=text.encode()
    if skill == "SHA256_TEXT":
        digest=hashlib.new("sha256")
        digest.update(encoded)
        return {"digest": digest.hexdigest(), "input_bytes": len(encoded)}
    if skill == "TEXT_METRICS":
        return {"characters": sum(1 for _ in text), "words": len(text.split()),
                "lines": len(text.splitlines())}
    if skill == "RISK_MARKERS":
        tokens=re.split(r"\W+", text.casefold())
        return {"literal_risk_marker_count": sum(x=="risk" for x in tokens)}
    raise ValueError("UNSUPPORTED_SYNTHETIC_SKILL")


def run_simulation(skill: str) -> dict:
    observations=[]
    for i, sample in enumerate(SAMPLES,1):
        answer=perform_local_skill(skill,sample)
        expected=_reference(skill,sample)
        observations.append({"scenario":i,"passed":answer==expected,
                             "response_sha256":hashlib.sha256(
                                 json.dumps(answer,sort_keys=True).encode()).hexdigest()})
    artifact=json.dumps({"skill":skill,"cases":observations},
                        sort_keys=True,separators=(",",":")).encode()
    return {"skill":skill,"total":len(observations),
            "passed":sum(x["passed"] for x in observations),
            "evidence_sha256":hashlib.sha256(artifact).hexdigest(),
            "scope":"synthetic-deterministic-fixtures-not-professional-certification"}
