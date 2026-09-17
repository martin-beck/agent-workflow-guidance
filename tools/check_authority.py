#!/usr/bin/env python3
"""Validate bounded authority and audit dispositions offline."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any
def fail(message: str) -> None: raise SystemExit(f"AWG-AUTHORITY-FAIL: {message}")
def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("cases", type=Path); args = parser.parse_args()
    try: value: Any = json.loads(args.cases.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error: fail(f"cannot read cases: {error}")
    if not isinstance(value, dict) or value.get("schema_version") != 1 or not isinstance(value.get("cases"), list) or not value["cases"]: fail("invalid authority set")
    seen: set[str] = set(); audit = {"task_id", "scope", "expiry", "disposition"}
    for case in value["cases"]:
        fields = ("id", "task_id", "requested_scope", "approved_scope", "current_tick", "expiry_tick", "alternatives_count", "context_present", "rejection_allowed", "disposition", "audit_fields")
        if not isinstance(case, dict) or any(field not in case for field in fields): fail("authority fields are incomplete")
        if not isinstance(case["id"], str) or case["id"] in seen or not isinstance(case["task_id"], str): fail("authority identity is invalid")
        seen.add(case["id"])
        if not isinstance(case["requested_scope"], list) or not case["requested_scope"] or not isinstance(case["approved_scope"], list) or not isinstance(case["audit_fields"], list) or not audit.issubset(case["audit_fields"]): fail(f"{case['id']}: scope or audit fields incomplete")
        if not set(case["approved_scope"]).issubset(set(case["requested_scope"])): fail(f"{case['id']}: approved scope exceeds requested scope")
        if not all(isinstance(case[key], int) and case[key] >= 0 for key in ("current_tick", "expiry_tick", "alternatives_count")): fail(f"{case['id']}: invalid numeric authority field")
        if not isinstance(case["context_present"], bool) or not isinstance(case["rejection_allowed"], bool) or case["disposition"] not in {"approved", "rejected", "expired"}: fail(f"{case['id']}: invalid disposition")
        if case["disposition"] == "approved" and (case["current_tick"] >= case["expiry_tick"] or case["alternatives_count"] < 2 or not case["context_present"] or not case["rejection_allowed"]): fail(f"{case['id']}: unsafe approval")
        if case["disposition"] == "approved" and not case["approved_scope"]: fail(f"{case['id']}: approval has no scope")
    print(f"AWG-AUTHORITY-PASS: {len(seen)} dispositions")
    return 0
if __name__ == "__main__": raise SystemExit(main())
