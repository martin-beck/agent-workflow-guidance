#!/usr/bin/env python3
"""Validate AWG JSON contracts with a bounded, dependency-free checker."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any


class ContractError(Exception):
    """Raised for an invalid contract or schema reference."""


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ContractError(f"{path}: cannot read canonical JSON: {error}") from error


def resolve_ref(ref: str, root_schema: dict[str, Any], schema_dir: Path) -> tuple[Any, dict[str, Any]]:
    if ref.startswith("#/"):
        value: Any = root_schema
        for part in ref[2:].split("/"):
            if not isinstance(value, dict) or part not in value:
                raise ContractError(f"unresolvable local schema reference: {ref}")
            value = value[part]
        return value, root_schema
    if "/" in ref or ref.endswith(".json"):
        target_name, _, fragment = ref.partition("#")
        target = load_json(schema_dir / target_name)
        if not isinstance(target, dict):
            raise ContractError(f"schema root is not an object: {target_name}")
        if not fragment:
            return target, target
        value: Any = target
        for part in fragment.lstrip("/").split("/"):
            if not isinstance(value, dict) or part not in value:
                raise ContractError(f"unresolvable schema reference: {ref}")
            value = value[part]
        return value, target
    raise ContractError(f"unsupported schema reference: {ref}")


def validate(value: Any, schema: dict[str, Any], root_schema: dict[str, Any], schema_dir: Path, path: str = "$") -> list[str]:
    if "$ref" in schema:
        resolved, resolved_root = resolve_ref(schema["$ref"], root_schema, schema_dir)
        return validate(value, resolved, resolved_root, schema_dir, path)

    errors: list[str] = []
    expected_type = schema.get("type")
    type_ok = {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }
    if expected_type and not type_ok.get(expected_type, False):
        return [f"{path}: expected {expected_type}"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: expected one of {schema['enum']!r}")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: shorter than minLength")
        pattern = schema.get("pattern")
        if pattern and re.fullmatch(pattern, value) is None:
            errors.append(f"{path}: does not match pattern {pattern!r}")
        if schema.get("format") == "date":
            try:
                dt.date.fromisoformat(value)
            except ValueError:
                errors.append(f"{path}: invalid ISO date")
        if schema.get("format") == "date-time":
            try:
                parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    errors.append(f"{path}: date-time must include a timezone")
            except ValueError:
                errors.append(f"{path}: invalid ISO date-time")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: below minimum")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: above maximum")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: fewer than minItems")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(validate(item, item_schema, root_schema, schema_dir, f"{path}[{index}]"))
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for required in schema.get("required", []):
            if required not in value:
                errors.append(f"{path}: missing required property {required!r}")
        if schema.get("additionalProperties") is False:
            unknown = sorted(set(value) - set(properties))
            errors.extend(f"{path}: unknown property {name!r}" for name in unknown)
        for name, child_schema in properties.items():
            if name in value:
                errors.extend(validate(value[name], child_schema, root_schema, schema_dir, f"{path}.{name}"))
        for name, child_schema in schema.get("$defs", {}).items():
            if not isinstance(child_schema, dict):
                errors.append(f"{path}: invalid $defs entry {name!r}")
    return errors


def schema_for(kind: str, schema_dir: Path) -> tuple[dict[str, Any], Path]:
    names = {
        "request": "decision-request.schema.json",
        "record": "decision-record.schema.json",
        "trigger": "human-decision-trigger.schema.json",
    }
    schema = load_json(schema_dir / names[kind])
    if not isinstance(schema, dict):
        raise ContractError("schema root is not an object")
    return schema, schema_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("contract", type=Path)
    parser.add_argument("--kind", choices=("request", "record", "trigger"), required=True)
    parser.add_argument("--schema-dir", type=Path, default=Path(__file__).parent.parent / "schema")
    args = parser.parse_args()
    try:
        schema, schema_dir = schema_for(args.kind, args.schema_dir)
        errors = validate(load_json(args.contract), schema, schema, schema_dir)
    except ContractError as error:
        print(f"AWG-CONTRACT-FAIL: {error}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"AWG-CONTRACT-FAIL: {error}", file=sys.stderr)
        return 1
    print(f"AWG-CONTRACT-PASS: {args.contract} ({args.kind})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
