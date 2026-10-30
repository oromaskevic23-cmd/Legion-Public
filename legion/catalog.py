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
