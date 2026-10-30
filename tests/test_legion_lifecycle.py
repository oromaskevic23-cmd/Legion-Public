"""LEGION unit tests: synthetic-only. Never evidence of professional AI agents."""
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from legion.catalog import (ROLES, ROLE_INDEX, SQUADS, validate_catalog,
                            PROFESSIONAL_ROLE_INDEX, PROFESSIONAL_ROLE_SECTORS, ALL_ROLE_INDEX)
from legion.lifecycle import Denied, Legion
from legion.sectors import SECTORS
from legion.simulator import run_simulation

ROOT = Path(__file__).resolve().parents[1]


class LegionLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db = Path(self.temp.name) / "legion.sqlite"
        self.system = Legion(self.db)
        self.time = 1000

    def add(self, aid="NCA-001", *, product_class="INTERNAL",
            lifetime_seconds=100, role="software-engineer",
            sector="software-development", mission="mission-1"):
        self.system.register(agent_id=aid, role=role, sector=sector, mission=mission,
                             product_class=product_class,
                             lifetime_seconds=lifetime_seconds, now=self.time)

    def ready(self, aid="NCA-001", **kwargs):
        self.add(aid, **kwargs)
        evidence = self.system.simulate(aid, now=1001)
        self.assertEqual(evidence["passed"], 12)
        self.system.activate_sandbox(aid, now=1002)
        return aid

    def assert_denied(self, code, fn):
        with self.assertRaises(Denied) as error:
            fn()
        self.assertEqual(str(error.exception), code)

    def test_catalog_is_25_roles_and_five_squads(self):
        validate_catalog()
        self.assertEqual(len(ROLES), 25)
        self.assertEqual(len(SQUADS), 5)
        self.assertEqual(len(ROLE_INDEX), 25)
        self.assertGreaterEqual(len(SECTORS), 30)

    def test_professional_catalog_covers_every_declared_online_sector(self):
        self.assertGreaterEqual(len(PROFESSIONAL_ROLE_INDEX), 35)
        self.assertEqual(set(PROFESSIONAL_ROLE_SECTORS.values()), SECTORS)
        self.assertGreater(len(ALL_ROLE_INDEX), 25)

    def test_creative_professional_simulation_then_bounded_work(self):
        self.ready("NCA-DESIGN", role="professional-graphic-designer",
                   sector="graphic-design", mission="design-mission")
        result = self.system.step("NCA-DESIGN", "synthetic brand title",
                                  now=1003)
        self.assertEqual(result["review"], "AUTO")
        self.assertFalse(result["real_world_action"])

    def test_marketing_profession_not_authorized_for_external_effect(self):
        self.ready("NCA-MARKETING", role="professional-marketing-analyst",
                   sector="digital-marketing", mission="marketing-mission")
        self.assert_denied("EXTERNAL_EFFECTS_FORBIDDEN", lambda:
                           self.system.step("NCA-MARKETING",
                               "send mass unsolicited outreach",
                               external_effect=True, now=1003))

    def test_profession_cannot_impersonate_other_sector(self):
        self.assert_denied("ROLE_SECTOR_MISMATCH", lambda:
                           self.add(role="professional-graphic-designer",
                                    sector="financial-reporting-research"))

    def test_simulation_for_all_three_safe_skills(self):
        for skill in ("TEXT_METRICS", "RISK_MARKERS", "SHA256_TEXT"):
            with self.subTest(skill=skill):
                evidence=run_simulation(skill)
                self.assertEqual((evidence["passed"],evidence["total"]),(12,12))
                self.assertEqual(len(evidence["evidence_sha256"]),64)

    def test_no_real_customer_activation_before_simulation(self):
        self.add()
        self.assert_denied("SIMULATION_FIRST", lambda:
                           self.system.activate_sandbox("NCA-001",now=1002))

    def test_simulation_certificate_and_activation(self):
        self.ready()
        row=self.system.inspect("NCA-001")
        self.assertEqual(row["state"],"SANDBOX_ACTIVE")
        self.assertEqual(row["simulated_cases"],12)
        self.assertEqual(len(row["certificate"]),64)

    def test_three_autonomous_steps_fourth_requires_review(self):
        self.ready()
        for i in range(3):
            out=self.system.step("NCA-001", f"synthetic {i}",now=1003+i)
            self.assertEqual(out["review"],"AUTO")
            self.assertFalse(out["real_world_action"])
        self.assert_denied("MANUAL_REVIEW_REQUIRED", lambda:
                           self.system.step("NCA-001","fourth",now=1006))
        out=self.system.step("NCA-001","reviewed synthetic",manual_review=True,now=1006)
        self.assertEqual(out["review"],"MANUAL_TEST_REVIEW")
        state=self.system.inspect("NCA-001")
        self.assertEqual((state["steps"],state["auto_steps"],state["manual_steps"]),(4,3,1))
        self.assertTrue(self.system.audit_valid())

    def test_fifth_step_resets_autonomy_window(self):
        self.ready()
        for i in range(4):
            self.system.step("NCA-001","x",manual_review=(i==3),now=1003+i)
        self.assertEqual(self.system.step("NCA-001","fifth",now=1007)["review"],"AUTO")

    def test_global_stop_blocks_existing_and_future_agents_and_survives_restart(self):
        self.ready()
        self.system.stop(scope="global",subject="*",reason="Owner stop all agents")
        self.assert_denied("OWNER_KILL_SWITCH",lambda:
                           Legion(self.db).step("NCA-001","no",now=1010))
        self.assert_denied("OWNER_KILL_SWITCH",lambda:
                           Legion(self.db).register(agent_id="NEW",role="software-engineer",
                           sector="software-development",mission="another",
                           product_class="INTERNAL",lifetime_seconds=100,now=1011))

    def test_squad_stop_blocks_only_its_squad(self):
        self.ready()
        self.ready("NCA-002",role="security-architect",sector="defensive-cybersecurity",
                   mission="mission-2")
        self.system.stop(scope="squad",subject="engineering",reason="Owner stops engineering")
        self.assert_denied("OWNER_KILL_SWITCH",lambda:self.system.step("NCA-001","no",now=1004))
        result=self.system.step("NCA-002","synthetic",now=1004)
        self.assertEqual(result["agent"],"NCA-002")

    def test_agent_stop_persistent(self):
        self.ready()
        self.system.stop(scope="agent",subject="NCA-001",reason="Owner disabled agent")
        self.assertEqual(self.system.inspect("NCA-001")["state"],"STOPPED")
        self.assert_denied("OWNER_KILL_SWITCH",lambda:Legion(self.db).step("NCA-001","no",now=1005))

    def test_mission_stop_persistent(self):
        self.ready()
        self.system.stop(scope="mission",subject="mission-1",reason="Terminate mission")
        self.assert_denied("OWNER_KILL_SWITCH",lambda:self.system.step("NCA-001","no",now=1005))

    def test_internal_agent_expires(self):
        self.ready()
        self.assert_denied("AGENT_EXPIRED",lambda:self.system.step("NCA-001","later",now=1100))

    def test_sale_offer_agent_has_no_agent_expiry(self):
        self.ready(product_class="SALE_OFFER",lifetime_seconds=None)
        row=self.system.inspect("NCA-001")
        self.assertIsNone(row["expires_at"])
        self.assertEqual(row["product_class"],"SALE_OFFER")
        # The product record does not expire, but its assigned mission does.
        self.assertEqual(row["mission_expires_at"], 4600)
        out=self.system.step("NCA-001","synthetic sample",now=1005)
        self.assertFalse(out["real_world_action"])
        self.assert_denied("MISSION_EXPIRED",lambda:self.system.step(
            "NCA-001","never an endless mission",now=4600))
        self.system.stop(scope="global",subject="*",reason="Safety override remains valid")
        self.assert_denied("OWNER_KILL_SWITCH",lambda:self.system.step("NCA-001","no",now=4601))

    def test_mission_expiry_applies_to_internal_agent(self):
        self.add(lifetime_seconds=100,mission="mission-1")
        self.system.simulate("NCA-001",now=1001)
        self.system.activate_sandbox("NCA-001",now=1002)
        self.assert_denied("MISSION_EXPIRED", lambda:
                           self.system.step("NCA-001","x",now=4600))

    def test_missing_mission_lease_is_fail_closed(self):
        self.ready()
        with sqlite3.connect(self.db) as cx:
            cx.execute("DELETE FROM mission_leases WHERE agent_id='NCA-001'")
        self.assert_denied("MISSING_MISSION_LEASE", lambda:
                           self.system.step("NCA-001","x",now=1004))

    def test_invalid_mission_ttl_rejected(self):
        self.assert_denied("FINITE_MISSION_TTL_REQUIRED",lambda:
            self.system.register(
                agent_id="NCA-001",role="software-engineer",
                sector="software-development",mission="mission-1",
                mission_lifetime_seconds=0,now=1000))

    def test_perpetual_sale_offer_rejects_expiration_input(self):
        self.assert_denied("SALE_OFFER_MUST_BE_TIMELESS",lambda:self.add(
            product_class="SALE_OFFER",lifetime_seconds=100))

    def test_internal_requires_positive_finite_lifetime(self):
        self.assert_denied("FINITE_INTERNAL_TTL_REQUIRED",lambda:self.add(lifetime_seconds=None))
        self.assert_denied("FINITE_INTERNAL_TTL_REQUIRED",lambda:self.add(lifetime_seconds=0))

    def test_external_effects_always_denied_even_if_manual_reviewed(self):
        self.ready()
        self.assert_denied("EXTERNAL_EFFECTS_FORBIDDEN",lambda:
                           self.system.step("NCA-001","pay customer",manual_review=True,
                                            external_effect=True,now=1005))

    def test_unknown_role_denied(self):
        self.assert_denied("UNREGISTERED_ROLE_OR_SECTOR",lambda:self.add(role="owner-superuser"))

    def test_duplicate_agent_denied(self):
        self.add()
        self.assert_denied("DUPLICATE_AGENT",self.add)

    def test_bad_stop_scopes_denied(self):
        self.assert_denied("INVALID_STOP_SCOPE",lambda:self.system.stop(
            scope="all-payouts",subject="*",reason="test"))

    def test_no_empty_stop_reason(self):
        self.assert_denied("REASON_REQUIRED",lambda:self.system.stop(
            scope="global",subject="*",reason=""))

    def test_audit_detects_in_place_event_change(self):
        self.ready()
        self.assertTrue(self.system.audit_valid())
        with sqlite3.connect(self.db) as cx:
            cx.execute("UPDATE audit SET event='tampered' WHERE seq=1")
        self.assertFalse(self.system.audit_valid())

    def test_manual_cli_stop(self):
        self.ready()
        done=subprocess.run([sys.executable,"-m","legion.cli","stop",
             "--db",str(self.db),"--scope","agent","--subject","NCA-001",
             "--reason","Owner manual CLI halt"],capture_output=True,text=True,check=True)
        self.assertTrue(json.loads(done.stdout)["stop_persisted"])
        self.assert_denied("OWNER_KILL_SWITCH",lambda:self.system.step("NCA-001","no",now=1007))

    def test_disposable_demo_end_to_end(self):
        done=subprocess.run([sys.executable,"-m","legion.cli","demo"],
                            capture_output=True,text=True,check=True)
        evidence=json.loads(done.stdout)
        self.assertEqual(evidence["simulation_passed"],12)
        self.assertEqual(evidence["step_reviews"],["AUTO","AUTO","AUTO","MANUAL_TEST_REVIEW"])
        self.assertTrue(evidence["owner_kill_switch_blocked_execution"])
        self.assertTrue(evidence["audit_chain_valid"])
        self.assertFalse(evidence["revenue_confirmed"])

    def test_english_only_founder_link(self):
        readme=(ROOT/"README.md").read_text()
        self.assertNotIn("EN / UK / RU",readme)
        self.assertIn("oromaskevic23-cmd#founder-introduction",readme)

    def test_license_inventory_matches_actual_root_license(self):
        self.assertTrue((ROOT/"LICENSE").is_file())
        inventory=(ROOT/"governance/LICENSE_INVENTORY.md").read_text()
        self.assertIn("ROOT LICENSE PRESENT",inventory)
        self.assertNotIn("Root license: NOT FOUND",inventory)


if __name__=="__main__":
    unittest.main()
