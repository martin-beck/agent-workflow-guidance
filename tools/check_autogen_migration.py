#!/usr/bin/env python3
"""Validate the bounded AutoGen successor decision snapshot."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any
def fail(message: str) -> None: raise SystemExit(f"AWG-AUTOGEN-FAIL: {message}")
def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("decision", type=Path); args = parser.parse_args()
    try: value: Any = json.loads(args.decision.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error: fail(f"cannot read decision: {error}")
    if not isinstance(value, dict) or value.get("schema_version") != 1 or value.get("decision") != "migrate-new-work" or value.get("runtime_dependency") is not False: fail("migration identity or dependency boundary is invalid")
    auto, successor = value.get("autogen"), value.get("successor")
    if not isinstance(auto, dict) or not re.fullmatch(r"[0-9a-f]{40}", str(auto.get("revision"))) or auto.get("repository") != "microsoft/autogen" or auto.get("maintenance_mode") is not True: fail("AutoGen maintenance evidence is invalid")
    if not isinstance(successor, dict) or successor.get("repository") != "microsoft/agent-framework" or not re.fullmatch(r"[0-9a-f]{40}", str(successor.get("revision"))): fail("successor identity or revision is invalid")
    dimensions = value.get("dimensions")
    if not isinstance(dimensions, dict) or set(dimensions) != {"user_feedback", "termination", "persistence", "authority"}: fail("comparison dimensions are incomplete")
    for name, row in dimensions.items():
        if not isinstance(row, dict) or not all(isinstance(row.get(field), str) and row[field] for field in ("autogen", "successor", "awg_gap")) or not isinstance(row.get("evidence"), str) or not row["evidence"].startswith("https://"): fail(f"{name}: evidence boundary is incomplete")
    if not isinstance(value.get("limitations"), list) or not value["limitations"]: fail("limitations are missing")
    print("AWG-AUTOGEN-PASS: maintenance-aware successor decision")
    return 0
if __name__ == "__main__": raise SystemExit(main())
