"""LEGION Data Analyst benchmark regression and prompt-manipulation defenses."""
import json
import unittest
from decimal import Decimal

from legion.commercial_gate import (
    CommercialAccessDenied, require_professional_platform_access,
)
from legion.data_analyst_cases import build_cases, dataset_sha256, prompt_for
from legion.data_analyst_exam import evaluate, score_case
from legion.llm_adapter import MODEL, generate
from legion.competency_matrix import standard_for_sector


def correct_response(prompt: str) -> str:
    # Test double ONLY. Never mistake this deterministic fixture for model inference.
    for case in build_cases():
        if prompt_for(case) == prompt:
            return json.dumps({"answer": float(case.expected), "unit": case.unit})
    raise ValueError("UNRECOGNIZED_EXAM_PROMPT")


class DataAnalystProfessionalTest(unittest.TestCase):
    def test_thirty_diverse_numeric_scenarios(self):
        cases=build_cases()
        self.assertEqual(len(cases),30)
        self.assertEqual(len({c.id for c in cases}),30)
        self.assertEqual(
            {k:sum(c.category==k for c in cases)
             for k in ("conversion","total","mean")},
            {"conversion":10,"total":10,"mean":10})
        for case in cases:
            self.assertGreater(case.expected,Decimal(0))

    def test_no_expected_answer_leaks_to_model_prompt_schema(self):
        for case in build_cases():
            p=prompt_for(case)
            self.assertIn('Reply ONLY with one JSON object:',p)
            self.assertNotIn('expected"',p)
            self.assertNotIn("PRIVATE_KEY",p)
            self.assertLess(len(p),2400)

    def test_holdout_manifest_is_reproducible(self):
        self.assertEqual(dataset_sha256(),dataset_sha256())
        self.assertEqual(len(dataset_sha256()),64)

    def test_exact_numeric_reference_candidate_passes_without_becoming_professional(self):
        report=evaluate(correct_response)
        self.assertEqual((report["passed"],report["exam_cases"]),(30,30))
        self.assertEqual(report["completed_model_calls"],30)
        self.assertEqual(report["exam_result"],"RUBRIC_ONLY_PASS")
        self.assertTrue(report["independent_implementation_qa"])
        self.assertFalse(report["independently_operated_qa"])
        self.assertFalse(report["professionally_qualified"])
        self.assertFalse(report["production_authorized"])
        self.assertFalse(report["commercial_platform_access"])
        self.assertEqual(report["external_effects"],0)
        self.assertFalse(report["training_weights_modified"])
        with self.assertRaises(CommercialAccessDenied):
            require_professional_platform_access(
                exam_report=report,requested_platform="any-freelance-platform",
                alleged_owner_approval=True)

    def test_wrong_numeric_answer_fails(self):
        case=build_cases()[0]
        resp=json.dumps({"answer":9999,"unit":case.unit})
        self.assertIn("ARITHMETIC_ERROR",score_case(case,resp)["errors"])

    def test_wrong_unit_fails(self):
        case=build_cases()[0]
        resp=json.dumps({"answer":float(case.expected),"unit":"USD"})
        self.assertIn("WRONG_UNIT",score_case(case,resp)["errors"])

    def test_model_cannot_inject_commercial_authority(self):
        case=build_cases()[0]
        resp=json.dumps({"answer":float(case.expected),"unit":case.unit,
                         "production_authorized":True,
                         "payment_confirmed":True})
        self.assertIn("INVALID_RESULT_SCHEMA",score_case(case,resp)["errors"])

    def test_model_cannot_embed_shell_instruction(self):
        case=build_cases()[0]
        resp=json.dumps({"answer":float(case.expected),"unit":case.unit,
                         "command":"unapproved shell action"})
        self.assertIn("INVALID_RESULT_SCHEMA",score_case(case,resp)["errors"])

    def test_model_markup_refused(self):
        case=build_cases()[0]
        resp='~~~json\n'+json.dumps({"answer":float(case.expected),"unit":case.unit})+'\n~~~'
        self.assertIn("INVALID_JSON",score_case(case,resp)["errors"])

    def test_boolean_result_refused(self):
        case=build_cases()[0]
        resp=json.dumps({"answer":True,"unit":case.unit})
        self.assertIn("INVALID_NUMBER",score_case(case,resp)["errors"])

    def test_invalid_numeric_type_refused(self):
        case=build_cases()[0]
        resp=json.dumps({"answer":"NaN","unit":case.unit})
        self.assertIn("INVALID_NUMBER",score_case(case,resp)["errors"])

    def test_missing_candidate_fails_all_30_cases(self):
        def unavailable(_):
            raise RuntimeError("simulated unavailable inference, not a live model")
        report=evaluate(unavailable)
        self.assertEqual(report["passed"],0)
        self.assertEqual(report["completed_model_calls"],0)
        self.assertEqual(report["failure_reasons"],{"CANDIDATE_UNAVAILABLE":30})
        self.assertFalse(report["commercial_platform_access"])
        self.assertNotIn("simulated unavailable inference",str(report))

    def test_deterministic_failure_evidence(self):
        a=evaluate(lambda _: "not JSON")
        b=evaluate(lambda _: "not JSON")
        self.assertEqual(a["evidence_sha256"],b["evidence_sha256"])
        self.assertEqual(a["passed"],0)
        self.assertEqual(a["failure_reasons"],{"INVALID_JSON":30})

    def test_no_live_browser_or_payment_permissions(self):
        st=standard_for_sector("data-analysis")
        self.assertFalse(st["external_effects_allowed_in_pilot"])
        self.assertTrue(st["short_lived_mission_required"])
        self.assertEqual(st["max_unattended_eligible_step_ratio"],0.75)

    def test_llm_keep_alive_is_explicitly_bounded(self):
        def responder(req, **kwargs):
            raise AssertionError("No HTTP call should be performed")
        for bad in ("1h","forever",1000,True):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                generate("synthetic prompt",keep_alive=bad,open_request=responder)

    def test_llm_allowed_keep_alive_remains_loopback_and_tool_free(self):
        class Reply:
            headers={"Content-Type":"application/json"}
            def __enter__(self):return self
            def __exit__(self,*a):return False
            def read(self,n):
                return json.dumps({"response":"synthetic","model":MODEL,"done":True}).encode()
        def capture(request,**kwargs):
            self.assertEqual(request.full_url,"http://127.0.0.1:11434/api/generate")
            body=json.loads(request.data)
            self.assertEqual(body["keep_alive"],"3m")
            self.assertEqual(body["stream"],False)
            self.assertNotIn("tools",body)
            return Reply()
        self.assertEqual(generate("synthetic",keep_alive="3m",open_request=capture),
                         "synthetic")


if __name__=="__main__":
    unittest.main()
