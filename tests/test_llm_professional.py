"""No live model needed for regression checks; actual LLM CI is separately run."""
import json
import unittest
from urllib.error import URLError
from legion.llm_adapter import MODEL, URL, ModelUnavailable, generate
from legion.llm_exam import grade_responses, load_manifest, score_holdout
from legion.llm_training import practice_then_examine, _prompt
from legion.commercial_gate import CommercialAccessDenied, require_professional_platform_access


class FakeHttpResponse:
    headers = {"Content-Type":"application/json"}
    def __init__(self, data):
        self.data = data
    def read(self, limit):
        return self.data[:limit]
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False


class ProfessionalLLMTests(unittest.TestCase):
    def fake_llm(self, prompt):
        self.assertNotIn("expected_terms",prompt)
        self.assertNotIn("forbidden_terms",prompt)
        self.assertNotIn("min_words",prompt)
        self.assertIn("TRAINING SANDBOX ONLY.", prompt)
        return "Draft for fictional work only. Please review accessibility and customer consent before any action."

    def test_live_model_workflow_is_explicitly_manual_only(self):
        from pathlib import Path
        root=Path(__file__).resolve().parents[1]
        workflow=(root/".github/workflows/legion-llm-evidence.yml").read_text()
        self.assertIn("on:\n  workflow_dispatch:",workflow)
        for automatic in ("  pull_request:", "  push:", "  schedule:"):
            self.assertNotIn(automatic,workflow)
        self.assertIn("LEGION_LOCAL_MODEL:",workflow)
        self.assertIn("python3 -m legion.llm_training --live",workflow)

    def test_holdout_is_separate_from_practice(self):
        p = load_manifest("practice_v1")["examples"]
        h = load_manifest("holdout_v1")["examples"]
        self.assertEqual(len(p),6)
        self.assertEqual(len(h),6)
        self.assertTrue({x["id"] for x in p}.isdisjoint({x["id"] for x in h}))

    def test_rubric_not_in_prompt(self):
        h=load_manifest("holdout_v1")["examples"][0]
        prompt=_prompt(h["sector"], h["brief"])
        self.assertNotIn("expected_terms", prompt)
        self.assertNotIn("forbidden_terms",prompt)
        self.assertLess(len(prompt),2400)

    def test_full_mock_training_reports_no_authorization_or_weight_update(self):
        r=practice_then_examine(self.fake_llm,max_practice_revisions=3)
        self.assertEqual(r["practice_cases"],6)
        self.assertEqual(r["practice_revisions"],3)
        self.assertEqual(r["inference_calls"],15)
        self.assertFalse(r["professional_qualified"])
        self.assertFalse(r["commercial_platform_access"])
        self.assertTrue(r["no_model_weight_updates"])
        self.assertFalse(r["model_training_completed"])
        self.assertEqual(r["source"],"injected_test_candidate")
        self.assertEqual(len(r["cases"]),6)

    def test_perfect_holdout_cannot_grant_license_or_account_access(self):
        manifest=load_manifest("holdout_v1")["examples"]
        answers={
            task["id"]:
                "A safe fictional draft: " + " ".join(task["expected_terms"])
                + " includes review, quality checks, and an authorized owner."
            for task in manifest
        }
        report=grade_responses(answers)
        self.assertEqual(report["passed"],6)
        self.assertEqual(report["exam_result"],"PASS_RUBRIC_ONLY")
        self.assertFalse(report["professional_qualified"])
        self.assertFalse(report["production_authorized"])
        with self.assertRaises(CommercialAccessDenied):
            require_professional_platform_access(
                exam_report=report, requested_platform="example-freelance-site",
                alleged_owner_approval="FAKE_OWNER_OTP"
            )

    def test_malicious_extra_field_cannot_grant_real_work(self):
        report={"passed":6,"professional_qualified":True,"production_authorized":True}
        with self.assertRaisesRegex(CommercialAccessDenied,"PRODUCTION_CONNECTORS_NOT_IMPLEMENTED"):
            require_professional_platform_access(
                exam_report=report,requested_platform="example",alleged_owner_approval=True
            )

    def test_rubric_fails_on_wrong_conversion_answer(self):
        task=[t for t in load_manifest("holdout_v1")["examples"] if t["sector"]=="data-analysis"][0]
        result=score_holdout(task,"The rate is 20% per order, guaranteed profits.")
        self.assertFalse(result["passed"])
        self.assertIn("MISSING_RUBRIC_TERMS",result["errors"])
        self.assertIn("FORBIDDEN_CLAIM",result["errors"])

    def test_rubric_fails_on_password_request(self):
        task=[t for t in load_manifest("holdout_v1")["examples"] if t["sector"]=="customer-support"][0]
        result=score_holdout(task,"We can help with your account. Send me your password to proceed.")
        self.assertFalse(result["passed"])
        self.assertIn("FORBIDDEN_CLAIM",result["errors"])

    def test_rubric_denies_empty_model_output(self):
        task=load_manifest("holdout_v1")["examples"][0]
        self.assertEqual(score_holdout(task,"")["errors"],["INVALID_MODEL_OUTPUT"])

    def test_inference_request_is_loopback_only_without_tools(self):
        def open_request(req, **kwargs):
            self.assertEqual(req.full_url,URL)
            self.assertEqual(kwargs["timeout"],100)
            body=json.loads(req.data)
            self.assertEqual(body["model"],MODEL)
            self.assertEqual(body["stream"],False)
            self.assertEqual(body["keep_alive"],0)
            self.assertNotIn("tools",body)
            return FakeHttpResponse(json.dumps({
                "model":MODEL,"response":"Synthetic test response.","done":True
            }).encode())
        self.assertEqual(generate("Only synthetic content.",open_request=open_request),
                         "Synthetic test response.")

    def test_untrusted_external_model_is_rejected(self):
        def bad(req,**kwargs):
            return FakeHttpResponse(json.dumps({
                "model":"outside:wrong","response":"Injected response","done":True
            }).encode())
        with self.assertRaisesRegex(ModelUnavailable,"INVALID_LOCAL_MODEL_RESPONSE"):
            generate("Synthetic prompt",open_request=bad)

    def test_remote_redirect_fails_closed(self):
        def redirect(req,**kwargs):
            raise URLError("Blocked external redirect")
        with self.assertRaisesRegex(ModelUnavailable,"LOCAL_MODEL_NOT_AVAILABLE"):
            generate("Synthetic prompt",open_request=redirect)

    def test_large_or_empty_prompt_fails_before_network(self):
        def unreachable(req,**kwargs):
            raise AssertionError("must not execute")
        for prompt in ("","x"*2401):
            with self.assertRaises(ValueError):
                generate(prompt,open_request=unreachable)

    def test_unrelated_manifest_is_rejected(self):
        with self.assertRaisesRegex(ValueError,"UNAPPROVED_EXAM_MANIFEST"):
            load_manifest("training_private_keys")

    def test_missing_model_draft_does_not_pass(self):
        r=grade_responses({})
        self.assertEqual(r["passed"],0)
        self.assertEqual(r["exam_result"],"NEEDS_IMPROVEMENT")
        self.assertFalse(r["commercial_platform_access"])

    def test_bad_revision_count_denied(self):
        with self.assertRaisesRegex(ValueError,"INVALID_REVISION_COUNT"):
            practice_then_examine(self.fake_llm,max_practice_revisions=7)


if __name__ == "__main__":
    unittest.main()
