#!/usr/bin/env python3
"""Check that oracle packets preserve informed disagreement."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

def fail(message: str) -> None: raise SystemExit(f"AWG-RUBBER-STAMP-FAIL: {message}")

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("cases", type=Path); args = parser.parse_args()
    try: value: Any = json.loads(args.cases.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error: fail(f"cannot read cases: {error}")
    if not isinstance(value, dict) or value.get("schema_version") != 1 or not isinstance(value.get("cases"), list) or not value["cases"]: fail("cases are incomplete")
    dispositions = {"approve", "reject", "clarify"}; seen = set()
    required = {"id", "material_alternatives", "material_alternatives_disclosed", "evidence_gaps", "framing", "rejection_affordance", "disposition", "authority_context"}
    for case in value["cases"]:
        if not isinstance(case, dict) or not required <= set(case): fail("packet fields are incomplete")
        if not isinstance(case["material_alternatives"], list) or len(case["material_alternatives"]) < 2: fail("at least two material alternatives must be exposed")
        if case["framing"] not in {"neutral", "explicitly-contested"}: fail("framing must expose a neutral or contested presentation")
        if not isinstance(case["evidence_gaps"], list) or not isinstance(case["rejection_affordance"], bool) or not case["rejection_affordance"]: fail("evidence gaps and rejection affordance are required")
        if case["disposition"] not in dispositions: fail("disposition must support approve, reject, or clarify")
        if not isinstance(case["authority_context"], str) or not case["authority_context"]: fail("authority context is required")
        if not case["material_alternatives_disclosed"]: fail("material alternatives cannot be hidden")
        if case["disposition"] == "approve" and case["evidence_gaps"]: fail("approval cannot silently suppress evidence gaps")
        seen.add(case["disposition"])
    if seen != dispositions: fail("approve, reject, and clarify dispositions are all required")
    print(f"AWG-RUBBER-STAMP-PASS: {len(value['cases'])} packets preserve alternatives and disagreement")
    return 0

if __name__ == "__main__": raise SystemExit(main())
