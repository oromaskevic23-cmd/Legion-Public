"""LEGION Website QA offline tests, always distinguish static QA from WCAG conformance."""
import copy
import hashlib
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from legion.commercial_gate import CommercialAccessDenied, require_professional_platform_access
from legion.lifecycle import Denied, Legion
from legion.website_qa import CHECKS, LocalReviewDenied, scan_html
from legion.website_qa_exam import evaluate, load_cases
from legion.website_qa_nca import (
    AGENT_ID, MISSION, ROLE, SECTOR, demo, run_step,
)


class WebsiteQATests(unittest.TestCase):
    def test_thirty_fixed_hand_labeled_synthetic_examples(self):
        cases=load_cases()
        self.assertEqual(len(cases),30)
        self.assertEqual(len({x["id"] for x in cases}),30)
        self.assertEqual(sum(bool(x["expected_codes"]) for x in cases),18)
        self.assertEqual(sum(not x["expected_codes"] for x in cases),12)
        self.assertEqual(len({x["category"] for x in cases}),6)
        self.assertTrue(all(x["synthetic_only"] is True for x in cases))

    def test_real_static_heuristic_matches_frozen_oracles(self):
        report=evaluate()
        self.assertEqual((report["passed"],report["total_cases"]),(30,30))
        self.assertEqual(report["failed"],0)
        self.assertEqual(report["exam_result"],"PASS_SYNTHETIC_CORPUS")
        self.assertEqual(len(report["groups"]),6)
        for group in report["groups"].values():
            self.assertEqual(group,{"passed":5,"cases":5})
        self.assertFalse(report["browser_tested"])
        self.assertFalse(report["fully_wcag_tested"])
        self.assertFalse(report["professionally_qualified"])
        self.assertFalse(report["production_authorized"])
        self.assertFalse(report["commercial_platform_access"])

    def test_finding_names_are_bounded(self):
        self.assertEqual(len(CHECKS),6)
        for case in load_cases():
            result=scan_html(case["html"])
            self.assertEqual(result["finding_codes"],sorted(case["expected_codes"]))
            self.assertFalse(result["real_client_access"])
            self.assertFalse(result["wcag_conformant"])

    def test_missing_lang_detected(self):
        x=next(c for c in load_cases() if c["id"]=="wqa-language-01")
        self.assertIn("MISSING_HTML_LANG",scan_html(x["html"])["finding_codes"])

    def test_missing_page_title_detected(self):
        x=next(c for c in load_cases() if c["id"]=="wqa-title-01")
        self.assertIn("EMPTY_PAGE_TITLE",scan_html(x["html"])["finding_codes"])

    def test_missing_image_alt_detected(self):
        x=next(c for c in load_cases() if c["id"]=="wqa-images-01")
        self.assertIn("IMAGE_MISSING_ALT",scan_html(x["html"])["finding_codes"])

    def test_empty_decorative_alt_is_not_automatically_a_violation(self):
        x=next(c for c in load_cases() if c["id"]=="wqa-images-05")
        self.assertEqual(scan_html(x["html"])["finding_codes"],[])

    def test_empty_accessible_link_name_detected(self):
        x=next(c for c in load_cases() if c["id"]=="wqa-links-03")
        self.assertIn("LINK_MISSING_NAME",scan_html(x["html"])["finding_codes"])

    def test_placeholder_is_not_accessible_label(self):
        x=next(c for c in load_cases() if c["id"]=="wqa-inputs-03")
        self.assertIn("INPUT_MISSING_LABEL",scan_html(x["html"])["finding_codes"])

    def test_label_association_with_for_id_and_wrapping(self):
        for id in ("wqa-inputs-04","wqa-inputs-05"):
            x=next(c for c in load_cases() if c["id"]==id)
            self.assertEqual(scan_html(x["html"])["finding_codes"],[])

    def test_heading_level_gap_detected(self):
        x=next(c for c in load_cases() if c["id"]=="wqa-headings-01")
        self.assertIn("HEADING_LEVEL_SKIP",scan_html(x["html"])["finding_codes"])

    def test_input_validation_denies_empty_binary_null_and_oversize(self):
        for value in ("", "a" * 40_001, "\x00", b"<html></html>", None):
            with self.subTest(value_type=type(value).__name__):
                with self.assertRaises(LocalReviewDenied):
                    scan_html(value)

    def test_broken_finding_contract_fails_examination(self):
        report=evaluate(candidate=lambda source:{
            "finding_codes":["UNAPPROVED_TOOL"],
            "production_authorized":False
        })
        self.assertEqual(report["passed"],0)
        self.assertEqual(report["exam_result"],"NEEDS_REMEDIATION")

    def test_unauthorized_production_claim_fails_examination(self):
        report=evaluate(candidate=lambda source:{
            "finding_codes":[],
            "production_authorized":True
        })
        self.assertEqual(report["passed"],0)

    def test_missing_candidate_fails_closed(self):
        def absent(source):
            raise RuntimeError("No local worker")
        report=evaluate(candidate=absent)
        self.assertEqual(report["failed"],30)
        self.assertFalse(report["commercial_platform_access"])

    def test_evidence_is_reproducible(self):
        a=evaluate()
        b=evaluate()
        self.assertEqual(a["evidence_sha256"],b["evidence_sha256"])
        self.assertEqual(len(a["dataset_sha256"]),64)

    def test_mission_execution_has_real_step_counter_and_fourth_review(self):
        with tempfile.TemporaryDirectory() as root:
            engine=Legion(Path(root)/"state.sqlite")
            engine.register(agent_id=AGENT_ID,role=ROLE,sector=SECTOR,
                            mission=MISSION,lifetime_seconds=60,
                            mission_lifetime_seconds=60,now=1000)
            engine.simulate(AGENT_ID,now=1001)
            engine.activate_sandbox(AGENT_ID,now=1002)
            cases=load_cases()
            steps=[run_step(engine,cases[i]["html"],manual_review=False,now=1003+i)
                   for i in range(3)]
            self.assertEqual([x["review"] for x in steps],["AUTO"]*3)
            with self.assertRaisesRegex(Denied,"MANUAL_REVIEW_REQUIRED"):
                run_step(engine,cases[3]["html"],manual_review=False,now=1006)
            final=run_step(engine,cases[3]["html"],manual_review=True,now=1006)
            self.assertEqual(final["review"],"MANUAL_TEST_REVIEW")
            self.assertTrue(engine.audit_valid())
            self.assertEqual(engine.inspect(AGENT_ID)["steps"],4)

    def test_agent_mission_expiration_denies_before_document_scan(self):
        with tempfile.TemporaryDirectory() as root:
            engine=Legion(Path(root)/"db.sqlite")
            engine.register(agent_id=AGENT_ID,role=ROLE,sector=SECTOR,
                            mission=MISSION,lifetime_seconds=120,
                            mission_lifetime_seconds=10,now=1000)
            engine.simulate(AGENT_ID,now=1001)
            engine.activate_sandbox(AGENT_ID,now=1002)
            with self.assertRaisesRegex(Denied,"MISSION_EXPIRED"):
                run_step(engine,load_cases()[0]["html"],manual_review=False,now=1010)

    def test_owner_global_stop_blocks_remaining_steps(self):
        evidence=demo()
        self.assertEqual(evidence["step_reviews"],["AUTO","AUTO","AUTO","MANUAL_TEST_REVIEW"])
        self.assertTrue(evidence["global_kill_stopped_execution"])
        self.assertTrue(evidence["audit_chain_valid"])
        self.assertFalse(evidence["commercial_access"])
        self.assertFalse(evidence["professionally_qualified"])

    def test_perfect_html_qa_still_cannot_access_customer_platforms(self):
        report=evaluate()
        with self.assertRaises(CommercialAccessDenied):
            require_professional_platform_access(
                exam_report=report,
                requested_platform="external-client-website",
                alleged_owner_approval="unverified-demo-approval",
            )


if __name__=="__main__":
    unittest.main()
