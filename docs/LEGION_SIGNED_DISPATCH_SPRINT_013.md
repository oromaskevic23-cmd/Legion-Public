# LEGION — Sprint 013: Ed25519-authenticated synthetic mission dispatch

**Founder and Final Architectural Decision Authority:** Alexander Nikolaevich Romaskevich (RomaskevicH)  
**Stage:** executable **local cryptographic protocol pilot**, not real production HANTER integration or signed Owner approval.  
**Strict trust boundary:** no real customer, payment, public website, commercial API, production AI Passport or external agent access.

## Why this gate exists

LEGION already demonstrates finite synthetic missions, a persisted local stop, a basic four-step 75% ceiling, limited HTML heuristics and a real-browser synthetic exam. None of those proves the issuing command is authentic. Sprint 013 tests one necessary cryptographic control before attempting to connect the private HANTER runtime to the federated orchestrator and an individual NCA.

## Canonical route — simulated only

Architect → HANTER (AI Command Center) → federated domain orchestrator → LEGION → NCA.

This implementation explicitly names **HANTER-DEMO-ONLY** and **ORCHESTRATOR-LEGION-DEMO**, not real connected services. The receiving **NCA-LEGION-WEBSITE-QA-001** uses the existing local SQLite lifecycle and the existing deterministic, read-only synthetic HTML inspector. A 12/12 browser pass does not grant rights to browse external sites. VELION remains the internal-model platform, with MAX as only a mode.

## Mechanism

1. The test process generates a temporary Ed25519 signing key; **no private key is committed**. The independent verification trust store contains a separately provisioned raw public key, indexed by a demo-only key ID.
2. Sign the domain-separated canonical JSON payload, including key ID in the signed bytes. Strict field allowlist prevents scope creep. The signed claims bind issuer, audience, federated route, NCA identity, exact mission, one local capability, SHA-256 document digest, unique 128-bit nonce, issuance and expiration.
3. A permit expires within **five minutes** maximum. Missing keys, forged signatures, wrong route/agent/mission, unknown capability, invalid clock, document substitution and all unrecognized fields fail closed.
4. A dedicated SQLite primary key for issuer and nonce permanently rejects replay **across local process restarts**; an accepted permit is recorded in the existing SHA-256 chained **local** audit. The original lifecycle gate checks mission lease, agent expiry, active sandbox state, and Owner Kill Switch. The existing lifecycle checks stop/expiry again before the synthetic step.
5. Step 4 still demands a **LOCAL DEMO manual-review boolean**, not a signed human approval. All external effects are forbidden by the unmodified lifecycle. The unmodified commercial gate denies every requested platform even with a valid demo signature.

## Evidence and limitations

- [Verifier and synthetic dispatcher](../legion/signed_demo_dispatch.py).
- [Ephemeral-key positive and negative-control suite](../signed_tests/test_signed_demo_dispatch.py).
- [Dedicated GitHub Actions evidence](../.github/workflows/legion-signed-dispatch.yml).
- Dependency pinned to public [cryptography 50.0.2](https://pypi.org/project/cryptography/50.0.2/).

Reproduce in a test-only environment:

    python -m pip install --requirement signed-requirements.txt
    python -m unittest discover -s signed_tests -p 'test_*.py' -v

GitHub Actions must be checked at the exact PR commit before claiming PASS. The suite includes correct signing, unknown/wrong key, signature alteration, signed scope rejection, strict TTL, document substitution, persistent replay, owner global/agent stop, mission expiry, the fourth-step review requirement, local audit tampering and immutable commercial denial.

**Not proven by this pilot:** actual HANTER private-key custody, HANTER service authorization, independent expert testing, authenticated Owner approval, AI Passport issuance, Guardian Core policy evaluation, Approval Gateway endorsement, externally anchored or tamper-resistant Audit Ledger, distributed in-flight Kill Switch, hardened executor isolation, real LLM professional performance, production operational availability, contractual rights or revenue. The local audit is hash-chained but **not independently anchored**. The nonce database is local SQLite, **not distributed high-availability replay protection**.

**Next production work:** align the signed protocol with an existing privately reviewed HANTER contract; provision keys via protected secret storage; bind real Owner approval and Guardian Core decisions; add shared transactional replay storage, certificate rotation/revocation, mutual service identity, distributed kill propagation, isolated worker execution and independently authored unseen expert QA. None may silently convert a synthetic permit into a commercial license.

**Preserved architecture:** Federated Multi-Orchestrator Architecture; AI Passport, Enterprise Skills, Guardian Core, Approval Gateway, Audit Ledger, Zero Trust, Public/Private Boundary and CRYPTO IMPERIAL Ecosystem Boundary. Every high-risk and commercial action requires distinct actual authorization.
