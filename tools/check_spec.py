#!/usr/bin/env python3
"""Offline structural and finite-state checks for AWG specifications."""

import argparse
import json
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(f"AWG-SPEC-FAIL: {message}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    args = parser.parse_args()
    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read JSON: {error}")
    required = (
        "schema_version", "spec_id", "version", "decision_class", "objective",
        "scope", "assumptions", "state_variables", "transitions", "invariants",
        "acceptance_predicates", "formalization",
    )
    missing = [key for key in required if key not in spec]
    if missing:
        fail(f"missing fields: {', '.join(missing)}")
    if spec["schema_version"] != "0.2":
        fail("unsupported schema_version")
    if spec["decision_class"] not in {"design", "conceptual", "operational"}:
        fail("invalid decision_class")
    for key in ("scope", "state_variables", "transitions", "invariants", "acceptance_predicates"):
        if not isinstance(spec[key], list) or not spec[key] or not all(isinstance(item, str) and item for item in spec[key]):
            fail(f"{key} must be a non-empty list of strings")
    formal = spec["formalization"]
    for key in ("method", "model_ref", "checker", "command", "scope", "expected_result"):
        if key not in formal:
            fail(f"formalization missing {key}")
    if not isinstance(formal["command"], list) or not formal["command"] or not all(isinstance(item, str) and item for item in formal["command"]):
        fail("formalization.command must be a non-empty argv array")
    if formal["method"] == "state-machine":
        model = formal.get("model")
        if not isinstance(model, dict):
            fail("state-machine formalization requires model")
        states = model.get("states")
        if not isinstance(states, list) or not states or not all(isinstance(state, str) and state for state in states):
            fail("state-machine model.states must be non-empty")
        if model.get("initial") not in states:
            fail("state-machine initial state is not declared")
        for edge in model.get("transitions", []):
            if not isinstance(edge, dict) or edge.get("from") not in states or edge.get("to") not in states:
                fail("state-machine transition references an unknown state")
        for edge in model.get("forbidden_transitions", []):
            if not isinstance(edge, dict) or edge.get("from") not in states or edge.get("to") not in states:
                fail("forbidden transition references an unknown state")
    print(f"AWG-SPEC-PASS: {spec['spec_id']} v{spec['version']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
