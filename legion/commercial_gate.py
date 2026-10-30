"""LEGION commercial access remains explicitly disabled.

An exam score is never an authorization token. A real transition must happen
later through deployed HANTER, AI Passport, Guardian and Approval controls.
"""
from __future__ import annotations


class CommercialAccessDenied(PermissionError):
    pass


def require_professional_platform_access(*, exam_report: dict,
                                         requested_platform: str,
                                         alleged_owner_approval: object = None) -> None:
    """Fail closed regardless of scoring or caller-provided fake approval."""
    if type(exam_report) is not dict or not requested_platform:
        raise CommercialAccessDenied("INVALID_ACCESS_REQUEST")
    raise CommercialAccessDenied("PRODUCTION_CONNECTORS_NOT_IMPLEMENTED")
