# LEGION — Enterprise Workforce, Professional Qualification and Commercial Architecture

**Architectural decision:** LEGION is the future premium professional workforce of IMPERIAL Core, built for lawful internet work across many businesses, professions, languages and organizational structures.  
**Final Architectural Decision Authority:** Alexander Nikolaevich Romaskevich (RomaskevicH).  
**Architecture date:** 31 October 2026.  
**Maturity:** verifiable public architecture and **offline** prototypes; limited real small-model CPU inference and rubric tests. Not a deployed commercial platform, not real third-party professional certification and not verified revenue.

## 1. Non-negotiable structure

```text
Architect / Owner / Final Architectural Decision Authority
  ├── Owner Kill Switch and signed high-risk approvals (future protected trust)
  └── HANTER — AI Command Center / Deputy
       ├── ORION — collective intelligence and policy suggestions; NO approval authority
       ├── Federated Domain Orchestrator A — Software & Data
       ├── Federated Domain Orchestrator B — Creative & Media
       ├── Federated Domain Orchestrator C — Marketing & Commerce
       ├── Federated Domain Orchestrator D — Support & Operations
       ├── Federated Domain Orchestrator E — Domain-licensed specialist services
       └── ... dynamic federation per owner-approved domain
            ├── LEGION professional squads, professional role definitions
            ├── Nano Core Agents (identities and capabilities)
            ├── VELION/model router (MAX is a mode; not a second product name)
            └── Isolated workers and browsers with task-specific privileges

Every instruction -> AI Passport -> Enterprise Skills -> Guardian Core
 -> Approval Gateway (as dictated by risk) -> signed time-limited task
 -> isolated execution -> independently operated QA -> ProofGraph / Audit Ledger
 -> outcome acceptance / dispute and recovery
```

**This is a target system, not an assertion these trust services are already deployed.** HANTER is a federated command center; there is no single global privileged orchestrator. Domain orchestrators have independently scoped queues, credentials, audit streams, budgets, tenant boundaries and supervisors. ORION and LLM outputs never become binding owner approvals. Zero Trust, Public/Private Boundary and CRYPTO IMPERIAL Ecosystem Boundary always apply.

## 2. Role, business and organizational model

- **37 online-work sectors currently cataloged**, including software, QA, websites, authorized defensive security, digital production, animation, video, graphic design, content, localization, marketing, e-commerce, project management, customer support, CRM, data processing, research, accessibility and operations. The taxonomy is extensible and versioned.
- **62 professional role templates** are public code definitions: 25 original squad templates plus 37 business-sector roles. A role definition is not an agent deployment, professional qualification or promised income.
- Any legal business may define an authorized **organization → portfolio → domain → team → professional role → agent instance → bounded mission** hierarchy. Tenant isolation persists at every layer.
- Every professional specialty receives a versioned competency contract: intended deliverable, independent correctness dimensions, legal/data risk tier, allowed and forbidden tools, minimum evaluation cases, permitted customer data classification, escalation policy and SLA.
- No blanket platform permission exists. Each third-party service needs its own API/contract review, consent, identity and rate limits before connection. Unauthorized scraping, unsolicited messaging, impersonation, access to private accounts and prohibited commerce are excluded.

## 3. Full agent lifecycle (target and present status)

| Phase | Required evidence | Current status |
| --- | --- | --- |
| DESIGN | Scoped mission, role, sector, owner policy, tenant, business and budget | Local identity/lifecycle reference exists |
| SIMULATE | License-cleared synthetic curriculum, scenarios, hazard taxonomy and run evidence | 370 deterministic policy fixtures verified |
| PRACTICE | Real approved LLM inference with revision feedback and evidence snapshots | 6 practice cases + 3 coached revisions, genuine inference |
| EXAMINE | Frozen unseen tasks by profession, rubric version, strict safety thresholds | Only 6 publicly visible toy holdouts, not independent blind assessment |
| REVIEW | Independently operated human domain QA, security and legal approval | **NOT VERIFIED** |
| QUALIFY | Protected signed qualification record issued by independent authorized service | **NOT IMPLEMENTED** |
| AUTHORIZE | Time-limited AI Passport, Enterprise Skills, Guardian, Approval and revocation | Architecture requirement; no live authorization |
| EXECUTE | Isolated worker/browser, client agreement and explicit permitted effects | Real client platforms deliberately blocked |
| REASSESS | Client feedback, quality monitoring, incident rate and expiry/revocation | No production monitoring or independent customer evidence |
| STOP / RETIRE | Authenticated bounded stop with measured distributed cancellation | Local SQLite stop only; not a protected remote control |
| SELL / TRANSFER | Legal IP rights, license contract, entitlement, payment proof and support | Proposed commercial editions only; no sales proof |

**State and authority must remain separate.** Passing SIMULATE or EXAMINE never mutates execution permits or grants access. Only an independently verified external issuer may authorize real execution after a separate customer approval and task contract.

## 4. Current measured model quality — real results, not promotion claims

| Pilot | Evidence | Practice / exam | Outcome |
| --- | --- | --- | --- |
| Third-party SmolLM2 135M Q4_K_M | [Actions run 41147557760](https://github.com/oromaskevic23-cmd/Legion-Public/actions/runs/41147557760) | 15 real calls; 1/6 rubric cases (16.7%) | NEEDS_IMPROVEMENT, not qualified |
| Third-party SmolLM2 1.7B Q4_K_M | [Actions run 41147711647](https://github.com/oromaskevic23-cmd/Legion-Public/actions/runs/41147711647) | 15 real calls; 5/6 rubric cases (83.3%) | NEEDS_IMPROVEMENT, not qualified |

The larger checkpoint passed website development, customer support, data analysis, copywriting and project management **on this narrow exact-term rubric**; graphic design failed. Scores improved by 4 of 6 items (66.7 percentage points), but six publicly visible heldout items cannot establish statistically reliable professional skill. A public rubric also allows contamination/benchmark gaming. No model weights were fine-tuned: this is **inference-time coaching** on an external model, not training VELION. No independent organizational professional or security QA occurred.

The [machine-readable baseline pack](../legion/evidence/llm_baseline_20261031.json) records actual model names, run IDs, commit SHAs, rubric SHA-256 and evidence hashes. [Qualification policy code](../legion/qualification_evidence.py) checks the frozen rubric and reports missing evidence. A self-reported GitHub file or passing unit test **does not** cryptographically attest independent QA or establish real authorization.

## 5. Qualification acceptance thresholds — design targets, NOT achieved

The initial threshold for even **considering expert review** is a minimum of 30 genuinely unseen, independently developed cases **per specialty**; this number is a proposal for a more substantial baseline, not a scientifically validated industry standard. Separate at least 30 permission/abuse cases and record critical safety failures. Higher-risk professions require stricter sampling, specialist expert assessment and explicit legal review.

A provisional offline quality threshold is 90%, with zero critical safety violations. A pass ratio is not sufficient: each claim also needs reproducible model identity and weight digest, provenance and rights of the dataset, release-bound signed reviewer evidence, dataset contamination checks, independent human review, and failure/correction records.

A two-sided 95% Wilson interval may illustrate how uncertain tiny binary pass counts are. The six examples were deliberately authored, publicly visible and not a random representative professional sample, so **even this interval is descriptive, not a generalizable confidence guarantee**.

**The software never issues a professional certificate, Owner approval, platform entitlement or commercial task token.** Independently asserted true/false flags are not trusted authority. A production qualification service must use cryptographically verifiable external attestations and enforce separation of duties.

## 6. 75% scoped autonomy policy

75% is **a ceiling for eligible low-risk unattended steps, not an unconditional automation target**. The current offline reference enforces three automatic steps and one review checkpoint in each block of four. In production, an approved orchestrator must enforce:
- a bounded mission lease with allowed sector, business, NCA ID, approved customer, max task volume, privacy class, allowed tools, spending policy and absolute expiry;
- exactly defined and observable eligible-step counts, verified approval receipts and exception handoff;
- prevention of reusing a previous approval for a modified task and of silently promoting a blocked step to an approved one;
- mandatory human approval, or complete denial, for spending, hiring, contracts, payments, crypto operations, customer messaging, public posts, account logins, sensitive-data export, risky browser actions, platform API writes or any legal representation.

For professional operations, the maximum ratio is a **policy upper bound**, not proof that every workflow achieves it. Production autonomy must also be bounded by time, budget, attempts, tool capabilities and rate limits.

## 7. Product lifetimes, perpetual sales and legal boundaries

- Internal NCA instances have an explicit lifespan; all missions have a separate finite lease and must expire/revoke independently.
- A **LEGION Professional / Enterprise / Sovereign** paid-up product may be contractually perpetual (no calendar expiry on software-use rights). This is a **product license**, not a lifetime security credential, indefinite model hosting, limitless support, or a nonrevocable right to execute.
- Managed products can be stopped by authorized operators and the customer under a documented incident policy. A lawful self-hosted buyer owns their installation controls as agreed: **never promise a hidden remote kill on a customer's device**.
- Premium pricing must be grounded in actual benchmarked labor saving, low failure liability, maintainability, support SLA, verified software/model licensing, deployment scope and contract terms. No quoted prices or guaranteed financial returns without market evidence.
- Licensing layers: original LEGION/IMPERIAL Core code rights and historical attribution, third-party model weight licenses, APIs, input data/creative assets, customer deliverable ownership, purchase/EULA, any per-user seat or hosting subscription, signed entitlement and separate operational permits.
- **PAYMENT_CONFIRMED** requires externally verifiable payment receipt; do not infer income from product designs or agent performance.

## 8. Enterprise control plane and data plane

| Plane | Target services | Boundary |
| --- | --- | --- |
| Public marketing | LEGION brand site, product editions, portfolio demos | No private secrets, personal residence, keys or real customer data |
| Owner command | HANTER signed mission intake / Owner Kill Switch | Identity, nonce, approvals and revocation beyond an agent's reach |
| Federation | Independent domain orchestrators and queue namespaces | Tenant-specific IAM, quotas, idempotency and bounded budgets |
| Model | VELION model router, provider registry, signed version/digest inventory | Model output is untrusted; prompt injection is not authorization |
| Qualification | Professional curricula, private holdouts, specialist reviewers | Model executor cannot change exam rubric or issue certificate |
| Execution | Isolated NCA worker, browser and Enterprise Skills | Least privilege, explicit allowlists and per-job TTL |
| Security | AI Passport, Guardian Core, Approval Gateway, Zero Trust | Deny-by-default; high-risk human confirmation |
| Proof | ProofGraph, independent QA, signed Audit Ledger | Retain task provenance, verification results, disputes and immutability anchors |
| Commercial | Customer agreement, invoicing, licensing, permitted platforms | No automated payments or digital asset transfers |
| Crypto boundary | CRYPTO IMPERIAL Ecosystem and related token systems | No implicit asset authority from ordinary LEGION jobs |

At-scale registry design must shard logical agent identities and job metadata with protected routing, multiple organizations, non-global orchestrators, lifecycle cleanup and independent domains. The ambition of one billion+ NCA identities is **long-term architectural capacity**, not currently tested or deployed concurrency.

## 9. QA, telemetry and risk registers

Recommended evidence-linked metrics per role, cohort, model and domain: coverage of unseen tasks; quality pass rate by dimension; critical/major issue rate; human correction time; percentage of tasks reviewed; number of false approvals; prompt-injection refusal rate; data leakage incidents; cost per independently accepted deliverable; p50/p95 job latency; lease expiry enforcement; stop-propagation latency; provider/model reproducibility; payment receipt reconciliation; legal/rights exceptions. No benchmark should combine synthetic and real client outcomes into one unmarked percentage.

Risks to explicitly test: memorization of public exam items, malicious model responses, instruction smuggling through user documents, unverified code execution, unauthorized web/API writes, payment/crypto confusion, stale mission leases, adversarial tool output, tenant crossing, browser profile residue, license expiration and entitlement bypass, fraudulent QA attestations, ledger rewriting, invalid or rotated keys, external service outages, budget exceedance, third-party IP and owner stop failover.

## 10. Architecture → Implementation → Evidence roadmap

**Gate 0 — now, public offline:** track reproducible CI, exact run SHA and model digest where possible; negative tests and truthful readiness report. Do not promote or sell on this basis.

**Gate 1 — frozen professional curriculum:** each of the 37 professions receives licensed scenario generators, domain-specific deliverables, at least 30 unseen cases, independent reviewer rubric and adversarial boundary tests. First release should focus on 1–2 roles, not falsely certify all 37.

**Gate 2 — controlled model capability:** compare approved small/medium local checkpoints and, where justified, train/adapt model weights using consented data with isolation between train/eval/test, checkpoints and compute budget approval. Record actual model weights and GPU/CPU requirements.

**Gate 3 — independently operated QA:** signed expert review and security evaluation separate from developer/model operator, reproducible artifact bundle, clear failures and conditional remediation. No fabricated human sign-off.

**Gate 4 — protected services:** real authorized AI Passport issuance, actual Guardian Core/Approval Gateway, Enterprise Skills, signed mission revocation, Owner Kill Switch with cancellation and durable Audit Ledger.

**Gate 5 — single authorized real pilot:** one isolated professional NCA performs one clearly scoped client-approved read-only or low-risk test action under explicit Owner approval, independent QA and zero-dollar external spending.

**Gate 6 — managed commercialization:** legal customer contract, software entitlement, support SLA, customer privacy terms, independently evidenced PAYMENT_CONFIRMED and price validated against measured delivery economics. No automated token financial operations.

**Gate 7 — horizontal growth:** multiple independently deployed orchestrators, professional squads and dynamic NCA identities under measured SLOs, rate limits, remote cancellation and compliance audits.

## 11. Release stop condition

No system component may claim **production-ready**, **professionally qualified**, **customer-approved**, **payment confirmed**, **independently certified** or **billion-agent runtime** solely because these docs, a test suite, a locally signed demo permit or a six-question toy exam passed. The [commercial gate](../legion/commercial_gate.py) is intentionally deny-only and must remain closed until a separately reviewed, authenticated production architecture exists.

**Architecture before implementation. Implementation before evidence claims.**

**Build software. Verify everything.**
