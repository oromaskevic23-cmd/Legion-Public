"""Single owner-controlled offline Website QA NCA pilot.

Runs only against in-memory synthetic HTML. Uses LEGION local mission expiry,
75% review window and global/agent/squad/mission stop via existing engine.
The review flag is not a signed human approval; production remains blocked.
"""
from __future__ import annotations
import hashlib
import json
import tempfile
from pathlib import Path

from .lifecycle import Denied, Legion
from .website_qa import scan_html
from .website_qa_exam import evaluate, load_cases

AGENT_ID = "NCA-LEGION-WEBSITE-QA-001"
MISSION = "synthetic-website-qa-pilot"
ROLE = "professional-accessibility-tester"
SECTOR = "accessibility-testing"


def run_step(engine: Legion, html: str, *, manual_review: bool,
             now: int) -> dict:
    """Consume precisely one bounded permitted step before inspecting text."""
    if type(html) is not str or not 0 < len(html) <= 40_000:
        raise Denied("INVALID_SYNTHETIC_HTML")
    # Synthetic input is not passed to remote services or made a tool.
    digest = hashlib.sha256(html.encode()).hexdigest()
    checked = engine.step(
        AGENT_ID,
        "Owned synthetic HTML snapshot sha256 " + digest,
        manual_review=manual_review, external_effect=False, now=now
    )
    report = scan_html(html)
    return {
        "agent":AGENT_ID,
        "mission":MISSION,
        "step":checked["step"],
        "review":checked["review"],
        "document_sha256":digest,
        "finding_codes":report["finding_codes"],
        "real_world_action":False,
        "production_authorized":False,
    }


def demo() -> dict:
    cases = load_cases()
    with tempfile.TemporaryDirectory(prefix="legion-webqa-") as root:
        engine = Legion(Path(root) / "nca.sqlite")
        engine.register(
            agent_id=AGENT_ID, role=ROLE, sector=SECTOR,
            mission=MISSION, product_class="INTERNAL",
            lifetime_seconds=180, mission_lifetime_seconds=180, now=1000
        )
        training = engine.simulate(AGENT_ID, now=1001)
        engine.activate_sandbox(AGENT_ID, now=1002)
        steps=[run_step(engine, case["html"],manual_review=(i==3),
                        now=1003+i) for i,case in enumerate(cases[:4])]
        engine.stop(scope="global",subject="*",reason="Owner demo emergency stop")
        kill_verified=False
        try:
            run_step(engine,cases[4]["html"],manual_review=False,now=1010)
        except Denied as exc:
            kill_verified = str(exc) == "OWNER_KILL_SWITCH"
        return {
            "agent":AGENT_ID,
            "role":ROLE,
            "mission":MISSION,
            "simulated_skill_cases":training["passed"],
            "step_reviews":[x["review"] for x in steps],
            "global_kill_stopped_execution":kill_verified,
            "audit_chain_valid":engine.audit_valid(),
            "site_qa_exam":{k:v for k,v in evaluate().items() if k!="results"},
            "real_world_action":False,
            "professionally_qualified":False,
            "commercial_access":False,
        }


def main() -> None:
    print(json.dumps(demo(),sort_keys=True,indent=2))


if __name__=="__main__":
    main()
