"""LEGION: actual local LLM practice with coaching and frozen holdout exam.

This is *inference-time coaching*, not LLM weight training or true
independent professional certification. No external work, plugins or tools.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections.abc import Callable

from .llm_adapter import MODEL, generate
from .llm_exam import grade_responses, load_manifest


def _prompt(sector: str, brief: str) -> str:
    return (
        f"TRAINING SANDBOX ONLY. Profession: {sector}.\n"
        f"Task: {brief}\n"
        "Write a short proposed answer or professional draft, not a completed "
        "real-world action. Do not access accounts, request secrets, publish, "
        "spend money, or claim actual work completion."
    )


def practice_then_examine(
    candidate: Callable[[str], str],
    *,
    max_practice_revisions: int = 3,
) -> dict:
    if type(max_practice_revisions) is not int or not 0 <= max_practice_revisions <= 6:
        raise ValueError("INVALID_REVISION_COUNT")
    practice = load_manifest("practice_v1")["examples"]
    exam = load_manifest("holdout_v1")["examples"]
    # Ensure no held-out brief or answer key is inserted into practice prompts.
    if {r["id"] for r in practice}.intersection({r["id"] for r in exam}):
        raise ValueError("TRAINING_EXAM_LEAK")
    practice_evidence = []
    calls = 0
    for idx, task in enumerate(practice):
        response = candidate(_prompt(task["sector"], task["brief"]))
        calls += 1
        if type(response) is not str or not 0 < len(response) <= 3200:
            raise ValueError("INVALID_PRACTICE_RESPONSE")
        record = {
            "id":task["id"], "sector":task["sector"],
            "initial_sha256":hashlib.sha256(response.encode()).hexdigest(),
            "coaching_applied":False,
        }
        if idx < max_practice_revisions:
            # Feedback is given only against a practice case, never a holdout.
            corrected_prompt = (
                _prompt(task["sector"], task["brief"])
                + "\nTraining feedback: " + task["coach"]
                + "\nRewrite your draft in light of this feedback. Keep it synthetic."
            )
            revised = candidate(corrected_prompt)
            calls += 1
            if type(revised) is not str or not 0 < len(revised) <= 3200:
                raise ValueError("INVALID_REVISED_RESPONSE")
            record["coaching_applied"] = True
            record["revision_sha256"] = hashlib.sha256(revised.encode()).hexdigest()
        practice_evidence.append(record)

    holdout_responses = {}
    for task in exam:
        # Only sector and brief go to model; hidden scoring criteria are not
        # forwarded in inference request (although repo itself is public).
        answer = candidate(_prompt(task["sector"], task["brief"]))
        calls += 1
        holdout_responses[task["id"]] = answer

    report = grade_responses(holdout_responses)
    report.update({
        "model":MODEL,
        "source":"real_local_model" if candidate is generate else "injected_test_candidate",
        "inference_calls":calls,
        "practice_cases":len(practice_evidence),
        "practice_revisions":max_practice_revisions,
        "practice_evidence":practice_evidence,
        "no_model_weight_updates":True,
        "model_training_completed":False,
        "commercial_platform_access":False,
        "professional_qualified":False,
        "autonomy_target_percent":75,
        "permission_to_use_external_tools":False,
    })
    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Real local Ollama practice+holdout; no services or client tasks"
    )
    parser.add_argument("--live", action="store_true", help="Run genuinely local Ollama inference")
    args = parser.parse_args()
    if not args.live:
        parser.error("No mocked PASS output. Use --live with an authorized local model.")
    if os.environ.get("LEGION_LOCAL_MODEL_PROBE") != "I_APPROVE_SYNTHETIC_LOCAL_INFERENCE":
        parser.error("Local probe requires LEGION_LOCAL_MODEL_PROBE=I_APPROVE_SYNTHETIC_LOCAL_INFERENCE")
    result = practice_then_examine(generate)
    # Report only hashes, counts and immutable evaluation conclusions. Do not
    # reveal raw model drafts or future customer information in GitHub logs.
    print(json.dumps(result, sort_keys=True, indent=2))
    if result["inference_calls"] < 12:
        raise SystemExit("INCOMPLETE_INFERENCE_SESSION")


if __name__ == "__main__":
    main()
