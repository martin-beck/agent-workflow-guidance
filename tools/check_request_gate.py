#!/usr/bin/env python3
"""Enforce the AWG formal gate before oracle presentation or implementation."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from check_spec import check_spec


def fail(message: str) -> None:
    raise SystemExit(f"AWG-GATE-FAIL: {message}")


def canonical(value: Any) -> bytes:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", type=Path)
    parser.add_argument("--phase", choices=("oracle", "implementation"), required=True)
    parser.add_argument("--task-revision", type=int)
    args = parser.parse_args()
    try:
        request = json.loads(args.request.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        fail(f"cannot read request: {error}")
    if not isinstance(request, dict):
        fail("request root must be an object")
    context = request.get("context")
    spec = request.get("specification")
    result = request.get("formal_check")
    if not isinstance(context, dict) or not isinstance(spec, dict) or not isinstance(result, dict):
        fail("request context, specification, and formal_check are required")
    check_spec(spec, args.request)
    if result.get("status") != "pass":
        fail("formal check is not pass")
    if result.get("spec_id") != spec.get("spec_id") or result.get("spec_version") != spec.get("version"):
        fail("formal check identity is stale")
    expected_digest = "sha256:" + hashlib.sha256(canonical(spec)).hexdigest()
    if result.get("artifact_digest") != expected_digest:
        fail("embedded specification digest is stale")
    if result.get("task_revision") != context.get("task_revision"):
        fail("formal check task revision is stale")
    if args.phase == "implementation" and args.task_revision != context.get("task_revision"):
        fail("implementation task revision differs from checked request")
    print(f"AWG-GATE-PASS: {request.get('request_id')} ({args.phase})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
