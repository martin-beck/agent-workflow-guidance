#!/usr/bin/env python3
"""Offline, fail-closed validation for AWG specifications and check results."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from typing import Any


def fail(message: str) -> None:
    raise SystemExit(f"AWG-SPEC-FAIL: {message}")


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        fail(f"cannot read {label}: {error}")
    if not isinstance(value, dict):
        fail(f"{label} root must be an object")
    return value


def nonempty_strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item for item in value)


def check_spec(spec: dict[str, Any], path: Path) -> None:
    required = (
        "schema_version", "spec_id", "version", "decision_class", "objective",
        "scope", "assumptions", "state_variables", "transitions", "invariants",
        "acceptance_predicates", "formalization",
    )
    missing = [key for key in required if key not in spec]
    if missing:
        fail(f"missing specification fields: {', '.join(missing)}")
    if spec["schema_version"] != "0.2":
        fail("unsupported schema_version")
    if not isinstance(spec["spec_id"], str) or re.fullmatch(r"AWG-SPEC-[A-Z0-9-]+", spec["spec_id"]) is None:
        fail("invalid spec_id")
    if not isinstance(spec["version"], int) or isinstance(spec["version"], bool) or spec["version"] < 1:
        fail("version must be a positive integer")
    if spec["decision_class"] not in {"design", "conceptual", "operational"}:
        fail("invalid decision_class")
    for key in ("scope", "state_variables", "transitions", "invariants", "acceptance_predicates"):
        if not nonempty_strings(spec[key]):
            fail(f"{key} must be a non-empty list of strings")
    formal = spec["formalization"]
    if not isinstance(formal, dict):
        fail("formalization must be an object")
    for key in ("method", "model_ref", "checker", "command", "scope", "expected_result"):
        if key not in formal:
            fail(f"formalization missing {key}")
    if formal["method"] not in {"json-schema", "state-machine", "tlaplus", "smtlib", "alloy"}:
        fail("unsupported formalization method")
    if not all(isinstance(formal[key], str) and formal[key] for key in ("model_ref", "checker", "scope")):
        fail("formalization model_ref, checker, and scope must be non-empty strings")
    if not isinstance(formal["command"], list) or not formal["command"] or not all(isinstance(item, str) and item for item in formal["command"]):
        fail("formalization.command must be a non-empty argv array")
    if formal["expected_result"] not in {"pass", "sat", "unsat", "invariants-hold"}:
        fail("unsupported formalization expected_result")
    timeout = formal.get("timeout_seconds")
    if not isinstance(timeout, int) or isinstance(timeout, bool) or not 1 <= timeout <= 86400:
        fail("formalization.timeout_seconds must be between 1 and 86400")
    if formal["method"] == "state-machine":
        model = formal.get("model")
        if not isinstance(model, dict):
            fail("state-machine formalization requires model")
        states = model.get("states")
        if not nonempty_strings(states) or len(set(states)) != len(states):
            fail("state-machine model.states must be non-empty and unique")
        if model.get("initial") not in states:
            fail("state-machine initial state is not declared")
        for edge_key in ("transitions", "forbidden_transitions"):
            edges = model.get(edge_key)
            if not isinstance(edges, list):
                fail(f"state-machine model.{edge_key} must be a list")
            for edge in edges:
                if not isinstance(edge, dict) or edge.get("from") not in states or edge.get("to") not in states:
                    fail(f"{edge_key} references an unknown state")
    digest = spec.get("artifact_digest")
    if digest is not None:
        expected = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != expected:
            fail(f"artifact_digest does not match {path}")


def check_result(result: dict[str, Any], spec: dict[str, Any], spec_path: Path) -> None:
    required = ("schema_version", "spec_id", "spec_version", "artifact_digest", "method", "checker", "status", "properties_checked", "checked_at", "evidence_digest")
    missing = [key for key in required if key not in result]
    if missing:
        fail(f"missing formal-check fields: {', '.join(missing)}")
    if result["schema_version"] != "0.2":
        fail("unsupported formal-check schema_version")
    if result["spec_id"] != spec["spec_id"] or result["spec_version"] != spec["version"]:
        fail("formal-check identity does not match specification")
    expected_digest = "sha256:" + hashlib.sha256(spec_path.read_bytes()).hexdigest()
    if result["artifact_digest"] != expected_digest:
        fail("formal-check artifact_digest is stale or mismatched")
    if result["method"] != spec["formalization"]["method"]:
        fail("formal-check method does not match specification")
    if not isinstance(result["checker"], str) or not result["checker"]:
        fail("formal-check checker must be non-empty")
    if result["status"] != "pass":
        fail("formal-check status is not pass")
    if not nonempty_strings(result["properties_checked"]):
        fail("formal-check properties_checked must be non-empty")
    for field in ("artifact_digest", "evidence_digest"):
        if re.fullmatch(r"sha256:[0-9a-f]{64}", result[field]) is None:
            fail(f"invalid formal-check {field}")
    if not isinstance(result["checked_at"], str):
        fail("formal-check checked_at must be an ISO date-time")
    try:
        checked_at = dt.datetime.fromisoformat(result["checked_at"].replace("Z", "+00:00"))
    except ValueError:
        fail("formal-check checked_at is not an ISO date-time")
    if checked_at.tzinfo is None:
        fail("formal-check checked_at must include a timezone")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("--result", type=Path, help="formal-check result to bind to this specification")
    args = parser.parse_args()
    spec = load_json(args.spec, "specification")
    check_spec(spec, args.spec)
    if args.result:
        check_result(load_json(args.result, "formal-check result"), spec, args.spec)
    suffix = " with bound result" if args.result else ""
    print(f"AWG-SPEC-PASS: {spec['spec_id']} v{spec['version']}{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
