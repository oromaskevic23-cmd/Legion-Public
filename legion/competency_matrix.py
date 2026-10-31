"""Coverage map for 37 internet-service sectors — planned standards only.

Professional competence has to be evaluated on meaningful domain deliverables,
not inferred from a role title or a generic language model.
"""
from __future__ import annotations

from .professional_cases import WORK_PRODUCT
from .sectors import SECTORS

SECURITY_CRITICAL = frozenset({
    "defensive-cybersecurity", "financial-reporting-research",
    "recruiting-administration", "customer-support", "crm-operations",
    "real-estate-research", "technical-support", "ecommerce-operations",
    "workflow-automation", "community-moderation",
})
DATA_SENSITIVE = frozenset({
    "customer-support", "crm-operations", "recruiting-administration",
    "real-estate-research", "financial-reporting-research", "technical-support",
    "community-moderation", "sales-research",
})

QUALITY_DIMENSIONS = (
    "domain_correctness",
    "explicit_uncertainty",
    "privacy_and_data_provenance",
    "scope_and_tool_safety",
    "reproducibility_and_artifact_quality",
    "client_contract_and_rights",
)
MIN_UNSEEN_PER_SECTOR = 30
MIN_INDEPENDENT_SAFETY_PER_SECTOR = 30


def standard_for_sector(sector: str) -> dict:
    if sector not in SECTORS:
        raise ValueError("UNKNOWN_PROFESSIONAL_SECTOR")
    return {
        "sector":sector,
        "expected_deliverable":WORK_PRODUCT[sector],
        "risk_tier":"HIGH" if sector in SECURITY_CRITICAL else "STANDARD",
        "potential_sensitive_data":sector in DATA_SENSITIVE,
        "quality_dimensions":QUALITY_DIMENSIONS,
        "minimum_unseen_exam_cases":MIN_UNSEEN_PER_SECTOR,
        "minimum_independent_safety_cases":MIN_INDEPENDENT_SAFETY_PER_SECTOR,
        "independent_expert_signoff_required":True,
        "actual_customer_permission_required":True,
        "authenticated_guardian_and_approval_required":True,
        "short_lived_mission_required":True,
        "max_unattended_eligible_step_ratio":0.75,
        "external_effects_allowed_in_pilot":False,
        "commercially_qualified":False,
    }


def all_standards() -> tuple[dict, ...]:
    return tuple(standard_for_sector(sector) for sector in sorted(SECTORS))
