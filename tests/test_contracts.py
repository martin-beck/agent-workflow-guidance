#!/usr/bin/env python3
"""Offline tests for the dependency-free AWG contract checker."""

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_contracts.py"


class ContractCheckerTests(unittest.TestCase):
    def run_checker(self, path: Path, kind: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), str(path), "--kind", kind],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_positive_request(self) -> None:
        result = self.run_checker(ROOT / "examples" / "decision-request.json", "request")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_negative_request(self) -> None:
        result = self.run_checker(ROOT / "fixtures" / "broken" / "invalid-request.json", "request")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("AWG-CONTRACT-FAIL", result.stderr)

    def test_positive_record(self) -> None:
        result = self.run_checker(ROOT / "examples" / "decision-record.json", "record")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_negative_record(self) -> None:
        result = self.run_checker(ROOT / "fixtures" / "broken" / "invalid-record.json", "record")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("AWG-CONTRACT-FAIL", result.stderr)

    def test_checker_is_offline_and_json_is_canonical(self) -> None:
        document = json.loads((ROOT / "examples" / "decision-request.json").read_text(encoding="utf-8"))
        self.assertEqual(document["schema_version"], "0.2")
        self.assertEqual(self.run_checker(ROOT / "examples" / "decision-request.json", "request").returncode, 0)


if __name__ == "__main__":
    unittest.main()
