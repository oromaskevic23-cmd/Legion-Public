"""A deliberately small rule-based candidate for synthetic LEGION policy triage.

It is not an LLM, skill training, content production engine, or autonomous
online agent. The output is inert, locally testable proposal data.
"""
from __future__ import annotations

from .professional_cases import Scenario


def propose(case: Scenario) -> dict:
    if type(case) is not Scenario:
        raise TypeError("ONLY_SYNTHETIC_SCENARIOS")
    if not case.authorized:
        decision = "DENY"
    elif case.sensitive_data or case.external_effect or case.spending:
        decision = "ESCALATE"
    else:
        decision = "PROPOSE"
    return {
        "scenario_id": case.scenario_id,
        "sector": case.sector,
        "decision": decision,
        "work_product": case.work_product,
        "artifact_outline": (
            "SYNTHETIC ONLY: outline for " + case.work_product
            if decision == "PROPOSE" else ""
        ),
        "requires_human": decision != "PROPOSE",
        "external_effects": 0,
        "spend_cents": 0,
        "professional_qualified": False,
        "production_authorized": False,
    }
