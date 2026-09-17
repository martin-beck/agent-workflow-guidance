#!/usr/bin/env python3
"""Check that AWG confidence calibration remains multidimensional."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

def fail(message: str) -> None: raise SystemExit(f"AWG-CONFIDENCE-FAIL: {message}")

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("contract", type=Path); args = parser.parse_args()
    try: value: Any = json.loads(args.contract.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error: fail(f"cannot read contract: {error}")
    if not isinstance(value, dict) or value.get("schema_version") != 1: fail("contract fields are incomplete")
    if value.get("thresholds_status") != "unvalidated": fail("initial thresholds must remain explicitly unvalidated")
    if value.get("collapsed_score") is not None: fail("collapsed score cannot replace dimensions")
    dimensions = value.get("dimensions")
    expected = {"applicability", "outcome", "downstream_impact"}
    if not isinstance(dimensions, list) or {d.get("name") for d in dimensions if isinstance(d, dict)} != expected: fail("all three confidence dimensions are required")
    for dimension in dimensions:
        if not isinstance(dimension, dict) or not all(isinstance(dimension.get(k), (int, float)) and 0 <= dimension[k] <= 1 for k in ("predicted", "observed", "mae", "threshold")): fail("dimension calibration fields are invalid")
        if abs(dimension["predicted"] - dimension["observed"]) > dimension["mae"] + 1e-9: fail("reported MAE is inconsistent")
    if len({d["observed"] for d in dimensions}) == 1: fail("a dimension disagreement must remain representable")
    print("AWG-CONFIDENCE-PASS: three dimensions remain separately calibrated and unvalidated")
    return 0

if __name__ == "__main__": raise SystemExit(main())
