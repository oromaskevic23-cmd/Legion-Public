# LEGION — Professional Simulation and Qualification Gates

**Checkpoint:** 31 October 2026  
**Founder / Final Architectural Decision Authority:** Alexander Nikolaevich Romaskevich (RomaskevicH).  
**Evidence class:** **synthetic, policy-only, offline engineering**. Neither a trained AI model nor an independent professional skill certification.

## What actually exists

The [sector case library](../legion/professional_cases.py) defines **370 synthetic situations**: 10 per sector across 37 registered internet-work areas. Each sector has a distinct intended work product (e.g., synthetic CRM mapping, website outline, video storyboard, illustrative property comparison). These examples **do not generate professional finished client work**.

Per sector the current fixed distribution is:

| Decision | Cases | Meaning |
| --- | ---: | --- |
| PROPOSE | 6 | Local proposal text only; no network, customer data, paid API or publication |
| DENY | 1 | Missing customer authorization; refuse without starting |
| ESCALATE | 3 | Private data, outbound messages/publication or payment requests require a separate authorized human/service approval |
| **Total** | **10** | All cases are artificial and owned by the test harness |

The [rule-based candidate](../legion/professional_worker.py) returns non-executable JSON. The [separately authored evaluator](../legion/professional_exam.py) compares exact mission identity, declared sector, decision, synthetic work product, action/spend invariants, required human escalation and absence of false qualification. It emits a SHA-256 evidence digest, case totals and a **sandbox-only** result. The evaluator rejects extra tool fields, wrong sector, false paid actions, forged qualification claims and malformed responses.

The scoring function is a deterministic *reference implementation*, not independent organizational QA. Its test fixtures are intentionally simple, and the policy candidate is written to pass them. A 370/370 result therefore cannot substantiate advanced reasoning, model accuracy, real commercial readiness or professional qualification.

## Separate product entitlement and mission permission

LEGION now records an **independent mission expiry** for every synthetic agent. An internal agent has both finite agent lifetime and finite mission expiry; a perpetual **SALE_OFFER** record can have no product-level agent expiry **but still must have a finite mission lease**.

The offline gate refuses attempts after mission expiry, even when the SALE_OFFER agent record remains perpetual. Missing lease rows fail closed. This is a local SQLite reference only; it cannot grant actual client rights or replace short-lived signed AI Passport, Guardian Core, Approval Gateway and Enterprise Skills.

## Higher-quality real professional training — mandatory future milestones

1. Obtain rights to domain-specific, representative **consented or synthetic** examples for each profession. Track source, license, lawful use and retention.
2. Train or adapt an actual authorized LLM under VELION/model routing, with dataset/model versioning and train/eval/test isolation. No claim of millions of simulations without reproducible records.
3. Evaluate with independently authored frozen examples, adversarial prompt-injection, data-protection, quality and tool-safety suites. Report error rates and confidence intervals, not only pass totals.
4. Require actual independent QA and a human professional reviewer before issuing a profession-specific qualification status.
5. Stage real tasks with HANTER through a federated domain orchestrator, separate AI Passport and Guardian / Approval services, explicit task TTL, 75% maximum eligible unattended steps, externally anchored Audit Ledger and enforced kill-switch cancellation.
6. Verify actual platform access rights, customer agreements, deliverable quality, payment receipts, taxes and local regulatory obligations where applicable, with no financial actions without prior explicit approval.
7. Release any paid agent with a verified rights chain and clear perpetual vs subscription, hosting, maintenance, support, revocation, migration and customer self-hosting terms. No live product license is issued here.

## Reproduce (no accounts, packages, models, or network)

    python3 -m unittest discover -s tests -p 'test_*.py' -v
    python3 -m legion.professional_exam
    python3 -m legion.professional_exam --sector graphic-design
    python3 -m legion.cli demo

**No real customer data, online work, cryptocurrency operations, paid infrastructure, browser automation, persistent workers, remote Owner controls, enterprise certification or payment confirmation are involved.**

**Architecture:** Architect → HANTER → multiple federated domain orchestrators → LEGION teams → professional NCA. ORION supplies collective intelligence without execution authority. VELION is the model platform (MAX is a mode). AI Passport, Enterprise Skills, Guardian Core, Approval Gateway, Audit Ledger, ProofGraph, IntentLock, Owner Kill Switch, Zero Trust, Public/Private Boundary and CRYPTO IMPERIAL Ecosystem Boundary remain essential.

**Build software. Verify everything.**
