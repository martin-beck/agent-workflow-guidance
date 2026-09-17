#!/usr/bin/env python3
"""Validate an evidence-complete, dated public-project comparison snapshot."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any
EXPECTED = {"LangGraph", "AutoGen", "Microsoft Agent Framework", "OpenHands", "SWE-agent"}
def fail(message: str) -> None: raise SystemExit(f"AWG-PUBLIC-MATRIX-FAIL: {message}")
def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("matrix", type=Path); args = parser.parse_args()
    try: value: Any = json.loads(args.matrix.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error: fail(f"cannot read matrix: {error}")
    if not isinstance(value, dict) or value.get("schema_version") != 1 or not isinstance(value.get("observed_at"), str) or not isinstance(value.get("candidates"), list): fail("invalid matrix identity")
    if {row.get("name") for row in value["candidates"] if isinstance(row, dict)} != EXPECTED: fail("required candidate set is incomplete")
    seen: set[str] = set()
    fields = ("name", "repository", "default_branch", "revision", "license", "maintenance", "persistence", "human_intervention", "awq_boundary", "evidence")
    for row in value["candidates"]:
        if not isinstance(row, dict) or any(field not in row for field in fields): fail("candidate evidence fields are incomplete")
        if row["name"] in seen or not re.fullmatch(r"[0-9a-f]{40}", row["revision"]): fail("candidate identity or exact revision is invalid")
        seen.add(row["name"])
        if not isinstance(row["license"], str) or not row["license"] or not all(isinstance(row[key], str) and row[key] for key in ("maintenance", "persistence", "human_intervention", "awq_boundary")): fail(f"{row['name']}: evidence text is incomplete")
        if "not established" not in row["persistence"].lower() and "not established" not in row["human_intervention"].lower() and "compar" not in row["awq_boundary"].lower(): fail(f"{row['name']}: missing explicit evidence boundary")
        if not isinstance(row["evidence"], list) or len(row["evidence"]) < 2 or not all(isinstance(url, str) and url.startswith("https://") for url in row["evidence"]): fail(f"{row['name']}: evidence links are incomplete")
    print(f"AWG-PUBLIC-MATRIX-PASS: {len(seen)} candidates at {value['observed_at']}")
    return 0
if __name__ == "__main__": raise SystemExit(main())
