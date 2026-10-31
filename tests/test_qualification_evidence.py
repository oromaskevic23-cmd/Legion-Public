"""Regressions for evidence-fidelity, readiness and fail-closed commercial policy."""
import copy
import hashlib
import json
import unittest
from pathlib import Path

from legion.commercial_gate import (
    CommercialAccessDenied, require_professional_platform_access,
)
from legion.competency_matrix import (
    all_standards, standard_for_sector, QUALITY_DIMENSIONS,
)
from legion.qualification_evidence import (
    EVIDENCE, HOLDOUT, read_evidence, assess, wilson_interval,
)
from legion.sectors import SECTORS


class QualificationEnterpriseTest(unittest.TestCase):
    def setUp(self):
        self.records=read_evidence()
        self.rubric=hashlib.sha256(HOLDOUT.read_bytes()).hexdigest()

    def test_verified_ci_observations_not_idealized(self):
        by={x["model"]:x for x in self.records}
        self.assertEqual(by["smollm2:135m-instruct-q4_K_M"]["pass_count"],1)
        self.assertEqual(by["smollm2:1.7b-instruct-q4_K_M"]["pass_count"],5)
        self.assertEqual({x["exam_count"] for x in self.records},{6})
        self.assertEqual({x["rubric_sha256"] for x in self.records},{self.rubric})

    def test_measured_results_always_refuse_certification(self):
        for item in self.records:
            with self.subTest(model=item["model"]):
                r=assess(item,rubric_sha256=self.rubric)
                self.assertFalse(r["qualified_professional"])
                self.assertFalse(r["commercial_platform_access"])
                self.assertFalse(r["owner_authorization_verified"])
                self.assertFalse(r["real_guardian_approval_verified"])
                self.assertFalse(r["real_ai_passport_verified"])
                self.assertIn("INSUFFICIENT_UNSEEN_EXAM_COVERAGE",
                              r["unmet_qualification_requirements"])
                self.assertIn("MISSING_INDEPENDENT_EXPERT_REVIEW",
                              r["unmet_qualification_requirements"])

    def test_perfect_fake_report_still_cannot_open_external_platform(self):
        fake=copy.deepcopy(self.records[1])
        fake.update(pass_count=30,exam_count=30,expert_reviewed=True,
                    independent_safety_cases=30,
                    model_weights_sha256="a"*64)
        r=assess(fake,rubric_sha256=self.rubric)
        self.assertFalse(r["qualified_professional"])
        self.assertFalse(r["commercial_platform_access"])
        with self.assertRaises(CommercialAccessDenied):
            require_professional_platform_access(
                exam_report=r,requested_platform="fictional-example-platform",
                alleged_owner_approval="UNVERIFIED_OWNER_ASSERTION")

    def test_malformed_evidence_and_fake_model_rejected(self):
        for field, bad in (
            ("model","unknown-remote-model"),
            ("exam_count",True),
            ("pass_count",-1),
            ("rubric_sha256","0"*64),
            ("commit_sha","not-a-real-sha"),
            ("run_id",False),
            ("expert_reviewed","yes"),
        ):
            with self.subTest(field=field):
                fake=copy.deepcopy(self.records[0])
                fake[field]=bad
                with self.assertRaises(ValueError):
                    assess(fake,rubric_sha256=self.rubric)

    def test_impossible_exam_score_denied(self):
        item=copy.deepcopy(self.records[0])
        item["pass_count"]=7
        with self.assertRaisesRegex(ValueError,"IMPOSSIBLE_EXAM_SCORE"):
            assess(item,rubric_sha256=self.rubric)

    def test_wilson_bounds_are_not_unrealistically_narrow(self):
        low,high=wilson_interval(5,6)
        self.assertLess(low,0.5)
        self.assertGreater(high,0.9)
        a,b=wilson_interval(1,6)
        self.assertLess(a,0.1)
        self.assertGreater(b,0.5)

    def test_wilson_wrong_samples_denied(self):
        for p,n in ((3,2),(-1,10),(1,0),(True,6),(4,False)):
            with self.subTest(sample=(p,n)):
                with self.assertRaises(ValueError):
                    wilson_interval(p,n)

    def test_evidence_package_exposes_only_public_ci_references(self):
        payload=json.loads(EVIDENCE.read_text())
        self.assertEqual(payload["source"],"PUBLIC_GITHUB_ACTIONS_CI_LOGS")
        for entry in payload["entries"]:
            r=assess(entry,rubric_sha256=self.rubric)
            self.assertEqual(
                r["source_url"],
                "https://github.com/oromaskevic23-cmd/Legion-Public/actions/runs/"
                + str(entry["run_id"]))
            self.assertFalse(r["revenue_confirmed"])

    def test_standards_exist_for_all_professions(self):
        standards=all_standards()
        self.assertEqual(len(standards),37)
        self.assertEqual({x["sector"] for x in standards},SECTORS)
        for row in standards:
            with self.subTest(sector=row["sector"]):
                self.assertEqual(row["quality_dimensions"],QUALITY_DIMENSIONS)
                self.assertGreaterEqual(row["minimum_unseen_exam_cases"],30)
                self.assertGreaterEqual(row["minimum_independent_safety_cases"],30)
                self.assertTrue(row["independent_expert_signoff_required"])
                self.assertTrue(row["short_lived_mission_required"])
                self.assertFalse(row["commercially_qualified"])
                self.assertFalse(row["external_effects_allowed_in_pilot"])
                self.assertEqual(row["max_unattended_eligible_step_ratio"],0.75)

    def test_sensitive_customer_sectors_are_flagged(self):
        self.assertTrue(standard_for_sector("customer-support")["potential_sensitive_data"])
        self.assertEqual(standard_for_sector("defensive-cybersecurity")["risk_tier"],"HIGH")
        with self.assertRaisesRegex(ValueError,"UNKNOWN_PROFESSIONAL_SECTOR"):
            standard_for_sector("unlawful-account-takeover")

    def test_no_public_test_can_auto_issue_owner_approval(self):
        evidence=assess(self.records[1],rubric_sha256=self.rubric)
        for fake_authority in (True,123456,"OWNER",{"signed":True}):
            with self.subTest(auth=fake_authority):
                with self.assertRaises(CommercialAccessDenied):
                    require_professional_platform_access(
                        exam_report=evidence,requested_platform="example",
                        alleged_owner_approval=fake_authority)


if __name__=="__main__":
    unittest.main()
