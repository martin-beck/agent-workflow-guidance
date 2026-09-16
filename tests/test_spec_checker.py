#!/usr/bin/env python3
"""Negative and positive tests for specification/result binding."""

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_spec.py"


class SpecificationCheckerTests(unittest.TestCase):
    def run_checker(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(CHECKER), *args], cwd=ROOT, check=False, capture_output=True, text=True)

    def test_positive_bound_result(self) -> None:
        result = self.run_checker("specifications/offline-contracts.json", "--result", "specifications/offline-contracts.check.json")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_spec_fails_closed(self) -> None:
        result = self.run_checker("fixtures/broken/invalid-spec.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("AWG-SPEC-FAIL", result.stderr)

    def test_stale_result_fails_closed(self) -> None:
        result = self.run_checker("specifications/offline-contracts.json", "--result", "fixtures/broken/invalid-formal-check.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("AWG-SPEC-FAIL", result.stderr)


if __name__ == "__main__":
    unittest.main()
