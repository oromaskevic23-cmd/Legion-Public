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

## Stronger-model evaluation

A second one-time comparative run uses **SmolLM2 1.7B Q4_K_M** with the same six held-out briefs and rubric. Its results must be read directly from the successful or failed [run 41147711647](https://github.com/oromaskevic23-cmd/Legion-Public/actions/runs/41147711647). Do not assume it passed or improved merely because the model has more parameters. The current repository is not allowed to publish a claimed result until that run completes with inspectable evidence.

## Prohibited inferences

No signed Owner customer authorization, live Guardian Core service, Approval Gateway or AI Passport issuance; no hired digital employee, revenue, model weight training, certified professional deliverables, real-world work, paid platform credentials or permission to spend. The HANTER federation, ORION synthesis, LEGION teams, VELION model target, 75% bounded autonomy, expiring missions and Owner Kill Switch remain architectural requirements for eventual supervised deployment.

**Commercial gate:** [legion/commercial_gate.py](../legion/commercial_gate.py) returns a denial irrespective of any exam score or caller-provided alleged permission. It deliberately cannot be overridden by prompts, agent roles, synthetic exam certificates or a public GitHub repository.

**Build software. Verify everything.**
