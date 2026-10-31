"""LEGION Sprint 013 signed demo dispatch: negative control and replay tests.

Ephemeral Ed25519 keys generated exclusively within test processes.
"""
import copy
import hashlib
import secrets
import tempfile
import unittest
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from legion.commercial_gate import (
    CommercialAccessDenied, require_professional_platform_access,
)
from legion.lifecycle import Denied, Legion
from legion.signed_demo_dispatch import (
    AGENT, AUDIENCE, CAPABILITY, ISSUER, MISSION, ROUTE,
    SignedMissionDenied, run_authorized_synthetic_html, signed_message,
    verify_demo_permit,
)
from legion.website_qa_exam import load_cases


class SignedDemoDispatchTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.database = Path(folder.name) / "agent.sqlite"
        self.engine = Legion(self.database)
        self.engine.register(
            agent_id=AGENT, role="professional-accessibility-tester",
            sector="accessibility-testing", mission=MISSION,
            lifetime_seconds=120, mission_lifetime_seconds=90, now=1000,
        )
        self.engine.simulate(AGENT, now=1001)
        self.engine.activate_sandbox(AGENT, now=1002)
        self.private_key = Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        self.key_id = "DEMO-HANTER-TEST-1"
        self.keys = {self.key_id:self.public_key}
        self.html = load_cases()[0]["html"]
        self.permit = self.new_permit()

    def new_permit(self, **changes):
        body = {
            "version":1, "issuer":ISSUER, "audience":AUDIENCE,
            "orchestrator_id":ROUTE, "agent_id":AGENT,
            "mission":MISSION, "capability":CAPABILITY,
            "html_sha256":hashlib.sha256(self.html.encode()).hexdigest(),
            "nonce":secrets.token_hex(16), "issued_at":1003, "expires_at":1050,
        }
        body.update(changes)
        return {
            "payload":body, "key_id":self.key_id,
            "signature":self.private_key.sign(
                signed_message(body,self.key_id)).hex(),
        }

    def run_step(self, permit=None, **kwargs):
        return run_authorized_synthetic_html(
            self.engine, envelope=self.permit if permit is None else permit,
            trusted_keys=self.keys, html=kwargs.pop("html", self.html),
            now=kwargs.pop("now",1004), **kwargs,
        )

    def assert_signer_denied(self, payload, code):
        with self.assertRaises(SignedMissionDenied) as ctx:
            verify_demo_permit(payload,self.keys,now=1004)
        self.assertEqual(str(ctx.exception),code)

    def test_one_signed_demo_step_is_accepted_and_all_live_rights_remain_false(self):
        result = self.run_step()
        self.assertEqual(result["step"],1)
        self.assertTrue(result["permit_verified_cryptographically"])
        self.assertTrue(result["permit_is_demo_only"])
        self.assertFalse(result["commercial_platform_access"])
        self.assertFalse(result["owner_approval_verified"])
        self.assertFalse(result["real_hanter_identity_verified"])
        self.assertFalse(result["browser_executed"])
        self.assertTrue(self.engine.audit_valid())

    def test_replay_is_denied_after_process_restart(self):
        self.run_step()
        with self.assertRaisesRegex(SignedMissionDenied,"PERMIT_REPLAY_DENIED"):
            self.run_step()
        self.engine=Legion(self.database)
        with self.assertRaisesRegex(SignedMissionDenied,"PERMIT_REPLAY_DENIED"):
            self.run_step()
        self.assertEqual(self.engine.inspect(AGENT)["steps"],1)

    def test_new_valid_nonce_can_authorize_next_bounded_step(self):
        self.run_step()
        result=self.run_step(permit=self.new_permit())
        self.assertEqual(result["step"],2)

    def test_forged_payload_without_new_signature_denied(self):
        fake=copy.deepcopy(self.permit)
        fake["payload"]["nonce"]="f"*32
        self.assert_signer_denied(fake,"INVALID_SIGNATURE")

    def test_signature_byte_tampering_denied(self):
        fake=copy.deepcopy(self.permit)
        fake["signature"]="00"*64
        self.assert_signer_denied(fake,"INVALID_SIGNATURE")

    def test_untrusted_signer_denied(self):
        with self.assertRaisesRegex(SignedMissionDenied,"UNKNOWN_TRUSTED_SIGNER"):
            verify_demo_permit(self.permit,{},now=1004)

    def test_wrong_public_key_denied(self):
        bogus=Ed25519PrivateKey.generate().public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        with self.assertRaisesRegex(SignedMissionDenied,"INVALID_SIGNATURE"):
            verify_demo_permit(self.permit,{self.key_id:bogus},now=1004)

    def test_missing_or_extra_fields_denied(self):
        fake=copy.deepcopy(self.permit)
        fake["payload"]["commercial_access"]=True
        self.assert_signer_denied(fake,"INVALID_PERMIT_SCHEMA")
        fake=copy.deepcopy(self.permit)
        del fake["payload"]["nonce"]
        self.assert_signer_denied(fake,"INVALID_PERMIT_SCHEMA")
        fake=copy.deepcopy(self.permit)
        fake["trusted_public_key"]=self.public_key.hex()
        self.assert_signer_denied(fake,"INVALID_ENVELOPE")

    def test_wrong_issuer_route_agent_mission_audience_or_capability_denied(self):
        for change in (
            {"issuer":"HANTER-PRODUCTION"},
            {"orchestrator_id":"ORCHESTRATOR-UNKNOWN"},
            {"agent_id":"NCA-OTHER"},
            {"mission":"commercial-work"},
            {"audience":"COMMERCIAL"},
            {"capability":"PAYMENT_AND_WEB_BROWSER"},
        ):
            with self.subTest(change=change):
                self.assert_signer_denied(
                    self.new_permit(**change), "FORBIDDEN_PERMIT_SCOPE"
                )

    def test_expired_future_too_long_or_invalid_clock_denied(self):
        self.assert_signer_denied(
            self.new_permit(issued_at=1000,expires_at=1004),"PERMIT_NOT_CURRENT"
        )
        self.assert_signer_denied(
            self.new_permit(issued_at=1010,expires_at=1060),"PERMIT_NOT_CURRENT"
        )
        self.assert_signer_denied(
            self.new_permit(issued_at=1000,expires_at=1600),"PERMIT_NOT_CURRENT"
        )
        with self.assertRaisesRegex(SignedMissionDenied,"INVALID_NOW"):
            verify_demo_permit(self.permit,self.keys,now=True)

    def test_document_swap_denied_before_permit_consumption(self):
        with self.assertRaisesRegex(SignedMissionDenied,"DOCUMENT_DIGEST_MISMATCH"):
            self.run_step(html=self.html+" ")
        self.assertEqual(self.run_step()["step"],1)

    def test_owner_global_stop_blocks_signed_permit(self):
        self.engine.stop(scope="global",subject="*",reason="Emergency owner stop")
        with self.assertRaisesRegex(Denied,"OWNER_KILL_SWITCH"):
            self.run_step()
        self.assertEqual(self.engine.inspect(AGENT)["steps"],0)

    def test_owner_agent_stop_blocks_signed_permit(self):
        self.engine.stop(scope="agent",subject=AGENT,reason="Stop one NCA")
        with self.assertRaisesRegex(Denied,"OWNER_KILL_SWITCH"):
            self.run_step()

    def test_mission_lease_expiry_still_denies_even_with_valid_signature(self):
        later=self.new_permit(issued_at=1091,expires_at=1130)
        with self.assertRaisesRegex(Denied,"MISSION_EXPIRED"):
            self.run_step(permit=later,now=1091)

    def test_fourth_step_requires_local_demo_review_not_fake_owner_approval(self):
        self.run_step()
        self.run_step(permit=self.new_permit())
        self.run_step(permit=self.new_permit())
        with self.assertRaisesRegex(Denied,"MANUAL_REVIEW_REQUIRED"):
            self.run_step(permit=self.new_permit())
        self.assertEqual(self.engine.inspect(AGENT)["steps"],3)
        # Purely LOCAL TEST flag, explicitly NOT a real Owner signature.
        fourth=self.run_step(permit=self.new_permit(),manual_review=True)
        self.assertEqual(fourth["review"],"MANUAL_TEST_REVIEW")
        self.assertFalse(fourth["owner_approval_verified"])

    def test_expert_scoring_or_fake_approval_never_opens_commerce(self):
        with self.assertRaises(CommercialAccessDenied):
            require_professional_platform_access(
                exam_report={"passed":1_000_000,"qualified":True},
                requested_platform="client-payments",
                alleged_owner_approval=self.permit,
            )

    def test_tampered_local_audit_causes_fail_closed_dispatch(self):
        self.engine.stop(scope="mission",subject="unrelated",reason="audit record")
        import sqlite3
        with sqlite3.connect(self.database) as db:
            db.execute("UPDATE audit SET event='tampered' WHERE seq=1")
        with self.assertRaisesRegex(SignedMissionDenied,"LOCAL_AUDIT_CHAIN_INVALID"):
            self.run_step()


if __name__ == "__main__":
    unittest.main()
