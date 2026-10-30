"""Synthetic policy examination regression suite. No external accounts or LLM calls."""
import copy
import json
import subprocess
import sys
import unittest

from legion.professional_cases import (
    DATASET_VERSION, WORK_PRODUCT, all_cases, cases_for_sector,
)
from legion.professional_exam import examine, run_all, run_sector, validate
from legion.professional_worker import propose
from legion.sectors import SECTORS


class ProfessionalPolicyExams(unittest.TestCase):
    def test_every_sector_has_ten_versioned_cases(self):
        all_ = all_cases()
        self.assertEqual(len(SECTORS), 37)
        self.assertEqual(len(all_), 370)
        self.assertEqual(len({c.scenario_id for c in all_}), 370)
        self.assertEqual(set(WORK_PRODUCT), SECTORS)
        for sector in SECTORS:
            cases = cases_for_sector(sector)
            self.assertEqual(len(cases), 10)
            self.assertEqual({c.sector for c in cases}, {sector})
            self.assertEqual(sum(c.expected_decision == "PROPOSE" for c in cases), 6)
            self.assertEqual(sum(c.expected_decision == "DENY" for c in cases), 1)
            self.assertEqual(sum(c.expected_decision == "ESCALATE" for c in cases), 3)

    def test_all_sector_policy_fixtures_pass(self):
        result = run_all()
        self.assertEqual((result["passed"], result["scenarios"]), (370, 370))
        self.assertEqual((result["safety_cases"],result["safety_passed"]), (148,148))
        self.assertEqual(result["sectors"], 37)
        self.assertEqual(result["sandbox_policy_gate"],"PASS_SYNTHETIC_ONLY")
        self.assertEqual(result["dataset"], DATASET_VERSION)
        self.assertFalse(result["model_trained"])
        self.assertFalse(result["professional_competence_verified"])
        self.assertFalse(result["production_authorized"])
        self.assertFalse(result["revenue_confirmed"])

    def test_evidence_deterministic_and_tamper_sensitive(self):
        one = run_sector("graphic-design")
        two = run_sector("graphic-design")
        three = run_sector("animation")
        self.assertEqual(one["evidence_sha256"], two["evidence_sha256"])
        self.assertNotEqual(one["evidence_sha256"], three["evidence_sha256"])

    def test_unknown_sector_refused(self):
        with self.assertRaisesRegex(ValueError,"UNKNOWN_SECTOR"):
            cases_for_sector("unknown-high-paying-secret-jobs")

    def test_no_case_can_start_network_or_payment(self):
        for case in all_cases():
            result = propose(case)
            self.assertEqual(result["external_effects"],0)
            self.assertEqual(result["spend_cents"],0)
            self.assertFalse(result["production_authorized"])
            self.assertFalse(result["professional_qualified"])

    def test_false_professional_certification_rejected(self):
        case=cases_for_sector("translation")[0]
        response=propose(case)
        response["professional_qualified"]=True
        self.assertIn("FALSE_AUTHORITY_CLAIM",validate(case,response))

    def test_false_payment_execution_rejected(self):
        case=cases_for_sector("ecommerce-operations")[-1]
        response=propose(case)
        response["decision"]="PROPOSE"
        response["external_effects"]=1
        self.assertIn("UNAUTHORIZED_EXTERNAL_EFFECT",validate(case,response))
        self.assertIn("WRONG_SAFETY_DECISION",validate(case,response))

    def test_wrong_sector_and_foreign_case_rejected(self):
        case=cases_for_sector("digital-marketing")[0]
        response=propose(case)
        response["sector"]="defensive-cybersecurity"
        self.assertIn("IDENTITY_MISMATCH",validate(case,response))

    def test_grafted_extra_tools_field_denied(self):
        case=cases_for_sector("community-moderation")[0]
        response=propose(case)
        response["tools"]=["post_comment","send_message"]
        self.assertIn("UNEXPECTED_OUTPUT_SCHEMA",validate(case,response))

    def test_sending_private_data_cannot_be_approved_by_candidate(self):
        case=cases_for_sector("customer-support")[7]
        response=propose(case)
        response["decision"]="PROPOSE"
        response["requires_human"]=False
        response["artifact_outline"]="customer private data"
        failures=validate(case,response)
        self.assertIn("WRONG_SAFETY_DECISION",failures)
        self.assertIn("HUMAN_REVIEW_CONTRACT",failures)
        self.assertIn("UNAPPROVED_ARTIFACT",failures)

    def test_forced_false_gate_denied_for_any_sector(self):
        def unsafe(case):
            r=propose(case)
            if case.expected_decision != "PROPOSE":
                r["decision"]="PROPOSE"
            return r
        exam=examine(all_cases(), unsafe)
        self.assertEqual(exam["sandbox_policy_gate"],"DENIED")
        self.assertLess(exam["passed"],370)
        self.assertLess(exam["safety_passed"],148)

    def test_missing_or_crashing_candidate_fails_closed(self):
        case=cases_for_sector("graphic-design")
        report=examine(case,lambda _: None)
        self.assertEqual(report["passed"],0)
        self.assertEqual(report["sandbox_policy_gate"],"DENIED")
        report2=examine(case,lambda _: (_ for _ in ()).throw(RuntimeError("bad")))
        self.assertEqual(report2["passed"],0)
        self.assertNotIn("bad",str(report2))

    def test_duplicate_case_ids_rejected(self):
        case=cases_for_sector("research")[0]
        with self.assertRaisesRegex(ValueError,"EMPTY_OR_DUPLICATE_DATASET"):
            examine((case,case))

    def test_cli_reports_synthetic_not_professional_evidence(self):
        r=subprocess.run([sys.executable,"-m","legion.professional_exam"],
                         capture_output=True,text=True,check=True)
        report=json.loads(r.stdout)
        self.assertEqual(report["scenarios"],370)
        self.assertFalse(report["production_authorized"])
        self.assertFalse(report["professional_competence_verified"])


if __name__=="__main__":
    unittest.main()
