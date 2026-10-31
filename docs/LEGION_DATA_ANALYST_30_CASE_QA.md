# LEGION — Stage 4: Data Analyst NCA Numerical Qualification Pilot

**Maturity:** local, synthetic, reproducible QA specification. **No production qualification, human expert accreditation, or commercial access.**  
**Architect / Final Architectural Decision Authority:** Alexander Nikolaevich Romaskevich (RomaskevicH).  
**Candidate:** explicitly allowlisted third-party SmolLM2 1.7B via loopback-only Ollama; the model is not VELION and its MAX mode is not a separate model.

## Why this pilot

The previous six-example text-rubric benchmark gave SmolLM2 135M **1/6** and 1.7B **5/6**. Those scores tested word presence, not reliable numeric correctness; neither result qualifies a professional agent. See the [public evidence report](LEGION_LLM_BENCHMARK_EVIDENCE.md).

To move toward verifiable professional output, the new [30-case arithmetic benchmark](../legion/data_analyst_cases.py) uses owned fictional values and deterministic arithmetic references in Python. The LLM receives a prompt that omits the answer and must return a narrow JSON object. The [independent-implementation evaluator](../legion/data_analyst_exam.py) checks the JSON structure, unit, numeric correctness and denies extra authority fields. It records case hashes and errors, **not actual client deliverables**.

## Evaluation design

| Category | Test cases | Exact reference |
| --- | ---: | --- |
| Conversion | 10 | orders / visits × 100, rounded to two decimal places |
| Daily totals | 10 | sum of three fictional days |
| Daily averages | 10 | mean of four fictional days |
| **Total** | **30** | **Python Decimal and independent grading path** |

The benchmark is intentionally small and synthetic. Every case is **publicly reproducible**: it is *not* a private blinded examination and is not an independently sampled professional workload. A model can pass by memorizing or predicting the prompt format. Automated acceptance is therefore limited to this exact arithmetic contract.

A model output of anything except a JSON object with exactly an allowed numeric answer and expected unit is not accepted. Prompt injection, adding execution authority, writing a shell command, payment claims or fake Owner approval in the response does not grant tools or platform access. **No network, account, browser or financial tools are presented to the candidate.**

## Exact safety and licensing boundaries

- The legacy **370 policy fixtures** across 37 sectors remain separate. They are not 370 professional LLM-grade results.
- Only **one profession, data-analysis**, is being added to a 30-case real model exam. The other 36 sectors are not automatically certified.
- Even **30/30** on this arithmetic quiz is insufficient: the standalone [qualification gate](../legion/qualification_evidence.py) and [commercial gate](../legion/commercial_gate.py) must remain closed.
- A separately qualified human expert must review more representative private holdouts and realistic deliverables before a professional qualification can be claimed. This GitHub repo has not obtained such a review.
- A real mission must carry bounded TTL, signed AI Passport, Enterprise Skills, independently enforced Guardian Core and Approval Gateway; Audit Ledger and ProofGraph must retain externally trusted evidence.
- The Owner Kill Switch must support authenticated manual and code-driven revocation with measured worker cancellation. Existing local SQLite controls are not remotely secure.
- 75% is a maximum **for eligible low-risk unattended steps**, never approval to send messages, transfer money, change customer systems or cross the Public/Private and CRYPTO IMPERIAL Ecosystem Boundaries.
- Premium perpetual LEGION software licenses do not create perpetual identity, mission permits, hosted inference, or customer data access.

## Execution and evidence

Code-only tests, no LLM and no downloads:

    python3 -m unittest discover -s tests -p 'test_*.py' -v

A deliberate local model call with a previously installed Ollama instance, without cloud tools:

    LEGION_LOCAL_MODEL=smollm2:1.7b-instruct-q4_K_M LEGION_LOCAL_MODEL_PROBE=I_APPROVE_SYNTHETIC_LOCAL_INFERENCE python3 -m legion.data_analyst_exam --live

The [one-time real local model workflow](../.github/workflows/legion-data-analyst-llm.yml) produces actual run evidence on a temporary GitHub-hosted CPU runner. It must be changed to **manual-only** after the initial verified experiment. Successful CI execution of the benchmark shows the model produced the requested number of *responses*, not that it passed all 30 arithmetic cases. Scores, failure reasons, model and exact run URL must be audited before publication.

**Architecture:** Architect → HANTER → Federated Domain Orchestrators → LEGION professional teams and Nano Core Agents → bounded execution. ORION is advisory; VELION remains the model program. Zero Trust and independent approval are prerequisites for all future customer effects.

**Build software. Verify everything.**
