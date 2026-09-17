#!/usr/bin/env python3
"""Validate the dependency-free conceptual OpenHands/AWG mapping."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

def fail(message: str) -> None:
    raise SystemExit(f"AWG-OPENHANDS-FAIL: {message}")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mapping", type=Path)
    args = parser.parse_args()
    try:
        value: Any = json.loads(args.mapping.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        fail(f"cannot read mapping: {error}")
    required = ("schema_version", "external_project", "external_repository", "external_revision", "runtime_dependency", "runtime_integration_claim", "privacy_boundary", "mappings")
    if not isinstance(value, dict) or any(key not in value for key in required) or value.get("schema_version") != 1:
        fail("mapping fields are incomplete")
    if value["external_project"] != "OpenHands" or value["external_repository"] != "OpenHands/OpenHands" or not isinstance(value["external_revision"], str) or len(value["external_revision"]) != 40 or any(char not in "0123456789abcdef" for char in value["external_revision"]):
        fail("external identity or exact revision is invalid")
    if value["runtime_dependency"] is not False or value["runtime_integration_claim"] is not False:
        fail("mapping must remain conceptual and dependency-free")
    if not isinstance(value["privacy_boundary"], list) or set(value["privacy_boundary"]) != {"no raw transcript", "no credentials", "no provider call", "synthetic action only"}:
        fail("privacy boundary is incomplete")
    expected = {("planning.tool_action", "ranked_options"), ("sandbox.tool_execution", "bounded_authority"), ("review.approval_pause", "decision_request"), ("conversation.resume", "continuation")}
    actual = {(item.get("external"), item.get("awg")) for item in value["mappings"] if isinstance(item, dict)}
    if actual != expected or not all(isinstance(item.get("invariant"), str) and item["invariant"] for item in value["mappings"]):
        fail("mapping or invariants are incomplete")
    print("AWG-OPENHANDS-PASS: conceptual decision-gate mapping")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
