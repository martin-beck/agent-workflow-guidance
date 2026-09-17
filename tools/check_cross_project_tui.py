#!/usr/bin/env python3
"""Offline, fail-closed composition checks for the public TUI contracts."""
import argparse
import json


def fail(message):
    raise SystemExit("AWG-TUI-CROSS-FAIL: " + message)


def check(value):
    if value.get("contract_versions") != {"coordinator": "AR-0029/v1", "awq": "AR-0065/v1"}:
        fail("exact public contract versions required")
    if value.get("queries") != 1 or len(value.get("discussion_points", [])) < 2:
        fail("independent discussion points must be batched")
    seen = set()
    for point in value["discussion_points"]:
        identity = point.get("id")
        if not identity or identity in seen:
            fail("duplicate or missing discussion-point identity")
        seen.add(identity)
        if len(point.get("proposals", [])) < 2 or not point.get("implications"):
            fail("ranked proposals and implications are required")
        response = point.get("response", {})
        if response.get("point_id") != identity:
            fail("cross-point authorization")
        added = response.get("user_proposal")
        if added is not None and not added.get("evaluated"):
            fail("user proposal must be evaluated before selection")
        if not response.get("selected"):
            fail("each point needs a selected proposal")
    if value.get("safe_exit", {}).get("saved") is not True:
        fail("safe exit must persist the complete packet")
    if not value.get("future_requests") or any(not item.get("ar_ref") for item in value["future_requests"]):
        fail("future requests must map to ARs")
    hostile = value.get("hostile_trace", {})
    if not all(hostile.get(key) is True for key in ("skipped_gate_rejected", "stale_revision_rejected", "dropped_request_rejected")):
        fail("hostile traces must be rejected")
    print("AWG-TUI-CROSS-PASS: " + str(value.get("session_id")))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture")
    args = parser.parse_args()
    with open(args.fixture, encoding="utf-8") as stream:
        check(json.load(stream))


if __name__ == "__main__":
    main()
