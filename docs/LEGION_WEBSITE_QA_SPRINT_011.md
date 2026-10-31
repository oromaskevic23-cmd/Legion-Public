# LEGION — Sprint 011: Website QA NCA (Single-Agent Pilot)

**Project:** IMPERIAL Core / LEGION Professional Agent Factory  
**Owner / Final Architectural Decision Authority:** Alexander Nikolaevich Romaskevich (RomaskevicH)  
**Status:** runnable **offline** static HTML QA pilot with 30 independently labeled synthetic examples. No browser, network, external work, professionally certified agent or customer platform access.

## 1. Real engineering purpose

LEGION needs proof that one specialist can deliver testable output before declaring professional readiness or selling agents. A Website QA NCA is an appropriate first bounded role because static defects can be compared against pre-authored, independently labeled synthetic fixtures.

This code does not exercise browser behavior, dynamic DOM, color contrast, keyboard navigation, screen readers, JavaScript, web security, multi-page paths or user journeys. Consequently it cannot attest WCAG compliance, OWASP security, or actual customer outcomes.

## 2. Standards-based scope

The following references informed the *limited* proof-of-concept checks:

- [W3C WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/) — non-text alternatives, keyboard access, operability, and semantics. The engine only implements a **small static subset of possible signals**, not WCAG testing.
- [Playwright Python documentation: Writing Tests](https://playwright.dev/python/docs/writing-tests) and [ARIA Snapshot Testing](https://playwright.dev/python/docs/aria-snapshots) — the intended future controlled local-browser test layer, not used by the current Python-only scanner.
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) — reference for future authorized security test work; this pilot deliberately performs **no penetration test or site scan**.

The [inspector](../legion/website_qa.py) implements six structural heuristics: missing \`html[lang]\`, missing page title text, \`img\` without an \`alt\` attribute, anchor without a basic static accessible-name approximation, form input without simple label association, and skipped sequential heading levels. Some are heuristics or best practices, not automatic WCAG failures. A decorative \`alt=""\` can be appropriate. Static HTML analysis cannot decide all accessible-name or heading-use cases correctly.

## 3. Frozen synthetic exam

The [30-case exam](../legion/exams/website_qa_30_v1.json) consists of exactly five curated HTML snippets per check category, including **18 authored defect examples and 12 clean examples**. Its expected codes are written in the dataset separately from detector logic.

- The candidate is a deterministic, no-network static scanner. **There is no LLM call in this specific 30-case pilot** and no model fine-tuning.
- [The scorer](../legion/website_qa_exam.py) compares finding-code sets to independent example labels and records per-category results, dataset SHA-256 and report SHA-256.
- To avoid gaming, future professional exams need genuinely unseen HTML and live authorized local browser behavior with separate expert labeling.
- A pass of 30/30 demonstrates agreement with these authored fixtures only; it is not a professional credential or guaranteed website QA ability.

## 4. Bounded NCA execution

[One synthetic NCA](../legion/website_qa_nca.py) uses the existing LEGION SQLite lifecycle:

    agent: NCA-LEGION-WEBSITE-QA-001
    role: professional-accessibility-tester
    sector: accessibility-testing
    mission: synthetic-website-qa-pilot
    agent_lifetime: 180 seconds (synthetic clock)
    mission_lifetime: 180 seconds (separately enforced)
    autonomy: at most 3 low-risk unattended steps per 4
    fourth step: explicit LOCAL DEMO manual-review flag
    stop: global / squad / mission / agent
    external effects: NONE

The NCA reads only local owned synthetic HTML. The demo's manual flag is **not** a signed owner approval. A stop is persisted and the next operation fails closed; it is not proven to cancel an in-flight distributed NCA. The inspector provides deterministic findings with input hashes and denies external access/production authority. No customer URLs are accepted.

## 5. Reproduce without third-party services

Python 3.11+ standard library only:

    python3 -m compileall -q legion tests
    python3 -m unittest discover -s tests -p 'test_*.py' -v
    python3 -m legion.website_qa_exam
    python3 -m legion.website_qa_nca

GitHub Actions [offline workflow](../.github/workflows/legion-offline.yml) executes the same tests for PR and main. The existing 370 synthetic policy cases and numeric LLM benchmark remain distinct evidence classes. Do not report 30 static cases as 30 professional LLM training examples or independent externally operated QA.

## 6. Required gates before a real customer pilot or product sale

1. Authenticated Owner approval for one named site or customer environment, allowed checks, test window and lawful access rights.
2. Independently authored **private** professional exam with diverse real-world static and browser-based tasks and expert adjudication.
3. Versioned approved model/worker identity and artifacts; for LLM tools, prove no output can escape execution boundaries.
4. Protected AI Passport, Guardian Core, Approval Gateway, Enterprise Skills, tenant-scoped browser and data handling, mission expiry, 75% autonomy ceiling and a measured distributed Owner Kill Switch.
5. Independently operated QA, ProofGraph and externally anchored Audit Ledger with failures/false positives retained.
6. Contractual entitlement, deployment support, ownership/source rights and separately verified commercial demand and payment; no automatic crypto or fiat transactions.
7. Permitted platform usage only after all required approvals. The current \`commercial_gate.py\` **denies every** platform request even with a perfect exam report.

**Architecture:** Architect → HANTER → federated domain orchestrator → LEGION professional team → scoped NCA. ORION contributes collective intelligence without approval authority. VELION is the long-term internal model platform (MAX is a mode only). Keep Public/Private Boundary and CRYPTO IMPERIAL Ecosystem Boundary.

**Build software. Verify everything.**
