#!/usr/bin/env python3
"""Validate revision-bound mixed-initiative feedback packets offline."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any
def fail(message: str) -> None: raise SystemExit(f"AWG-MIXED-INITIATIVE-FAIL: {message}")
def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("cases", type=Path); args = parser.parse_args()
    try: value: Any = json.loads(args.cases.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error: fail(f"cannot read cases: {error}")
    if not isinstance(value, dict) or value.get("schema_version") != 1 or not isinstance(value.get("cases"), list) or not value["cases"]: fail("invalid case set")
    seen: set[str] = set()
    for case in value["cases"]:
        fields = ("id", "packet_id", "recommendation_revision", "correction_revision", "superseded_revision", "confirmed_revision", "paused_revision", "resumed_revision", "context_id", "expected")
        if not isinstance(case, dict) or any(field not in case for field in fields): fail("case fields are incomplete")
        if not isinstance(case["id"], str) or case["id"] in seen or not isinstance(case["packet_id"], str) or not isinstance(case["context_id"], str) or case["expected"] != "pass": fail("case identity or expected status is invalid")
        seen.add(case["id"])
        rec = case["recommendation_revision"]
        if not isinstance(rec, int) or rec < 1: fail(f"{case['id']}: invalid recommendation revision")
        correction = case["correction_revision"]
        if correction is None:
            if case["superseded_revision"] is not None or case["confirmed_revision"] != rec: fail(f"{case['id']}: confirmation does not bind recommendation")
            effective = rec
        else:
            if not isinstance(correction, int) or correction <= rec or case["superseded_revision"] != rec or case["confirmed_revision"] != correction: fail(f"{case['id']}: correction or confirmation revision is stale")
            effective = correction
        if case["paused_revision"] != effective or case["resumed_revision"] != effective: fail(f"{case['id']}: pause/resume revision is not preserved")
    print(f"AWG-MIXED-INITIATIVE-PASS: {len(seen)} packets")
    return 0
if __name__ == "__main__": raise SystemExit(main())
