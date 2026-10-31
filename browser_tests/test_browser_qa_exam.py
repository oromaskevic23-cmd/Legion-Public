"""Actual browser tests, intentionally separate from dependency-free offline suite."""
import unittest

from legion.browser_qa import BrowserQADenied, probe
from legion.browser_qa_exam import evaluate, load_cases


class BrowserExamTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import os
        cls.browser_path = os.environ.get("LEGION_BROWSER_EXECUTABLE")

    def test_frozen_independent_oracle(self):
        cases = load_cases()
        self.assertEqual(len(cases), 12)
        self.assertEqual(sum(x["expected_pass"] for x in cases), 6)
        self.assertEqual(len({x["category"] for x in cases}), 6)

    def test_real_chromium_passes_all_behavioral_oracles(self):
        report = evaluate(executable_path=self.browser_path)
        self.assertEqual((report["matched"], report["cases"]), (12, 12))
        self.assertTrue(report["browser_executed"])
        self.assertFalse(report["professional_qualified"])
        self.assertFalse(report["commercial_platform_access"])
        self.assertFalse(report["wcag_conformance_proven"])

    def test_always_claiming_success_fails_six_negative_controls(self):
        def fake(browser, html, category):
            return {"observed_pass": True, "browser_executed": True,
                    "network_attempts":0,"commercial_platform_access":False,
                    "production_authorized":False}
        report = evaluate(candidate=fake, executable_path=self.browser_path)
        self.assertEqual(report["matched"], 6)
        self.assertEqual(report["result"], "FAIL_BROWSER_EXAM")

    def test_no_evidence_fails_closed(self):
        report = evaluate(candidate=lambda b,h,c: {"observed_pass":True},
                          executable_path=self.browser_path)
        self.assertEqual(report["matched"], 0)
        self.assertFalse(report["production_authorized"])

    def test_external_capability_is_denied(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True, **({"executable_path":self.browser_path} if self.browser_path else {}))
            try:
                for html in ('<img src="https://example.org/x">',
                             '<script>fetch("/secret")</script>',
                             '<iframe src="about:blank"></iframe>'):
                    with self.assertRaises(BrowserQADenied):
                        probe(browser, html, "click")
            finally:
                browser.close()


if __name__ == "__main__":
    unittest.main()
