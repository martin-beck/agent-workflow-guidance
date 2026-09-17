#!/usr/bin/env python3
"""Check expiry, scope, provenance, and revalidation of reusable guidance."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

def fail(message: str) -> None: raise SystemExit(f"AWG-GUIDANCE-FAIL: {message}")

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("cases", type=Path); args = parser.parse_args()
    try: value: Any = json.loads(args.cases.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error: fail(f"cannot read cases: {error}")
    if not isinstance(value, dict) or value.get("schema_version") != 1 or not isinstance(value.get("cases"), list) or not value["cases"]: fail("lifecycle cases are incomplete")
    statuses = {"reusable", "expired", "invalidated", "revalidated"}
    seen = set()
    for case in value["cases"]:
        required = {"id", "scope", "repository_revision", "status", "authorization", "counterexample", "revalidated_from"}
        if not isinstance(case, dict) or not required <= set(case) or not isinstance(case["scope"], str) or not case["scope"]: fail("scope and provenance are required")
        revision = case["repository_revision"]
        if not isinstance(revision, str) or len(revision) != 40 or any(c not in "0123456789abcdef" for c in revision): fail("repository revision is not exact")
        if case["status"] not in statuses or case["authorization"] not in {"allowed", "blocked"}: fail("lifecycle status is invalid")
        if case["status"] in {"expired", "invalidated"} and case["authorization"] != "blocked": fail("stale or invalidated guidance must be blocked")
        if case["status"] == "revalidated" and (case["authorization"] != "allowed" or not isinstance(case["revalidated_from"], str) or not case["revalidated_from"]): fail("revalidation must bind a new allowed record to its predecessor")
        if case["counterexample"] and case["authorization"] != "blocked": fail("counterexamples invalidate authorization")
        seen.add(case["status"])
    if not {"reusable", "expired", "invalidated", "revalidated"} <= seen: fail("active, stale, changed-context, and revalidated cases are required")
    print(f"AWG-GUIDANCE-PASS: {len(value['cases'])} cases enforce scoped reusable guidance")
    return 0

if __name__ == "__main__": raise SystemExit(main())
