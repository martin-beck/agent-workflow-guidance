#!/usr/bin/env python3
"""Check that benchmark scores cannot stand in for governance evidence."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

def fail(message: str) -> None:
    raise SystemExit(f"AWG-SWE-GOVERNANCE-FAIL: {message}")

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("cases", type=Path); args = parser.parse_args()
    try: value: Any = json.loads(args.cases.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error: fail(f"cannot read cases: {error}")
    if not isinstance(value, dict) or value.get("schema_version") != 1 or value.get("production_safety_claim") is not False:
        fail("cases must be synthetic and must not claim production safety")
    revision = value.get("external_revision")
    if not isinstance(revision, str) or len(revision) != 40 or any(char not in "0123456789abcdef" for char in revision): fail("external revision is not exact")
    cases = value.get("cases")
    if not isinstance(cases, list) or not cases: fail("cases are missing")
    required = {"id", "task_score", "intervention_cost", "rework_count", "dependent_impact", "decision_quality", "governance_status"}
    for case in cases:
        if not isinstance(case, dict) or not required <= set(case): fail("each case needs independent outcome and governance fields")
        if not isinstance(case["task_score"], (int, float)) or not 0 <= case["task_score"] <= 1: fail("task score is invalid")
        if not isinstance(case["intervention_cost"], dict) or not isinstance(case["rework_count"], int) or case["rework_count"] < 0: fail("intervention or rework evidence is invalid")
        quality = case["decision_quality"]
        if not isinstance(quality, dict) or not all(isinstance(quality.get(k), (int, float)) and 0 <= quality[k] <= 1 for k in ("applicability", "downstream_risk")): fail("decision-quality evidence is invalid")
        if case["governance_status"] not in ("pass", "fail"): fail("governance status is invalid")
        unsafe = case["rework_count"] > 0 or case["dependent_impact"] not in ("none", "contained") or quality["downstream_risk"] > 0.5
        if unsafe and case["governance_status"] == "pass": fail("unsafe governance evidence cannot pass because task score succeeded")
    if not any(case["task_score"] == 1.0 and case["governance_status"] == "fail" for case in cases): fail("fixture must demonstrate score/governance separation")
    print(f"AWG-SWE-GOVERNANCE-PASS: {len(cases)} synthetic cases keep score and governance separate")
    return 0

if __name__ == "__main__": raise SystemExit(main())
