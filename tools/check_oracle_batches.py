#!/usr/bin/env python3
"""Check item-level authorization in batched oracle packets."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

def fail(message: str) -> None: raise SystemExit(f"AWG-BATCH-FAIL: {message}")

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("batches", type=Path); args = parser.parse_args()
    try: value: Any = json.loads(args.batches.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error: fail(f"cannot read batches: {error}")
    if not isinstance(value, dict) or value.get("schema_version") != 1 or value.get("workload_claim") is not False: fail("batch evidence must not claim workload improvement")
    batches = value.get("batches")
    if not isinstance(batches, list) or not batches: fail("batches are missing")
    relations = {"single", "independent", "coupled"}
    seen = set()
    for batch in batches:
        if not isinstance(batch, dict) or batch.get("relation") not in relations: fail("batch relation is invalid")
        items, authorized, unresolved = batch.get("items"), batch.get("authorized"), batch.get("unresolved")
        if not isinstance(items, list) or not items or len(set(items)) != len(items) or not isinstance(authorized, list) or not isinstance(unresolved, list): fail("item identities are invalid")
        if set(authorized) & set(unresolved) or set(authorized) | set(unresolved) != set(items): fail("authorized and unresolved sets do not partition items")
        responded = set()
        for response in batch.get("responses", []):
            if not isinstance(response, dict) or not isinstance(response.get("item_ids"), list): fail("response item binding is invalid")
            response_items = set(response["item_ids"])
            if not response_items <= set(items): fail("response authorizes an item outside its packet")
            if batch["relation"] == "independent" and len(response_items) != 1: fail("independent response must name one item")
            if batch["relation"] == "single" and response_items != {items[0]}: fail("single response binding is invalid")
            responded |= response_items
        if responded != set(authorized): fail("authorization is not the union of response item sets")
        if batch["relation"] == "coupled" and set(authorized) not in (set(), set(items)): fail("coupled items must authorize together")
        seen.add(batch["relation"])
    if seen != relations: fail("single, independent, and coupled examples are all required")
    print(f"AWG-BATCH-PASS: {len(batches)} packets preserve item-level authorization")
    return 0

if __name__ == "__main__": raise SystemExit(main())
