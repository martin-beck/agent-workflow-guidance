#!/usr/bin/env python3
"""Validate the optional dependency-free LangGraph/AWG mapping."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any
def fail(message: str) -> None: raise SystemExit(f"AWG-LANGGRAPH-FAIL: {message}")
def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("mapping", type=Path); args = parser.parse_args()
    try: value: Any = json.loads(args.mapping.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error: fail(f"cannot read mapping: {error}")
    required = ("schema_version", "external_project", "external_repository", "external_revision", "runtime_dependency", "runtime_integration_claim", "privacy_boundary", "mappings")
    if not isinstance(value, dict) or any(key not in value for key in required) or value.get("schema_version") != 1: fail("mapping fields are incomplete")
    if value["external_project"] != "LangGraph" or value["external_repository"] != "langchain-ai/langgraph" or not isinstance(value["external_revision"], str) or len(value["external_revision"]) != 40 or any(char not in "0123456789abcdef" for char in value["external_revision"]): fail("external identity or exact revision is invalid")
    if value["runtime_dependency"] is not False or value["runtime_integration_claim"] is not False: fail("mapping must remain conceptual and dependency-free")
    if not isinstance(value["privacy_boundary"], list) or set(value["privacy_boundary"]) != {"no raw transcript", "no credentials", "no provider call", "synthetic checkpoint only"}: fail("privacy boundary is incomplete")
    expected = {("checkpoint.thread_id", "execution_id"), ("interrupt.payload", "decision_request"), ("human.response", "oracle_decision"), ("resume.input", "continuation")}
    actual = {(item.get("external"), item.get("awg")) for item in value["mappings"] if isinstance(item, dict)}
    if actual != expected or not all(isinstance(item.get("invariant"), str) and item["invariant"] for item in value["mappings"]): fail("mapping or invariants are incomplete")
    print("AWG-LANGGRAPH-PASS: conceptual interrupt/checkpoint mapping")
    return 0
if __name__ == "__main__": raise SystemExit(main())
