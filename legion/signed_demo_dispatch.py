"""LEGION Sprint 013: Ed25519-authenticated *synthetic-only* mission dispatch.

This is a cryptographic protocol demonstrator; keys are generated in tests.
It is NOT connected to the deployed HANTER, a real Owner identity, AI Passport,
Guardian Core or Approval Gateway. Commercial and network actions are forbidden.
Requires the separately pinned 'cryptography' library.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from typing import Mapping

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .lifecycle import Denied, Legion
from .website_qa import scan_html

DOMAIN = b"IMPERIAL-LEGION-DEMO-PERMIT-V1\x00"
VERSION = 1
ISSUER = "HANTER-DEMO-ONLY"
AUDIENCE = "LEGION-SYNTHETIC-ONLY"
ROUTE = "ORCHESTRATOR-LEGION-DEMO"
AGENT = "NCA-LEGION-WEBSITE-QA-001"
MISSION = "synthetic-website-qa-pilot"
CAPABILITY = "STATIC_HTML_QA_LOCAL_ONLY"
MAX_TTL_SECONDS = 300
FIELDS = frozenset({
    "version", "issuer", "audience", "orchestrator_id", "agent_id",
    "mission", "capability", "html_sha256", "nonce",
    "issued_at", "expires_at",
})
ENVELOPE_FIELDS = frozenset({"payload", "key_id", "signature"})
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
NONCE_RE = re.compile(r"[0-9a-f]{32}\Z")
KEY_RE = re.compile(r"DEMO-[A-Za-z0-9._-]{1,60}\Z")
SIGNATURE_RE = re.compile(r"[0-9a-f]{128}\Z")


class SignedMissionDenied(PermissionError):
    """No permission to dispatch the signed local simulation."""


def _canonical(payload: dict) -> bytes:
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def signed_message(payload: dict, key_id: str) -> bytes:
    """Domain-separated deterministic representation; no signing keys here."""
    if type(payload) is not dict or type(key_id) is not str or not KEY_RE.fullmatch(key_id):
        raise SignedMissionDenied("INVALID_SIGNED_MESSAGE")
    return DOMAIN + key_id.encode("ascii") + b"\x00" + _canonical(payload)


def verify_demo_permit(envelope: object, trusted_keys: Mapping[str, bytes],
                       *, now: int) -> dict:
    """Validate one public-key signature and strictly scoped demo claims.

    Trusted public keys MUST be provisioned separately from the signed message.
    Never import a key supplied by the envelope itself.
    """
    if type(now) is not int or now < 0:
        raise SignedMissionDenied("INVALID_NOW")
    if type(envelope) is not dict or set(envelope) != ENVELOPE_FIELDS:
        raise SignedMissionDenied("INVALID_ENVELOPE")
    payload = envelope["payload"]
    kid = envelope["key_id"]
    sig = envelope["signature"]
    if (type(payload) is not dict or set(payload) != FIELDS
            or type(kid) is not str or not KEY_RE.fullmatch(kid)
            or type(sig) is not str or not SIGNATURE_RE.fullmatch(sig)):
        raise SignedMissionDenied("INVALID_PERMIT_SCHEMA")
    if (type(payload["version"]) is not int or payload["version"] != VERSION
            or any(type(payload[x]) is not str for x in (
                "issuer", "audience", "orchestrator_id", "agent_id", "mission",
                "capability", "html_sha256", "nonce"
            ))):
        raise SignedMissionDenied("INVALID_PERMIT_FIELDS")
    if (payload["issuer"] != ISSUER or payload["audience"] != AUDIENCE
            or payload["orchestrator_id"] != ROUTE or payload["agent_id"] != AGENT
            or payload["mission"] != MISSION
            or payload["capability"] != CAPABILITY):
        raise SignedMissionDenied("FORBIDDEN_PERMIT_SCOPE")
    if (not SHA256_RE.fullmatch(payload["html_sha256"])
            or not NONCE_RE.fullmatch(payload["nonce"])):
        raise SignedMissionDenied("INVALID_DIGEST_OR_NONCE")
    issued = payload["issued_at"]
    expires = payload["expires_at"]
    if (type(issued) is not int or type(expires) is not int
            or issued < 0 or expires <= issued
            or expires - issued > MAX_TTL_SECONDS or not issued <= now < expires):
        raise SignedMissionDenied("PERMIT_NOT_CURRENT")
    if not isinstance(trusted_keys, Mapping):
        raise SignedMissionDenied("INVALID_TRUST_STORE")
    key_material = trusted_keys.get(kid)
    if type(key_material) is not bytes or len(key_material) != 32:
        raise SignedMissionDenied("UNKNOWN_TRUSTED_SIGNER")
    try:
        Ed25519PublicKey.from_public_bytes(key_material).verify(
            bytes.fromhex(sig), signed_message(payload, kid)
        )
    except (InvalidSignature, ValueError, TypeError):
        raise SignedMissionDenied("INVALID_SIGNATURE") from None
    return dict(payload)


def run_authorized_synthetic_html(
    engine: Legion, *, envelope: object, trusted_keys: Mapping[str, bytes],
    html: str, now: int, manual_review: bool = False,
) -> dict:
    """Persist replay protection before one existing read-only lifecycle step.

    Valid demo signer != actual HANTER authentication or Owner approval.
    A rejected/failed step may consume the nonce; it can never be replayed.
    All operations are local. No LLM, URL, customer platform or payment tool.
    """
    if type(html) is not str or not 0 < len(html) <= 40_000 or "\x00" in html:
        raise SignedMissionDenied("INVALID_SYNTHETIC_DOCUMENT")
    if type(manual_review) is not bool:
        raise SignedMissionDenied("INVALID_REVIEW_FLAG")
    permit = verify_demo_permit(envelope, trusted_keys, now=now)
    digest = hashlib.sha256(html.encode("utf-8")).hexdigest()
    if digest != permit["html_sha256"]:
        raise SignedMissionDenied("DOCUMENT_DIGEST_MISMATCH")
    # No effects are possible from the scanner; catch invalid source before
    # debiting the permit or consuming the lifecycle step.
    report = scan_html(html)
    if not engine.audit_valid():
        raise SignedMissionDenied("LOCAL_AUDIT_CHAIN_INVALID")
    with engine._db() as cx:
        cx.execute("BEGIN IMMEDIATE")
        row = engine._agent(cx, AGENT)
        engine._gate(cx, row, now)
        if (row["state"] != "SANDBOX_ACTIVE" or row["mission"] != MISSION
                or row["role"] != "professional-accessibility-tester"
                or row["sector"] != "accessibility-testing"):
            raise SignedMissionDenied("UNEXPECTED_AGENT_LIFECYCLE_OR_SCOPE")
        cx.execute("""CREATE TABLE IF NOT EXISTS signed_demo_dispatches (
            issuer TEXT NOT NULL, nonce TEXT NOT NULL,
            agent_id TEXT NOT NULL, payload_sha256 TEXT NOT NULL,
            accepted_at INTEGER NOT NULL,
            PRIMARY KEY (issuer, nonce)
        )""")
        payload_digest = hashlib.sha256(
            signed_message(permit, envelope["key_id"])
        ).hexdigest()
        try:
            cx.execute(
                "INSERT INTO signed_demo_dispatches"
                "(issuer,nonce,agent_id,payload_sha256,accepted_at)"
                " VALUES (?,?,?,?,?)",
                (permit["issuer"], permit["nonce"], AGENT, payload_digest, now)
            )
        except sqlite3.IntegrityError:
            raise SignedMissionDenied("PERMIT_REPLAY_DENIED") from None
        engine._append(cx, {
            "type":"SIGNED_SYNTHETIC_PERMIT_CONSUMED",
            "agent":AGENT, "issuer":ISSUER, "nonce":permit["nonce"],
            "payload_sha256":payload_digest,
            "document_sha256":digest, "real_world_action":False,
        })
    # The established engine checks current persistent stop state, expiry and
    # 75% review policy AGAIN. No real-world effects are allowed by engine.step.
    step = engine.step(
        AGENT, "Signed synthetic HTML digest " + digest,
        manual_review=manual_review, external_effect=False, now=now
    )
    return {
        "permit_verified_cryptographically":True,
        "permit_is_demo_only":True, "permit_consumed":True,
        "agent":AGENT, "mission":MISSION,
        "step":step["step"], "review":step["review"],
        "finding_codes":report["finding_codes"],
        "document_sha256":digest, "payload_sha256":payload_digest,
        "browser_executed":False, "real_world_action":False,
        "real_hanter_identity_verified":False,
        "owner_approval_verified":False,
        "real_guardian_approval_verified":False,
        "real_ai_passport_verified":False,
        "independent_qa_qualified":False,
        "production_authorized":False, "commercial_platform_access":False,
    }
