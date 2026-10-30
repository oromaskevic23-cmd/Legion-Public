"""LEGION local demo command line. No owner authentication or remote control.

The stop command is manual when used by an authorized local operator; the
corresponding Legion.stop() method is the code-level interface. Production
must add authenticated owner commands and distributed cancellation.
"""
from __future__ import annotations
import argparse
import json
import tempfile
from pathlib import Path
from .lifecycle import Denied, Legion


def synthetic_demo() -> dict:
    with tempfile.TemporaryDirectory(prefix="legion-sim-") as root:
        db=Path(root) / "legion.sqlite"
        system=Legion(db)
        system.register(agent_id="NCA-LEGION-001", role="software-engineer",
                        sector="software-development",mission="demo-mission",
                        product_class="INTERNAL",lifetime_seconds=900,now=1000)
        simulation=system.simulate("NCA-LEGION-001",now=1001)
        system.activate_sandbox("NCA-LEGION-001",now=1002)
        steps=[]
        for index in range(4):
            steps.append(system.step("NCA-LEGION-001",
                 f"synthetic project text {index}",manual_review=(index==3),now=1003+index)["review"])
        system.stop(scope="global",subject="*",reason="Owner-initiated sandbox stop")
        stopped=False
        try:
            system.step("NCA-LEGION-001","must be blocked",now=1008)
        except Denied as e:
            stopped=str(e)=="OWNER_KILL_SWITCH"
        return {"agent":"NCA-LEGION-001","simulation_passed":simulation["passed"],
                "simulation_total":simulation["total"],"step_reviews":steps,
                "owner_kill_switch_blocked_execution":stopped,
                "audit_chain_valid":system.audit_valid(),
                "local_sandbox_only":True,"revenue_confirmed":False}


def main():
    parser=argparse.ArgumentParser(description="LEGION offline simulation and stop controls")
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("demo",help="Disposable 12-case training, 4 steps, global kill")
    kill=sub.add_parser("stop",help="Persist a fail-closed kill control in a local SQLite file")
    kill.add_argument("--db",required=True)
    kill.add_argument("--scope",required=True,choices=("global","squad","agent","mission"))
    kill.add_argument("--subject",required=True)
    kill.add_argument("--reason",required=True)
    inspect=sub.add_parser("inspect",help="Read an existing local test agent")
    inspect.add_argument("--db",required=True)
    inspect.add_argument("--agent",required=True)
    args=parser.parse_args()
    try:
        if args.command=="demo":
            output=synthetic_demo()
        elif args.command=="stop":
            Legion(Path(args.db)).stop(scope=args.scope,subject=args.subject,reason=args.reason)
            output={"stop_persisted":True,"scope":args.scope,"subject":args.subject}
        else:
            output=Legion(Path(args.db)).inspect(args.agent)
        print(json.dumps(output,sort_keys=True,indent=2))
    except Denied as exc:
        parser.exit(2,"DENIED: "+str(exc)+"\n")

if __name__=="__main__":
    main()
