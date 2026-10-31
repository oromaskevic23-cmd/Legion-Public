"""Prevent promoting the real measured failed 30-case experiment to a certificate."""
import json
import unittest
from pathlib import Path
from legion.commercial_gate import CommercialAccessDenied, require_professional_platform_access


ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT / "legion/evidence/data_analyst_numeric_20261031.json"
WORKFLOW=ROOT / ".github/workflows/legion-data-analyst-llm.yml"


class RealDataAnalystEvidenceTest(unittest.TestCase):
    def setUp(self):
        self.data=json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_report_contains_real_failures_instead_of_a_fabricated_pass(self):
        e=self.data
        self.assertEqual((e["passed"],e["exam_cases"]),(5,30))
        self.assertEqual(e["completed_model_calls"],30)
        self.assertEqual(sum(x["passed"] for x in e["category_scores"].values()),5)
        self.assertEqual(e["failure_reasons"]["ARITHMETIC_ERROR"],24)
        self.assertEqual(e["failure_reasons"]["WRONG_UNIT"],9)
        self.assertEqual(e["status"],"MEASURED_AND_NOT_QUALIFIED")
        self.assertEqual(len(e["evidence_sha256"]),64)

    def test_no_platform_permissions_or_revenue_claimed(self):
        self.assertIs(self.data["professional_qualified"],False)
        self.assertIs(self.data["commercial_platform_access"],False)
        self.assertIs(self.data["revenue_confirmed"],False)
        self.assertIs(self.data["independently_operated_qa"],False)
        with self.assertRaises(CommercialAccessDenied):
            require_professional_platform_access(
                exam_report=self.data,
                requested_platform="any-paid-platform",
                alleged_owner_approval={"owner":"asserted-by-agent"}
            )

    def test_ollama_evidence_run_is_now_explicitly_manual_only(self):
        workflow=WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("on:\n  workflow_dispatch:\n",workflow)
        for auto in ("  pull_request:","  push:","  schedule:"):
            self.assertNotIn(auto,workflow)
        self.assertIn("permissions:\n  contents: read",workflow)

    def test_source_of_truth_is_exact_actions_run(self):
        e=self.data
        self.assertEqual(e["run_id"],41149646836)
        self.assertEqual(e["model"],"smollm2:1.7b-instruct-q4_K_M")
        self.assertEqual(len(e["tested_commit_sha"]),40)
        self.assertEqual(e["source"],"PUBLIC_GITHUB_ACTIONS_COMPLETED_JOB_LOG")


if __name__=="__main__":
    unittest.main()
