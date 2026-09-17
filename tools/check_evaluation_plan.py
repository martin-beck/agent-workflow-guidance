#!/usr/bin/env python3
"""Validate the bounded, offline synthetic AWG evaluation input contract."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

REQUIRED_MEASURES = {"decision_quality", "oracle_effort", "rework", "dependent_task_impact", "calibration_applicability", "calibration_outcome", "calibration_downstream_impact", "inappropriate_autonomy"}
FORBIDDEN = ("transcript", "prompt", "secret", "credential", "password", "token", "http://", "https://")
def fail(message: str) -> None: raise SystemExit(f"AWG-EVALUATION-FAIL: {message}")
def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("plan", type=Path); args = parser.parse_args()
    try: value: Any = json.loads(args.plan.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error: fail(f"cannot read plan: {error}")
    if not isinstance(value, dict) or value.get("schema_version") != 1: fail("invalid plan identity")
    for key in ("plan_id", "specification_ref", "conditions", "measures", "scenarios"):
        if key not in value: fail(f"missing {key}")
    if not isinstance(value["conditions"], list) or set(value["conditions"]) != {"autonomous", "oracle-guided", "independent-batch", "reusable-guidance"}: fail("conditions are incomplete")
    if not isinstance(value["measures"], list) or not REQUIRED_MEASURES.issubset(value["measures"]): fail("required measures are incomplete")
    scenarios = value["scenarios"]
    if not isinstance(scenarios, list) or not 4 <= len(scenarios) <= 24: fail("scenario count must be bounded between 4 and 24")
    seen: set[str] = set()
    for scenario in scenarios:
        if not isinstance(scenario, dict): fail("scenario is not an object")
        required = ("id", "alternatives", "applicability_confidence", "outcome_confidence", "downstream_impact_confidence", "expected_action", "expected_oracle", "dependent_tasks", "expected_rework", "expected_inappropriate_autonomy")
        if any(key not in scenario for key in required): fail("scenario fields are incomplete")
        if scenario["id"] in seen or not isinstance(scenario["id"], str): fail("scenario identifiers must be unique")
        seen.add(scenario["id"])
        if not isinstance(scenario["alternatives"], list) or len(scenario["alternatives"]) < 2: fail("each scenario needs at least two alternatives")
        for key in ("applicability_confidence", "outcome_confidence", "downstream_impact_confidence"):
            if not isinstance(scenario[key], (int, float)) or isinstance(scenario[key], bool) or not 0 <= scenario[key] <= 1: fail(f"{key} must be between 0 and 1")
        if scenario["expected_action"] not in {"autonomous", "oracle-guided", "independent-batch", "reusable-guidance"} or not isinstance(scenario["expected_oracle"], str): fail("invalid expected disposition")
        if not isinstance(scenario["dependent_tasks"], int) or scenario["dependent_tasks"] < 0 or not isinstance(scenario["expected_rework"], int) or scenario["expected_rework"] < 0 or not isinstance(scenario["expected_inappropriate_autonomy"], bool): fail("invalid scenario outcome fields")
    serialized = json.dumps(value, ensure_ascii=False).lower()
    if any(marker in serialized for marker in FORBIDDEN): fail("plan contains forbidden network or private-transcript marker")
    print(f"AWG-EVALUATION-PASS: {value['plan_id']} ({len(scenarios)} scenarios)")
    return 0
if __name__ == "__main__": raise SystemExit(main())
