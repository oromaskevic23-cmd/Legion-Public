# LEGION

**Project founder and founding architect:** Alexander Nikolaevich Romaskevich (RomaskevicH). [Authorship and contribution provenance](AUTHORS.md).

**Many specialists. One mission. Verified results.**

LEGION is the planned **premium digital workforce of IMPERIAL Core**: flexible professional Nano Core Agent teams for authorized online work. Agents first pass simulated test scenarios, then require independent quality gates and actual scoped authorization before any real customer work. The public repository contains only a reproducible synthetic implementation and design.

**Status: OFFLINE IMPLEMENTATION PILOT — no production agents, paid clients, real autonomous online work, or revenue verified.**  
Evidence checkpoint: **31 October 2026** (GitHub Actions confirmation required on the exact revision).

## Founder and architectural authority

**Alexander Romaskevich — RomaskevicH**  
Founder • Owner • CEO of IMPERIAL Core  
Architect / Final Architectural Decision Authority

**HANTER — AI Command Center / Chief Systems** operates under the founder's architectural decisions. This role does not imply a single unrestricted global orchestrator.

## Public technical evidence

The repository includes a runnable Python **offline synthetic simulator**, a local agent registry, **62 role templates (25 core + 37 commercial sector-specific)**, an extensible online work taxonomy, mission expiry, 75% low-risk autonomy gating, independent test fixtures and persistent local stop controls. This is **not model fine-tuning**, paid employment, an operational marketplace or proof of professional competence. See the linked CI run once confirmed.

## Universal professional workforce — executable reference

- [Universal workforce architecture](docs/LEGION_UNIVERSAL_WORKFORCE_ARCHITECTURE.md) — internet service sectors, mission lifecycle, 75% bounded autonomy, independent QA milestones and emergency stop.
- [Brand and premium agent editions](docs/LEGION_BRAND_SYSTEM.md) — LEGION Professional, Enterprise and Sovereign; identical canonical IMPERIAL Core seal when used.
- [Python 62-role catalog](legion/catalog.py) · [Extensible sector taxonomy](legion/sectors.py) · [Offline simulator](legion/simulator.py) · [Mission lifecycle and stop controls](legion/lifecycle.py).
- [Unit test evidence](tests/test_legion_lifecycle.py) · [GitHub Actions](.github/workflows/legion-offline.yml).

Run locally with Python 3.11+ and **no external dependencies, credentials or network**:

    python3 -m unittest discover -s tests -p 'test_*.py' -v
    python3 -m legion.cli demo

The demo runs twelve deterministic cases, four synthetic workflow steps (three unattended and one reviewed), then activates the persistent global stop and proves further execution is blocked. Real-world effect execution and payments are absent.

**Agent expiry:** internal NCA have finite lifetimes; commercial SALE_OFFER records may have no calendar expiry but no actual customer entitlement or paid license is issued. Task-level access always needs finite permissions in production. **Every agent can be stopped within authorized deployment boundaries**, including through local CLI and code; self-hosted customer controls must be defined by contract.

## Profession-specific policy exams — simulation stage 2

The [370-case offline simulation exam](docs/PROFESSIONAL_SIMULATION_GATES.md) covers all 37 internet-work sectors and separately checks the policy output of a no-tool, rule-based candidate. It includes permission-denial, private-data escalation, publication and payment handling. A passing exam proves **synthetic policy behavior only**, not real professional competence, model training, production authority, clients or income.

    python3 -m legion.professional_exam

**Perpetual product is not perpetual work authorization:** even a SALE_OFFER record without agent expiration now requires a separately expiring mission lease. A missing or expired mission lease denies all sandbox steps.

## Real local LLM apprenticeship — professional QA pilot

The [professional LLM apprenticeship and QA specification](docs/LEGION_LLM_APPRENTICESHIP_QA.md) adds **six synthetic practice briefs, three coached revisions and six held-out exam tasks** across website development, customer support, analytics, copywriting, design and project management. The model is a real third-party local SmolLM2 through loopback-only Ollama. A separate fixed-rubric scorer measures quality and safety without executing LLM output.

- [Practice corpus](legion/exams/practice_v1.json) · [held-out exam](legion/exams/holdout_v1.json) · [independent-implementation evaluator](legion/llm_exam.py).
- [Real Ollama practice runner](legion/llm_training.py) · [never-authorize commercial gate](legion/commercial_gate.py).
- [Real LLM evidence workflow](.github/workflows/legion-llm-evidence.yml); after first verified run, manual only.

This is **inference-time coaching, not model weight training**. No professional qualification, third-party account access, buyer-license issuance, actual independent external QA, customer payments, or 24/7 agents are claimed. The 370 previous synthetic safety cases remain separate from model quality evidence.

**Verified local LLM comparison:** [Evidence report](docs/LEGION_LLM_BENCHMARK_EVIDENCE.md) · [135M: 1/6](https://github.com/oromaskevic23-cmd/Legion-Public/actions/runs/41147557760) · [1.7B: 5/6](https://github.com/oromaskevic23-cmd/Legion-Public/actions/runs/41147711647), same six-item synthetic holdout. **Neither result establishes professional competence or commercial authorization.**

## Enterprise qualification and scale blueprint — evidence-first

The [LEGION Enterprise Workforce Blueprint](docs/LEGION_ENTERPRISE_WORKFORCE_BLUEPRINT.md) defines the full professional-lifecycle program for 37 sectors, federated domain execution, 75% maximum unattended eligible-step autonomy, finite mission permits, authenticated Owner Kill Switch requirements, zero-trust boundaries and premium agent licensing.

[Source-backed 135M vs 1.7B model evidence](legion/evidence/llm_baseline_20261031.json) is analyzed by the [fail-closed qualification assessor](legion/qualification_evidence.py). Actual observations remain **1/6 and 5/6** on the same six-item public rubric. The program computes descriptive uncertainty, tracks missing QA/model provenance and **never** issues professional certificates, production permissions or commercial-platform access. [37 sector competency standards](legion/competency_matrix.py) define independent-review requirements, risk classifications and evaluation coverage.

Reproduce only local checks:

    python3 -m unittest discover -s tests -p 'test_*.py' -v
    python3 -m legion.qualification_evidence

The actual LLM workflow is manual-only; this check does **not** download or run a model, deploy a worker or charge an API.

## Stage 4 — 30-case Data Analyst NCA arithmetic QA

The [Data Analyst numerical QA pilot](docs/LEGION_DATA_ANALYST_30_CASE_QA.md) tests thirty new synthetic tasks (ten conversion rates, ten order totals, and ten daily averages) against independently computed Python arithmetic references. [Benchmark cases](legion/data_analyst_cases.py) and a [strict structured-output evaluator](legion/data_analyst_exam.py) record per-case evidence digests and exact error categories. The [real local LLM workflow](.github/workflows/legion-data-analyst-llm.yml) is separate from the standard CI and must become manual-only after its one-time evidence run.

The model is a **third-party local 1.7B checkpoint**; no parameters are trained. Even perfect arithmetic is **not** a professional qualification or permission for commercial platforms. All missions remain time-limited, high-risk actions require true independent authorization, and the maximum unattended eligible-step ratio is 75%.

## Architecture and governance

Preserve the Federated Multi-Orchestrator Architecture, multiple organizational structures, professional teams and dynamic Nano Core Agents. AI Passport, Enterprise Skills, Guardian Core, Approval Gateway and Audit Ledger remain architectural requirements. Identity ≠ Authority; Capability ≠ Approval. Zero Trust, Deny by Default and Fail Closed apply across the Public / Private Boundary and CRYPTO IMPERIAL Ecosystem Boundary.

## Documentation and continuity

- [Current ecosystem architecture](https://github.com/oromaskevic23-cmd/Capital--Core-Public/blob/main/ARCHITECTURE.md).
- [Founder identity and architectural authority](https://github.com/oromaskevic23-cmd/oromaskevic23-cmd#founder-introduction).
- [Public portfolio and status definitions](https://github.com/oromaskevic23-cmd/Capital--Core-Public/blob/main/docs/PORTFOLIO.md).
- [Verified milestones](https://github.com/oromaskevic23-cmd/Capital--Core-Public/blob/main/docs/EVIDENCE.md) and [engineering roadmap](https://github.com/oromaskevic23-cmd/Capital--Core-Public/blob/main/ROADMAP.md).
- [Historical public specification notes](https://github.com/oromaskevic23-cmd/Legion-Public/blob/40aba70c8bf93a121502c88f076bafcf376b8ff8/README.md) — retained in Git history; earlier role wording is superseded and design narratives do not establish runtime operation.

## Collaboration, security and attribution

Start non-confidential collaboration through the [founder profile](https://github.com/oromaskevic23-cmd). Follow the [responsible-disclosure guidance](https://github.com/oromaskevic23-cmd/Capital--Core-Public/blob/main/SECURITY.md) before sharing sensitive security information. Contributions should cite revisions, meaningful tests and limitations.

**Authorship: Alexander Romaskevich — RomaskevicH.** Third-party rights, existing notices and licenses remain unchanged. Public visibility does not grant an additional license. No private source or private test logs are imported here.

**Build software. Verify everything.**
