"""LEGION public demo: 25 professional team role *specifications*, not workers.

New roles can be appended through independently reviewed versioned catalogs.
No names, skills or titles are evidence of deployed NCA or model capabilities.
"""
from __future__ import annotations

from dataclasses import dataclass

CATALOG_VERSION = "legion-roles-v0.1"
SQUADS = ("engineering", "security", "quality", "operations", "research")
SKILLS = frozenset(("TEXT_METRICS", "RISK_MARKERS", "SHA256_TEXT"))
_ROLE_ROWS = (('engineering','systems-architect','TEXT_METRICS'),('engineering','backend-engineer','TEXT_METRICS'),('engineering','frontend-engineer','TEXT_METRICS'),('engineering','integration-engineer','TEXT_METRICS'),('engineering','software-engineer','TEXT_METRICS'),('security','security-architect','RISK_MARKERS'),('security','appsec-engineer','RISK_MARKERS'),('security','identity-specialist','RISK_MARKERS'),('security','threat-analyst','RISK_MARKERS'),('security','audit-specialist','RISK_MARKERS'),('quality','qa-lead','TEXT_METRICS'),('quality','test-engineer','TEXT_METRICS'),('quality','reliability-analyst','TEXT_METRICS'),('quality','accessibility-analyst','TEXT_METRICS'),('quality','release-verifier','TEXT_METRICS'),('operations','operations-lead','SHA256_TEXT'),('operations','incident-coordinator','SHA256_TEXT'),('operations','domain-coordinator','SHA256_TEXT'),('operations','deployment-reviewer','SHA256_TEXT'),('operations','automation-analyst','SHA256_TEXT'),('research','research-lead','TEXT_METRICS'),('research','knowledge-curator','TEXT_METRICS'),('research','data-analyst','TEXT_METRICS'),('research','model-evaluator','TEXT_METRICS'),('research','documentation-engineer','TEXT_METRICS'))


@dataclass(frozen=True)
class Role:
    code: str
    squad: str
    allowed_skill: str


ROLES = tuple(Role(code, squad, skill) for squad, code, skill in _ROLE_ROWS)
ROLE_INDEX = {role.code: role for role in ROLES}


def validate_catalog() -> None:
    if len(ROLES) != 25 or len(ROLE_INDEX) != 25:
        raise ValueError("Expected exactly 25 distinct pilot role specifications")
    for squad in SQUADS:
        if sum(role.squad == squad for role in ROLES) != 5:
            raise ValueError("Five demo roles required for each pilot squad")
    for role in ROLES:
        if role.squad not in SQUADS or role.allowed_skill not in SKILLS:
            raise ValueError("Unknown squad or safe demo capability")


validate_catalog()

# Additional commercial profession templates. These are descriptions of roles,
# not trained models or deployed workers. New sectors require reviewed catalog
# versions and corresponding domain-specific training/QA before external use.
from .sectors import SECTORS

PROFESSIONAL_ROLE_VERSION = "legion-professional-pack-v0.1"
_PROFESSIONAL_ROWS = (
    ('professional-software-consultant', 'software-development', 'engineering', 'TEXT_METRICS'),
    ('professional-web-developer', 'website-development', 'engineering', 'SHA256_TEXT'),
    ('professional-quality-tester', 'quality-assurance', 'quality', 'TEXT_METRICS'),
    ('professional-defensive-security-analyst', 'defensive-cybersecurity', 'security', 'RISK_MARKERS'),
    ('professional-researcher', 'research', 'research', 'TEXT_METRICS'),
    ('professional-data-analyst', 'data-analysis', 'research', 'TEXT_METRICS'),
    ('professional-data-cleaner', 'data-cleaning', 'research', 'TEXT_METRICS'),
    ('professional-business-analyst', 'business-analytics', 'research', 'TEXT_METRICS'),
    ('professional-graphic-designer', 'graphic-design', 'creative', 'TEXT_METRICS'),
    ('professional-video-editor', 'video-production', 'creative', 'SHA256_TEXT'),
    ('professional-animator', 'animation', 'creative', 'TEXT_METRICS'),
    ('professional-audio-producer', 'audio-production', 'creative', 'SHA256_TEXT'),
    ('professional-copywriter', 'copywriting', 'creative', 'TEXT_METRICS'),
    ('professional-translator', 'translation', 'creative', 'TEXT_METRICS'),
    ('professional-localization-specialist', 'localization', 'creative', 'TEXT_METRICS'),
    ('professional-content-manager', 'content-management', 'creative', 'TEXT_METRICS'),
    ('professional-seo-analyst', 'ethical-seo', 'growth', 'RISK_MARKERS'),
    ('professional-marketing-analyst', 'digital-marketing', 'growth', 'TEXT_METRICS'),
    ('professional-customer-support-specialist', 'customer-support', 'customer', 'TEXT_METRICS'),
    ('professional-crm-operator', 'crm-operations', 'customer', 'SHA256_TEXT'),
    ('professional-lead-researcher', 'sales-research', 'growth', 'RISK_MARKERS'),
    ('professional-ecommerce-manager', 'ecommerce-operations', 'commerce', 'TEXT_METRICS'),
    ('professional-technical-writer', 'product-documentation', 'creative', 'TEXT_METRICS'),
    ('professional-education-author', 'education-content', 'education', 'TEXT_METRICS'),
    ('professional-virtual-assistant', 'virtual-assistance', 'operations', 'TEXT_METRICS'),
    ('professional-project-manager', 'project-management', 'operations', 'TEXT_METRICS'),
    ('professional-workflow-specialist', 'workflow-automation', 'operations', 'SHA256_TEXT'),
    ('professional-real-estate-researcher', 'real-estate-research', 'research', 'TEXT_METRICS'),
    ('professional-recruiting-coordinator', 'recruiting-administration', 'customer', 'TEXT_METRICS'),
    ('professional-accessibility-tester', 'accessibility-testing', 'quality', 'TEXT_METRICS'),
    ('professional-reporting-analyst', 'financial-reporting-research', 'research', 'TEXT_METRICS'),
    ('professional-community-moderator', 'community-moderation', 'customer', 'RISK_MARKERS'),
    ('professional-ux-researcher', 'ux-research', 'creative', 'TEXT_METRICS'),
    ('professional-market-researcher', 'market-research', 'research', 'TEXT_METRICS'),
    ('professional-digital-product-builder', 'digital-product-development', 'engineering', 'TEXT_METRICS'),
    ('professional-technical-support', 'technical-support', 'customer', 'TEXT_METRICS'),
    ('professional-process-consultant', 'business-process-analysis', 'operations', 'TEXT_METRICS'),
)
PROFESSIONAL_ROLE_INDEX = {
    code: Role(code, squad, skill)
    for code, sector, squad, skill in _PROFESSIONAL_ROWS
}
PROFESSIONAL_ROLE_SECTORS = {
    code: sector for code, sector, squad, skill in _PROFESSIONAL_ROWS
}
ALL_ROLE_INDEX = {**ROLE_INDEX, **PROFESSIONAL_ROLE_INDEX}

if len(PROFESSIONAL_ROLE_INDEX) != len(_PROFESSIONAL_ROWS):
    raise ValueError("Professional role codes must be unique")
if set(PROFESSIONAL_ROLE_INDEX).intersection(ROLE_INDEX):
    raise ValueError("Commercial profession names must not collide with original roles")
if set(PROFESSIONAL_ROLE_SECTORS.values()) != SECTORS:
    raise ValueError("Each initial business sector needs a professional role template")
if any(r.allowed_skill not in SKILLS for r in PROFESSIONAL_ROLE_INDEX.values()):
    raise ValueError("Commercial template skill not allowlisted")
