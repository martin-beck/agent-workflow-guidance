#!/usr/bin/env python3
"""Check deterministic expected-regret clarification cases offline."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any
FORBIDDEN = ("transcript", "prompt", "secret", "credential", "password", "token", "http://", "https://")
def fail(message: str) -> None: raise SystemExit(f"AWG-CLARIFICATION-FAIL: {message}")
def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("cases", type=Path); args = parser.parse_args()
    try: value: Any = json.loads(args.cases.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error: fail(f"cannot read cases: {error}")
    if not isinstance(value, dict) or value.get("schema_version") != 1 or not isinstance(value.get("cases"), list) or not value["cases"]: fail("invalid case set")
    seen: set[str] = set()
    for case in value["cases"]:
        if not isinstance(case, dict): fail("case is not an object")
        fields = ("id", "alternatives", "applicability_confidence", "ambiguity", "downstream_impact", "harm_if_wrong", "intervention_cost", "material_ambiguity", "ambiguity_resolved", "question_scope", "expected_decision")
        if any(field not in case for field in fields): fail("case fields are incomplete")
        if not isinstance(case["id"], str) or case["id"] in seen: fail("case identifiers must be unique")
        seen.add(case["id"])
        if not isinstance(case["alternatives"], list) or len(case["alternatives"]) < 2: fail("each case needs at least two alternatives")
        for field in ("applicability_confidence", "ambiguity", "downstream_impact", "harm_if_wrong"):
            if not isinstance(case[field], (int, float)) or isinstance(case[field], bool) or not 0 <= case[field] <= 1: fail(f"{field} must be between 0 and 1")
        if not isinstance(case["intervention_cost"], (int, float)) or isinstance(case["intervention_cost"], bool) or case["intervention_cost"] < 0: fail("intervention_cost must be non-negative")
        if not isinstance(case["material_ambiguity"], bool) or not isinstance(case["ambiguity_resolved"], bool) or not isinstance(case["question_scope"], str) or not 1 <= len(case["question_scope"]) <= 160: fail("invalid ambiguity or question scope")
        expected = "clarify" if (case["material_ambiguity"] and not case["ambiguity_resolved"]) or case["ambiguity"] * case["downstream_impact"] * case["harm_if_wrong"] > case["intervention_cost"] else "act"
        if case["expected_decision"] != expected: fail(f"{case['id']}: expected decision does not match deterministic gate")
    if any(marker in json.dumps(value, ensure_ascii=False).lower() for marker in FORBIDDEN): fail("case set contains forbidden network or private marker")
    print(f"AWG-CLARIFICATION-PASS: {len(seen)} cases")
    return 0
if __name__ == "__main__": raise SystemExit(main())
