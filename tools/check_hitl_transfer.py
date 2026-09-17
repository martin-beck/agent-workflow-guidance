#!/usr/bin/env python3
"""Check bounded transfer of HITL/RL terminology into AWG."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

def fail(message: str) -> None: raise SystemExit(f"AWG-HITL-FAIL: {message}")

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("terms", type=Path); args = parser.parse_args()
    try: value: Any = json.loads(args.terms.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error: fail(f"cannot read terms: {error}")
    if not isinstance(value, dict) or value.get("schema_version") != 1 or value.get("behavioral_transfer_claim") is not False: fail("transfer must remain bounded and non-equivalence")
    terms = value.get("terms")
    if not isinstance(terms, list) or not terms: fail("terms are missing")
    required = {"term", "source_meaning", "awg_meaning", "disposition", "counterexample"}
    by_name = {}
    for term in terms:
        if not isinstance(term, dict) or not required <= set(term) or not all(isinstance(term[k], str) and term[k] for k in required): fail("term mapping is incomplete")
        if term["disposition"] not in {"transferred", "rejected", "conditional", "bounded"}: fail("unknown disposition")
        if term["counterexample"].lower() in {"none", "n/a"}: fail("every term needs a counterexample")
        by_name[term["term"]] = term
    for name in ("action_correction", "delayed_outcome", "intervention_timing", "confidence"):
        if name not in by_name: fail(f"missing required term: {name}")
    if by_name["delayed_outcome"]["disposition"] != "rejected" or by_name["confidence"]["disposition"] == "transferred": fail("delayed outcomes or confidence have unsafe transfer")
    if "reward" in by_name["confidence"]["awg_meaning"].lower() or "approval" in by_name["confidence"]["awg_meaning"].lower(): fail("confidence must remain distinct from reward and approval")
    print(f"AWG-HITL-PASS: {len(terms)} terms have bounded transfer dispositions")
    return 0

if __name__ == "__main__": raise SystemExit(main())
