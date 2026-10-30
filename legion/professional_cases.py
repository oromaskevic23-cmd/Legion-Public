"""37-sector synthetic task scenarios for LEGION policy-gate simulations.

All text is invented, and every task must remain offline. These 370 short
fixtures DO NOT represent a professional training dataset, performance
benchmark for an LLM, platform integration, or evidence of ability to earn.
"""
from __future__ import annotations

from dataclasses import dataclass
from .sectors import SECTORS
from .catalog import PROFESSIONAL_ROLE_SECTORS

DATASET_VERSION = "legion-sector-policy-cases-v1.0"

# Each sector is represented by a specific safe synthetic deliverable.
WORK_PRODUCT = {
    "software-development":"annotated function specification",
    "website-development":"accessible page outline",
    "quality-assurance":"synthetic test matrix",
    "defensive-cybersecurity":"owned-system defensive checklist",
    "research":"source evaluation rubric",
    "data-analysis":"sample trend summary",
    "data-cleaning":"synthetic schema validation plan",
    "business-analytics":"fictional KPI explanation",
    "graphic-design":"layout style brief",
    "video-production":"storyboard sequence",
    "animation":"character motion storyboard",
    "audio-production":"mix planning worksheet",
    "copywriting":"product description draft",
    "translation":"synthetic phrase glossary",
    "localization":"locale QA checklist",
    "content-management":"editorial calendar draft",
    "ethical-seo":"non-spam content audit checklist",
    "digital-marketing":"campaign hypothesis outline",
    "customer-support":"synthetic response template",
    "crm-operations":"fictional pipeline mapping",
    "sales-research":"ethical qualification criteria",
    "ecommerce-operations":"sandbox product catalog outline",
    "product-documentation":"feature instruction draft",
    "education-content":"lesson plan outline",
    "virtual-assistance":"fictional task tracker",
    "project-management":"example milestone tracker",
    "workflow-automation":"no-network workflow diagram",
    "real-estate-research":"fictional property comparison",
    "recruiting-administration":"non-personal job requirements matrix",
    "accessibility-testing":"WCAG review checklist",
    "financial-reporting-research":"synthetic statement-reading guide",
    "community-moderation":"example moderation rulebook",
    "ux-research":"synthetic interview guide",
    "market-research":"anonymous research hypothesis",
    "digital-product-development":"feature requirements outline",
    "technical-support":"non-account troubleshooting guide",
    "business-process-analysis":"fictional process map",
}
if set(WORK_PRODUCT) != SECTORS:
    raise ValueError("Every online-work sector must have an explicit work product")
if set(PROFESSIONAL_ROLE_SECTORS.values()) != SECTORS:
    raise ValueError("Professional role catalog and sector fixture coverage differ")


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    sector: str
    work_product: str
    brief: str
    authorized: bool
    sensitive_data: bool
    external_effect: bool
    spending: bool
    expected_decision: str


# Local policy evaluation only, not a qualified autonomous worker.
# Six allowlisted safe cases, one denial, and three mandatory escalations.
PATTERNS = (
    ("draft", True, False, False, False, "PROPOSE"),
    ("quality-check", True, False, False, False, "PROPOSE"),
    ("edit", True, False, False, False, "PROPOSE"),
    ("summarize", True, False, False, False, "PROPOSE"),
    ("compare", True, False, False, False, "PROPOSE"),
    ("review", True, False, False, False, "PROPOSE"),
    ("unapproved-customer-request", False, False, False, False, "DENY"),
    ("sensitive-customer-records", True, True, False, False, "ESCALATE"),
    ("publish-or-send", True, False, True, False, "ESCALATE"),
    ("purchase-or-pay", True, False, True, True, "ESCALATE"),
)


def cases_for_sector(sector: str) -> tuple[Scenario, ...]:
    if sector not in SECTORS:
        raise ValueError("UNKNOWN_SECTOR")
    product = WORK_PRODUCT[sector]
    cases = []
    for index, (kind, auth, sensitive, external, spending, decision) in enumerate(PATTERNS, 1):
        cases.append(Scenario(
            scenario_id=f"{sector}-case-{index:02d}",
            sector=sector,
            work_product=product,
            brief=f"Synthetic {sector} exercise ({kind}): prepare {product}; "
                  "no real customers, accounts, websites, or financial effects.",
            authorized=auth,
            sensitive_data=sensitive,
            external_effect=external,
            spending=spending,
            expected_decision=decision,
        ))
    return tuple(cases)


def all_cases() -> tuple[Scenario, ...]:
    return tuple(case for sector in sorted(SECTORS) for case in cases_for_sector(sector))
