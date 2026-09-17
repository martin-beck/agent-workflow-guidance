#!/usr/bin/env python3
"""Validate separate AWG confidence calibration cases offline."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any
DIMENSIONS = ("applicability", "outcome", "downstream_impact")
def fail(message: str) -> None: raise SystemExit(f"AWG-CALIBRATION-FAIL: {message}")
def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("cases", type=Path); args = parser.parse_args()
    try: value: Any = json.loads(args.cases.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error: fail(f"cannot read cases: {error}")
    if not isinstance(value, dict) or value.get("schema_version") != 1 or not isinstance(value.get("thresholds"), dict) or not isinstance(value.get("cases"), list) or not value["cases"]: fail("invalid calibration set")
    threshold = value["thresholds"].get("downstream_escalation_confidence"); max_error = value["thresholds"].get("maximum_dimension_mae")
    if not isinstance(threshold, (int, float)) or not 0 <= threshold <= 1 or not isinstance(max_error, (int, float)) or not 0 <= max_error <= 1: fail("invalid calibration thresholds")
    seen: set[str] = set(); errors = {dimension: [] for dimension in DIMENSIONS}
    for case in value["cases"]:
        if not isinstance(case, dict) or not isinstance(case.get("id"), str) or case["id"] in seen: fail("case identifiers must be unique")
        seen.add(case["id"])
        for dimension in DIMENSIONS:
            confidence, label = case.get(f"{dimension}_confidence"), case.get(f"{dimension}_label")
            if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1 or label not in {0, 1}: fail(f"{case['id']}: missing separate {dimension} confidence/label")
            errors[dimension].append(abs(confidence - label))
        expected = case["downstream_impact_confidence"] < threshold
        if case.get("expected_escalation") is not expected: fail(f"{case['id']}: escalation predicate is inconsistent")
    means = {dimension: sum(values) / len(values) for dimension, values in errors.items()}
    if any(mean > max_error for mean in means.values()): fail("dimension MAE exceeds declared fixture threshold")
    if not all(f"{dimension}_confidence" in value["cases"][0] for dimension in DIMENSIONS): fail("collapsed confidence is not permitted")
    print(f"AWG-CALIBRATION-PASS: {len(seen)} cases; separate MAE " + ", ".join(f"{key}={value:.3f}" for key, value in means.items()))
    return 0
if __name__ == "__main__": raise SystemExit(main())
