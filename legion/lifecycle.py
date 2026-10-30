"""LEGION offline lifecycle and stop-control reference. No network, money or live agents.

All permissions are synthetic fixtures, not AI Passports / Owner credentials.
The 75% policy means at most three unattended low-risk steps per four-step
window. Every fourth requires a separate local human confirmation stub.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import time
from pathlib import Path

from .catalog import ALL_ROLE_INDEX, PROFESSIONAL_ROLE_SECTORS
from .sectors import SECTORS

class Denied(Exception):
    """Fail-closed reason code."""

def _event_payload(values: dict) -> str:
    return json.dumps(values, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

class Legion:
    def __init__(self, database: Path):
        self.database = Path(database)
        self.database.parent.mkdir(parents=True, exist_ok=True)
        with self._db() as cx:
            cx.executescript("""
                CREATE TABLE IF NOT EXISTS agents(
                    id TEXT PRIMARY KEY, role TEXT NOT NULL, sector TEXT NOT NULL,
                    squad TEXT NOT NULL, mission TEXT NOT NULL,
                    product_class TEXT NOT NULL, expires_at INTEGER,
                    state TEXT NOT NULL, steps INTEGER NOT NULL DEFAULT 0,
                    auto_steps INTEGER NOT NULL DEFAULT 0,
                    manual_steps INTEGER NOT NULL DEFAULT 0,
                    simulated_cases INTEGER NOT NULL DEFAULT 0,
                    certificate TEXT NOT NULL DEFAULT ''
                );
                CREATE TABLE IF NOT EXISTS kills(
                    scope TEXT NOT NULL, subject TEXT NOT NULL, reason TEXT NOT NULL,
                    PRIMARY KEY(scope, subject)
                );
                CREATE TABLE IF NOT EXISTS audit(
                    seq INTEGER PRIMARY KEY AUTOINCREMENT,
                    event TEXT NOT NULL, prior_sha TEXT NOT NULL, entry_sha TEXT NOT NULL
                );
            """)

    def _db(self):
        cx = sqlite3.connect(self.database, timeout=5)
        cx.row_factory = sqlite3.Row
        cx.execute("PRAGMA busy_timeout=5000")
        return cx

    @staticmethod
    def _now(now: int | None) -> int:
        value = int(time.time()) if now is None else now
        if type(value) is not int or value < 0:
            raise Denied("INVALID_TIME")
        return value

    @staticmethod
    def _identifier(value: str) -> bool:
        return type(value) is str and bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,99}", value))

    def _append(self, cx, event: dict):
        previous = cx.execute("SELECT entry_sha FROM audit ORDER BY seq DESC LIMIT 1").fetchone()
        prev = previous["entry_sha"] if previous else "0" * 64
        body = _event_payload(event)
        digest = hashlib.sha256((prev + "|" + body).encode()).hexdigest()
        cx.execute("INSERT INTO audit(event,prior_sha,entry_sha) VALUES(?,?,?)", (body, prev, digest))

    def _agent(self, cx, agent_id: str):
        row = cx.execute("SELECT * FROM agents WHERE id=?", (agent_id,)).fetchone()
        if row is None:
            raise Denied("UNKNOWN_AGENT")
        return row

    def _gate(self, cx, row, now: int):
        for scope, subject in (("global","*"),("squad",row["squad"]),
                               ("agent",row["id"]),("mission",row["mission"])):
            if cx.execute("SELECT 1 FROM kills WHERE scope=? AND subject=?", (scope,subject)).fetchone():
                raise Denied("OWNER_KILL_SWITCH")
        if row["state"] == "STOPPED":
            raise Denied("AGENT_STOPPED")
        if row["expires_at"] is not None and now >= row["expires_at"]:
            raise Denied("AGENT_EXPIRED")

    def register(self, *, agent_id: str, role: str, sector: str,
                 mission: str, product_class: str = "INTERNAL",
                 lifetime_seconds: int | None = 3600, now: int | None = None):
        """Perpetual SALE_OFFER has no agent expiration; no sale/entitlement is issued."""
        ts = self._now(now)
        if not self._identifier(agent_id) or not self._identifier(mission):
            raise Denied("INVALID_ID_OR_MISSION")
        if role not in ALL_ROLE_INDEX or sector not in SECTORS:
            raise Denied("UNREGISTERED_ROLE_OR_SECTOR")
        if role in PROFESSIONAL_ROLE_SECTORS and PROFESSIONAL_ROLE_SECTORS[role] != sector:
            raise Denied("ROLE_SECTOR_MISMATCH")
        if product_class not in ("INTERNAL","SALE_OFFER"):
            raise Denied("INVALID_PRODUCT_CLASS")
        if product_class == "SALE_OFFER":
            if lifetime_seconds is not None:
                raise Denied("SALE_OFFER_MUST_BE_TIMELESS")
            expiry = None
        else:
            if type(lifetime_seconds) is not int or not 1 <= lifetime_seconds <= 31_536_000:
                raise Denied("FINITE_INTERNAL_TTL_REQUIRED")
            expiry = ts + lifetime_seconds
        squad = ALL_ROLE_INDEX[role].squad
        with self._db() as cx:
            cx.execute("BEGIN IMMEDIATE")
            if cx.execute("SELECT 1 FROM kills WHERE scope='global' AND subject='*'").fetchone():
                raise Denied("OWNER_KILL_SWITCH")
            if cx.execute("SELECT 1 FROM kills WHERE scope='squad' AND subject=?", (squad,)).fetchone():
                raise Denied("OWNER_KILL_SWITCH")
            if cx.execute("SELECT 1 FROM kills WHERE scope='mission' AND subject=?", (mission,)).fetchone():
                raise Denied("OWNER_KILL_SWITCH")
            try:
                cx.execute("""INSERT INTO agents
                    (id,role,sector,squad,mission,product_class,expires_at,state)
                    VALUES (?,?,?,?,?,?,?,'DESIGNED')""",
                    (agent_id,role,sector,squad,mission,product_class,expiry))
            except sqlite3.IntegrityError:
                raise Denied("DUPLICATE_AGENT") from None
            self._append(cx,{"type":"REGISTERED","id":agent_id,"mission":mission,
                             "product_class":product_class,"expires_at":expiry})

    def simulate(self, agent_id: str, *, now: int | None = None) -> dict:
        """Twelve synthetic exercises; deterministic scoring is NOT model training."""
        ts=self._now(now)
        with self._db() as cx:
            cx.execute("BEGIN IMMEDIATE")
            row=self._agent(cx,agent_id)
            self._gate(cx,row,ts)
            if row["state"] != "DESIGNED":
                raise Denied("BAD_LIFECYCLE_STATE")
            role=ALL_ROLE_INDEX[row["role"]]
            from .simulator import run_simulation
            evidence=run_simulation(role.allowed_skill)
            if evidence["passed"] != evidence["total"] or evidence["total"] != 12:
                self._append(cx,{"type":"SIMULATION_FAILED","id":agent_id,
                                 "passed":evidence["passed"],"total":evidence["total"]})
                raise Denied("SIMULATION_NOT_PASSED")
            cx.execute("UPDATE agents SET state='SIMULATED',simulated_cases=?,certificate=? WHERE id=?",
                       (evidence["passed"], evidence["evidence_sha256"],agent_id))
            self._append(cx,{"type":"SIMULATION_PASSED","id":agent_id,
                             "cases":evidence["passed"],"evidence_sha256":evidence["evidence_sha256"]})
            return evidence

    def activate_sandbox(self, agent_id: str, *, now: int | None=None):
        """Synthetic read-only demo only, NEVER customer-work authorization."""
        ts=self._now(now)
        with self._db() as cx:
            cx.execute("BEGIN IMMEDIATE")
            row=self._agent(cx,agent_id)
            self._gate(cx,row,ts)
            if row["state"] != "SIMULATED" or row["simulated_cases"] != 12:
                raise Denied("SIMULATION_FIRST")
            cx.execute("UPDATE agents SET state='SANDBOX_ACTIVE' WHERE id=?",(agent_id,))
            self._append(cx,{"type":"SANDBOX_ACTIVATED","id":agent_id})

    def step(self, agent_id: str, text: str, *, manual_review: bool=False,
             external_effect: bool=False, now: int | None=None) -> dict:
        """At most 3 of 4 slots unattended; 4th needs explicit LOCAL demo review."""
        ts=self._now(now)
        if type(text) is not str or not 1 <= len(text) <= 2000 or "\x00" in text:
            raise Denied("INVALID_SYNTHETIC_INPUT")
        if type(manual_review) is not bool or type(external_effect) is not bool:
            raise Denied("INVALID_POLICY_FLAGS")
        if external_effect:
            raise Denied("EXTERNAL_EFFECTS_FORBIDDEN")
        with self._db() as cx:
            cx.execute("BEGIN IMMEDIATE")
            row=self._agent(cx,agent_id)
            self._gate(cx,row,ts)
            if row["state"] != "SANDBOX_ACTIVE":
                raise Denied("NOT_SANDBOX_ACTIVE")
            slot=row["steps"] % 4
            if slot == 3 and not manual_review:
                raise Denied("MANUAL_REVIEW_REQUIRED")
            from .simulator import perform_local_skill
            skill=ALL_ROLE_INDEX[row["role"]].allowed_skill
            result=perform_local_skill(skill,text)
            cx.execute("""UPDATE agents SET steps=steps+1,
                auto_steps=auto_steps+?,manual_steps=manual_steps+?
                WHERE id=?""",(0 if manual_review else 1,1 if manual_review else 0,agent_id))
            record={"type":"SANDBOX_STEP","id":agent_id,
                    "step":row["steps"]+1,"autonomy":"MANUAL_TEST_REVIEW" if manual_review else "AUTO",
                    "result_sha256":hashlib.sha256(_event_payload(result).encode()).hexdigest()}
            self._append(cx,record)
            return {"agent":agent_id,"step":row["steps"]+1,"result":result,
                    "review":record["autonomy"],"real_world_action":False}

    def stop(self, *, scope: str, subject: str, reason: str):
        """Manual CLI or programmatic call persists fail-closed across restarts."""
        if scope not in ("global","squad","agent","mission"):
            raise Denied("INVALID_STOP_SCOPE")
        if not self._identifier(subject) and not (scope=="global" and subject=="*"):
            raise Denied("INVALID_STOP_TARGET")
        if scope=="global" and subject!="*":
            raise Denied("INVALID_STOP_TARGET")
        if type(reason) is not str or not 1<=len(reason)<=180:
            raise Denied("REASON_REQUIRED")
        with self._db() as cx:
            cx.execute("BEGIN IMMEDIATE")
            cx.execute("INSERT OR REPLACE INTO kills(scope,subject,reason) VALUES(?,?,?)",
                       (scope,subject,reason))
            if scope=="agent":
                cx.execute("UPDATE agents SET state='STOPPED' WHERE id=?",(subject,))
            self._append(cx,{"type":"KILL_SWITCH","scope":scope,
                             "subject":subject,"reason":reason})

    def inspect(self, agent_id: str) -> dict:
        with self._db() as cx:
            row=self._agent(cx,agent_id)
            return dict(row)

    def audit_valid(self) -> bool:
        with self._db() as cx:
            prev="0"*64
            for row in cx.execute("SELECT event,prior_sha,entry_sha FROM audit ORDER BY seq"):
                digest=hashlib.sha256((prev+"|"+row["event"]).encode()).hexdigest()
                if row["prior_sha"]!=prev or row["entry_sha"]!=digest:
                    return False
                prev=row["entry_sha"]
            return True
