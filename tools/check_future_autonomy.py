#!/usr/bin/env python3
"""Check evidence required before scoped oracle-free eligibility."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

def fail(message: str) -> None: raise SystemExit(f"AWG-AUTONOMY-FAIL: {message}")

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("cases", type=Path); args = parser.parse_args()
    try: value: Any = json.loads(args.cases.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error: fail(f"cannot read cases: {error}")
    if not isinstance(value, dict) or value.get("schema_version") != 1 or not isinstance(value.get("cases"), list) or not value["cases"]: fail("cases are incomplete")
    seen = set(); required = {"id", "task_class", "context", "intervention_count", "calibration_evidence", "outcome_evidence", "safety_evidence", "scope_match", "disposition"}
    for case in value["cases"]:
        if not isinstance(case, dict) or not required <= set(case): fail("evidence fields are incomplete")
        if not isinstance(case["intervention_count"], int) or case["intervention_count"] < 0: fail("intervention count is invalid")
        if case["disposition"] not in {"oracle-required", "oracle-free-eligible"}: fail("autonomy disposition is invalid")
        evidence_ready = case["calibration_evidence"] and case["outcome_evidence"] and case["safety_evidence"] and case["scope_match"]
        if case["disposition"] == "oracle-free-eligible" and not evidence_ready: fail("eligibility requires calibration, outcome, safety, and scope evidence")
        if case["disposition"] == "oracle-required" and evidence_ready and case["scope_match"]: fail("complete in-scope evidence should be eligible")
        if case["intervention_count"] == 0 and case["disposition"] == "oracle-free-eligible" and not evidence_ready: fail("low intervention frequency cannot establish eligibility")
        seen.add(case["disposition"])
    if seen != {"oracle-required", "oracle-free-eligible"}: fail("both required and eligible evidence boundaries must be represented")
    print(f"AWG-AUTONOMY-PASS: {len(value['cases'])} cases require scoped outcome and safety evidence")
    return 0

if __name__ == "__main__": raise SystemExit(main())
