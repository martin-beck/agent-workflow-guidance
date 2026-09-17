import subprocess, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_confidence_calibration.py"

class ConfidenceCalibrationTests(unittest.TestCase):
    def test_contract_passes(self):
        result = subprocess.run([sys.executable, str(CHECKER), str(ROOT / "examples/confidence-calibration-contract.json")], cwd=ROOT, check=False, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_collapsed_fixture_fails(self):
        result = subprocess.run([sys.executable, str(CHECKER), str(ROOT / "fixtures/broken/invalid-confidence-calibration-contract.json")], cwd=ROOT, check=False, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)

if __name__ == "__main__": unittest.main()
