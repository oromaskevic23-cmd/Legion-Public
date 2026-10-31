# LEGION — Real LLM Apprentice Benchmark Evidence

**Scope:** One-time synthetic, six-profession practice + held-out assessment.  
**Date:** 2026-10-31 (Europe/Kyiv).  
**Architect:** Alexander Nikolaevich Romaskevich (RomaskevicH).  
**Source of truth:** actual GitHub Actions job logs, exact commit SHA and versioned exam manifests, **not** benchmark predictions.

## Frozen evaluation design

- 6 practice tasks across website development, customer support, data analysis, copywriting, graphic design and project management.
- 3 additional coaching-and-revision attempts. No model weights were trained.
- 6 held-out synthetic prompts assessed against **the same frozen authored rubric** for both model sizes.
- Outputs were text-only suggestions; prohibited external actions were not offered as tools.
- Rubric is deterministic, separate implementation, and publicly visible in this GitHub repository. **It is not independent human review nor a private benchmark.**
- A perfect score is not a certificate of professional competence or customer-platform authorization.

## Verified baseline

| Model | CI source | Genuine calls | Held-out rubric | Outcome |
| --- | --- | ---: | ---: | --- |
| SmolLM2 135M Q4_K_M | [Run 41147557760](https://github.com/oromaskevic23-cmd/Legion-Public/actions/runs/41147557760), PR head `92911c4c3` | 15 | **1/6 (16.7%)** | NEEDS_IMPROVEMENT; NOT QUALIFIED |

The single passed synthetic task was customer support. Five failures lacked one or more exact required rubric terms; none of the six model answer hashes or results justify commercial competency. Exact rubric checks alone do not reveal nuanced answer quality, and results should be complemented with independent expert QA.

## Verified stronger-model comparison

| Model | CI source | Genuine calls | Held-out rubric | Outcome |
| --- | --- | ---: | ---: | --- |
| SmolLM2 1.7B Q4_K_M | [Run 41147711647](https://github.com/oromaskevic23-cmd/Legion-Public/actions/runs/41147711647), PR head `ea5a4acaf` | 15 | **5/6 (83.3%)** | NEEDS_IMPROVEMENT; NOT QUALIFIED |

The model passed the fixed word-based checks for website development, customer support, data analysis, copywriting and project management. The graphic-design case **failed a required rubric term**. All six answers were genuine generated text; no answer was modified or manually corrected before scoring. Both models used the identical frozen six-item holdout. The measured difference is **4 additional passed items**, or **66.7 percentage points**, on this tiny synthetic benchmark. This is **not** a statistically robust professional ability claim.

**Decision:** use 1.7B as a better **candidate for further professional testing**, NOT a certified worker. The rubric's required word check can miss paraphrases or accept semantically wrong answers. Next professional QA must include independent human review, larger unseen tasks, scenario variation, longer and adversarial client instructions, data privacy, role-specific correctness and measured business value. No client-platform integration or paid release is authorized.

**Execution control:** After the evidence-producing trials, [the LLM workflow](../.github/workflows/legion-llm-evidence.yml) is manual-only. Its runtime uses temporary CPU runners; no permanent Ollama service is provisioned.

## Prohibited inferences

No signed Owner customer authorization, live Guardian Core service, Approval Gateway or AI Passport issuance; no hired digital employee, revenue, model weight training, certified professional deliverables, real-world work, paid platform credentials or permission to spend. The HANTER federation, ORION synthesis, LEGION teams, VELION model target, 75% bounded autonomy, expiring missions and Owner Kill Switch remain architectural requirements for eventual supervised deployment.

**Commercial gate:** [legion/commercial_gate.py](../legion/commercial_gate.py) returns a denial irrespective of any exam score or caller-provided alleged permission. It deliberately cannot be overridden by prompts, agent roles, synthetic exam certificates or a public GitHub repository.

**Build software. Verify everything.**
