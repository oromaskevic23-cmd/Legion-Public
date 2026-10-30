# LEGION — Universal Digital Workforce Architecture

**Founder and Final Architectural Decision Authority:** Alexander Nikolaevich Romaskevich (RomaskevicH).
**Status:** Future Enterprise architecture and executable offline synthetic simulator — NOT deployed business agents, professional model training, a marketplace, or verified revenue.

## Mission and operating model

LEGION is the professional digital workforce of IMPERIAL Core, intended to support many authorized forms of internet work. Architecture: **Architect → HANTER → federated domain orchestrators → LEGION professional teams → Nano Core Agents → isolated execution**. ORION provides collective intelligence but no execution authority. VELION is the AI model platform (MAX is a mode only). The original 25 professions remain seed templates across five squads; professional teams, sectors, missions, organizational structures and number of NCA must be extensible.

The work taxonomy is implemented in legion/sectors.py and includes software, websites, quality assurance, permitted defensive security, design, video/animation, audio, content, localization, marketing, ethical SEO, customer service, CRM, e-commerce, documentation, research, analytics, operations, education, recruiting administration, digital products, project management and more. Inclusion is NOT evidence of paying opportunities, platform authorization, demand, legality or platform API availability. All work must respect contracts, client consent, applicable law, account terms, anti-spam rules and personal data boundaries.

## Agent lifecycle

1. DESIGN: select mission, profession, sector, tenant and least-privilege skills.
2. SIMULATE: exercise synthetic edge cases and failures without customer accounts or side effects.
3. EVALUATE: reproduce metrics, run adversarial tests and independent QA.
4. QUALIFY: independently confirm domain competence, safety and requirements.
5. AUTHORIZE: require actual signed AI Passport, Enterprise Skills, Guardian Core and Approval Gateway.
6. EXECUTE: limited-time mission, isolated browser/worker and approved external effects only.
7. REASSESS: audit quality, incidents, kill state, revoked access and customer feedback.
8. STOP or RETIRE: halt via Architect, authorized operator, code or expiry.

The current Python pilot implements **DESIGNED → SIMULATED → SANDBOX_ACTIVE** and persistent STOP. Its 12 synthetic fixtures per safe test skill are **not LLM training, professional qualification, or evidence of real internet earnings**.

## Missions, expiry and 75% autonomy

- Internal NCA must have finite agent lifecycle expiry.
- For-sale SKU offers can have a **perpetual license entitlement** subject to an actual executed customer contract; the reference uses SALE_OFFER with no agent calendar expiry. Such products are NOT automatically sold or activated for customers.
- **Every real mission, AI Passport, service token and delegated permission expires independently**, including for a customer with a perpetual product license. Perpetual does not mean unrestricted, unrevocable or free model hosting.
- **75%** means at most **3 unattended, low-risk synthetic steps per four-step control window**, with step four requiring a separate human-review checkpoint. Actual share is measured and can be lower. On incomplete windows it is not necessarily 75%.
- All high-risk actions require real Approval Gateway authorization or are prohibited: spending, posting, sending messages, financial/crypto transactions, account access, signing contracts, private data export, scraping not authorized by platforms, outreach spam and anything outside the mission.
- Manual-review flags in the public demo are NOT cryptographically authenticated owner signatures; production approval requires a distinct trusted service.

## Manual and programmatic emergency stop

The offline engine stores stop controls in SQLite and checks them before every local task. It supports **global, squad, agent and mission** scopes; a global stop blocks all current and new test agents and survives application restart.

Manual local command example:

    python3 -m legion.cli stop --db /path/to/local-legion.sqlite --scope global --subject '*' --reason 'Owner emergency halt'

Code-level invocation:

    system.stop(scope="agent", subject="NCA-001", reason="Owner halt")

No remote administration is implemented. Before any server deployment, require signed commands, identity authentication, scope authorization, replay prevention, external audit anchoring, propagation SLO, in-flight cancellation and fail-closed behavior. A vendor cannot promise to remotely terminate independently owned customer deployments absent a lawful contract and technical control.

## Commercial product positioning

Proposed premium editions: **LEGION Professional** (profession-specific), **LEGION Enterprise** (multi-team licensed workflows) and **LEGION Sovereign** (customer-controlled infrastructure and separately negotiated legal rights). Premium pricing must be grounded in verifiable capability, independent QA, production support, security and actual customer terms — not arbitrary price claims or promises of income.

Perpetual licensing must explicitly state rights, third-party/model licenses, transfer and redistribution limits, version coverage, support/updates, hosting fees, security stop/revocation grounds, customer rights and ownership. No certificate, signing key, customer authorization or PAYMENT_CONFIRMED is issued by this public repository. Decorative brand seals do not create commercial rights.

## Mandatory governance and scale boundaries

AI Passport, Enterprise Skills, Guardian Core, Approval Gateway, Audit Ledger, ProofGraph, IntentLock, Owner Kill Switch, Zero Trust, Public/Private Boundary and CRYPTO IMPERIAL Ecosystem Boundary remain architectural requirements. The public pilot does not implement trusted live equivalents.

Real workflows require separately authenticated and isolated NCA runtime, independent QA, repeatable benchmarks, safe model inference, durable idempotent assignments and external proof of payment and legal rights. The future 1,000,000,000+ identity goal describes a scalable logical registry **not a current working fleet**.

**Build software. Verify everything.**
