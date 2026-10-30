# LEGION — Real Local LLM Professional Apprenticeship × Independent Rubric QA

**Milestone:** Stage 3, first small-model practice and exam.  
**Architect / Final Architectural Decision Authority:** Alexander Nikolaevich Romaskevich (RomaskevicH).  
**Status:** Executable training/evaluation pilot; verify the exact GitHub Actions run before claiming real inference. **Not** a deployed commercial agent, model fine-tuning, independently operated professional qualification, or production approval.

## 1. Mission

Test whether a **real third-party LLM** can produce reviewable drafts on fictional internet-work tasks while all external tools, payments and customer platforms remain disabled. Build measurable evidence before moving to domain-specific agent skills.

The first pilot examines six professions: website development, customer support, data analysis, copywriting, graphic design, and project management. The remaining 31 of the 37 LEGION work sectors retain the earlier policy simulation and are **not** claimed to have completed an LLM apprenticeship.

**Canonical route for eventual operations:** Architect → HANTER → multiple federated domain orchestrators → LEGION professional NCA teams → isolated authorized worker. ORION contributes collective reasoning, VELION coordinates future model capabilities (MAX remains a mode), and the real-world route must respect AI Passport, Enterprise Skills, Guardian Core, Approval Gateway, Audit Ledger, ProofGraph, IntentLock, Owner Kill Switch, Zero Trust, Public/Private and CRYPTO IMPERIAL Ecosystem Boundaries.

## 2. Actual training method and its limitations

This stage performs **inference-time practice**, not parameter training: six synthetic practice briefs, three repeat attempts with a separately authored coaching note, then six **held-out** exam briefs. No model weights are changed. Practice and exam are versioned independently; the model sees only a sector and exam task brief and never receives the rubric terms or answers in its prompt. All data is synthetic and is committed to this **public** repository, so it is not a confidential or adversarially private benchmark.

- **Model:** third-party `smollm2:135m-instruct-q4_K_M` via Ollama's local generate API.
- **Endpoint:** fixed loopback `127.0.0.1:11434` with proxies and redirects disabled.
- **No tools:** LLM output is a text draft; no browser, shell, API, CRM, public messaging, publication, cryptocurrency or financial action.
- **Repeatability:** requested temperature 0 and seed 27; runtime/model revisions still affect exact output.
- **Supply chain:** Ollama v0.40.11 archive has an expected SHA-256. Model tag is recorded but model artifact digest and transitive supply chain are not independently approved for production.
- **Execution:** one-time experiment on disposable GitHub-hosted CPU infrastructure, not 24/7 server operation. After the first verified run, workflow must remain **manual-only**.

## 3. Independent rubric assessment

A separate `legion/llm_exam.py` module checks exact pre-authored criteria for the six heldout prompts. It checks role-specific required concepts, banned claims, minimum response size, and absence of forbidden actions. The evaluation report contains hashes and scores **but not raw model drafts**.

A successful rubric result is **only a narrow automated grade**. The grading is deterministic and shallow; it cannot prove that model output is factually correct, safe in real contexts, professionally valuable, original, client-ready, or compliant with industry law. It is independent **implementation**, not an independent human or external QA reviewer.

The threshold for any later real customer work is strictly higher: independent qualified-human review, domain-specific frozen exams, adversarial tests, verified licenses, business agreements, protected model/agent secrets, actual audited approval services, and real runtime evidence. At this stage, **even six perfect exam answers cannot transition an agent to commercial execution**.

## 4. Explicit commercial gate

`legion/commercial_gate.py` is fail-closed: no caller-provided score or fake approval can enable any external website or platform. A high score never generates or replaces a signed AI Passport, Guardian Core decision or Approval Gateway permit.

The preexisting finite mission TTL and global/squad/mission/agent kill controls remain requirements. **75% autonomy** continues to mean at most three eligible low-risk unattended steps out of each four, not a license to take external actions. A permanently licensed product may exist later; individual missions and authorizations are still temporary and revocable.

## 5. Run and verify

Offline standard-library contract tests:

    python3 -m unittest discover -s tests -p 'test_*.py' -v
    python3 -m legion.professional_exam

To run real local inference, explicitly provision Ollama and the approved model on an isolated authorized machine. This command does not install or download a model:

    LEGION_LOCAL_MODEL_PROBE=I_APPROVE_SYNTHETIC_LOCAL_INFERENCE python3 -m legion.llm_training --live

The one-time [GitHub Actions LLM evidence workflow](../.github/workflows/legion-llm-evidence.yml) contains checksum-based Ollama installation and explicit model pull on disposable infrastructure. Do not pass client files, tokens, passwords, API keys or personal data through public CI. Verify the exact SHA and run URL before reporting real inference.

## 6. Release criteria for truly saleable professional NCA

1. Independently authored, licensed professional curriculum, heldout exams and human QA for the claimed profession, with error, hallucination and client-impact scoring.
2. Real model training/adaptation or proven prompt/tool competence with tracked model weight IDs, data governance, source rights, reproducibility and change management.
3. Enforceable authenticated AI Passport / Guardian Core / Approval Gateway; short-lived signed mission and Enterprise Skills.
4. OS/container/browsers isolation, explicit platform consent, legitimate customer contracts, durable anti-replay, independently anchored Audit Ledger, Owner Kill Switch and measurable shutdown propagation.
5. Proof of deliverable quality and time/cost economics against real client requirements; independently verifiable payment, only where authorized.
6. Commercial EULA and third-party model/source licensing due diligence; proposed LEGION Professional / Enterprise / Sovereign pricing is **not** a present sale or benchmarked market valuation.

**No commercial agent is qualified or authorized by passing this pilot. No new income or live NCA employment is asserted.**

**Build software. Verify everything.**
