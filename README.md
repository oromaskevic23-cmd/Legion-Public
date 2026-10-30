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

The engineering branch includes a runnable Python **offline synthetic simulator**, a local agent registry, 25 professional role templates, an extensible online work taxonomy, mission expiry, 75% low-risk autonomy gating, independent test fixtures and persistent local stop controls. This is **not model fine-tuning**, paid employment, an operational marketplace or proof of professional competence. See the linked CI run once confirmed.

## Universal professional workforce — executable reference

- [Universal workforce architecture](docs/LEGION_UNIVERSAL_WORKFORCE_ARCHITECTURE.md) — internet service sectors, mission lifecycle, 75% bounded autonomy, independent QA milestones and emergency stop.
- [Brand and premium agent editions](docs/LEGION_BRAND_SYSTEM.md) — LEGION Professional, Enterprise and Sovereign; identical canonical IMPERIAL Core seal when used.
- [Python 25-role catalog](legion/catalog.py) · [Extensible sector taxonomy](legion/sectors.py) · [Offline simulator](legion/simulator.py) · [Mission lifecycle and stop controls](legion/lifecycle.py).
- [Unit test evidence](tests/test_legion_lifecycle.py) · [GitHub Actions](.github/workflows/legion-offline.yml).

Run locally with Python 3.11+ and **no external dependencies, credentials or network**:

    python3 -m unittest discover -s tests -p 'test_*.py' -v
    python3 -m legion.cli demo

The demo runs twelve deterministic cases, four synthetic workflow steps (three unattended and one reviewed), then activates the persistent global stop and proves further execution is blocked. Real-world effect execution and payments are absent.

**Agent expiry:** internal NCA have finite lifetimes; commercial SALE_OFFER records may have no calendar expiry but no actual customer entitlement or paid license is issued. Task-level access always needs finite permissions in production. **Every agent can be stopped within authorized deployment boundaries**, including through local CLI and code; self-hosted customer controls must be defined by contract.

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
