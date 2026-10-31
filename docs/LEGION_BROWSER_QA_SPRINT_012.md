# LEGION — Sprint 012: Real Chromium, synthetic Website QA exam

**Founder and Final Architectural Decision Authority:** Alexander Nikolaevich Romaskevich (RomaskevicH)  
**Scope:** one local-browser Website QA competency probe. **Not deployed**, not a commercial service, not a WCAG compliance certificate.  
**Change classification:** professional training evidence; **no change to commercial/production permissions**.

## Execution chain

Architect → HANTER (AI Command Center) → federated domain orchestrator → LEGION → `NCA-LEGION-WEBSITE-QA-001` (existing offline pilot identity). The browser exam is a QA instrument, not a continuously operating NCA or delegated authorization.

- Twelve **repository-owned synthetic** HTML cases: one positive and one negative per category (mouse click, keyboard focus, accessible textbox name, ARIA status update, disclosure state, native required-field validation).
- Test descriptions and independent oracle labels: [`browser_qa_12_v1.json`](../legion/exams/browser_qa_12_v1.json).
- Browser behavior probe: [`browser_qa.py`](../legion/browser_qa.py), using real Playwright Chromium. Does not read labels.
- Exam scorer: [`browser_qa_exam.py`](../legion/browser_qa_exam.py), comparing observed behavior with frozen oracle, SHA-256 of inputs/results, collecting negative controls and failing closed on errors or missing browser.
- Separate actual-browser tests: [`test_browser_qa_exam.py`](../browser_tests/test_browser_qa_exam.py). PR CI installs pinned Playwright + browser; no permanent server or API tokens.

## Containment and truthful limits

- Only our synthetic fixture corpus is run. Browser context uses `offline=True`, blocks service workers, aborts routed requests, and disallows downloads/permissions.
- These safeguards **are not equivalent to a hardened OS-level sandbox** and cannot establish a hard network-denial guarantee for arbitrary hostile HTML or WebRTC traffic. Never feed untrusted customer HTML to this code. Do not grant browser access to a NCA for arbitrary websites.
- This is behavioral and partial accessibility testing, not full screen-reader testing, WCAG 2.2 AA conformance, security scanning, or human expert QA. Dynamic defects outside these six categories are unmeasured.
- Passing all 12 intentionally small, public synthetic cases is a prerequisite learning signal only. The withheld professional exam, independently operated QA, tenant-level browser isolation, production AI Passport, Guardian Core, Approval Gateway, Audit Ledger, ProofGraph, authenticated Owner Kill Switch and actual customer rights remain outstanding.
- `legion/commercial_gate.py` is unchanged and continues to deny **all** external commercial platform requests, including if all synthetic tests pass.
- FREE_ONLY: public GitHub CI and local CPU/browser; no paid provider API, deployment, payout transfer, token spending or unattended customer access.

## Reproduction

```bash
python -m pip install -r browser-requirements.txt
python -m playwright install chromium
python -m unittest discover -s browser_tests -p 'test_*.py' -v
python -m legion.browser_qa_exam
```

This exam uses Playwright Python 1.64.1 and its corresponding installed Chromium. For a preinstalled local Chromium, `LEGION_BROWSER_EXECUTABLE=/absolute/path/to/chromium` may be set explicitly (not a customer URL). Keep local and GitHub CI results separate and record actual commit SHA/workflow run before claiming GitHub CI PASS.

**Next gate:** independently reviewed hidden browser tasks for complex workflows and keyboard navigation, signed authorization from HANTER, and server-side NCA worker isolation. Do not transform these into automatic commercial permits.

**Architecture preservation:** AI Passport, Enterprise Skills, Guardian Core, Approval Gateway, Audit Ledger, Zero Trust, Public/Private Boundary and CRYPTO IMPERIAL Ecosystem Boundary remain mandatory. VELION is the model platform; MAX is one mode. ORION has no authority to grant access.
