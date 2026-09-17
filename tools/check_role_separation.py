#!/usr/bin/env python3
"""Check that approval, implementation, quality, and review remain separate."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

def fail(message: str) -> None: raise SystemExit(f"AWG-ROLE-FAIL: {message}")

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("cases", type=Path); args = parser.parse_args()
    try: value: Any = json.loads(args.cases.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error: fail(f"cannot read cases: {error}")
    if not isinstance(value, dict) or value.get("schema_version") != 1 or value.get("synthetic_only") is not True: fail("cases must be synthetic")
    cases = value.get("cases")
    if not isinstance(cases, list) or not cases: fail("cases are missing")
    kinds = {"recommendation", "oracle_decision", "implementation", "quality_evidence", "independent_review"}
    saw_failed_quality = False
    for case in cases:
        records = case.get("records") if isinstance(case, dict) else None
        if not isinstance(records, list): fail("records are missing")
        by_kind = {r.get("kind"): r for r in records if isinstance(r, dict)}
        if set(by_kind) != kinds: fail("all five evidence roles are required")
        for record in records:
            if not all(isinstance(record.get(k), (str, type(None))) for k in ("id", "predecessor", "status")): fail("record fields are invalid")
        ordered = [by_kind[k] for k in ("recommendation", "oracle_decision", "implementation", "quality_evidence", "independent_review")]
        for previous, current in zip(ordered, ordered[1:]):
            if current["predecessor"] != previous["id"]: fail("predecessor binding is broken")
        if by_kind["oracle_decision"]["status"] != "approved": fail("oracle decision must be explicit")
        quality = by_kind["quality_evidence"]["status"]
        review = by_kind["independent_review"]["status"]
        if quality == "fail":
            saw_failed_quality = True
            if review != "blocked": fail("failed quality evidence must block review")
        elif quality == "pass" and review == "pass": pass
        else: fail("quality evidence status is invalid")
    if not saw_failed_quality: fail("must represent a plausible but incorrect implementation")
    print(f"AWG-ROLE-PASS: {len(cases)} cases preserve approval, implementation, quality, and review separation")
    return 0

if __name__ == "__main__": raise SystemExit(main())
