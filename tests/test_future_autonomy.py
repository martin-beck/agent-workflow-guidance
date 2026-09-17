import subprocess, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_future_autonomy.py"

class FutureAutonomyTests(unittest.TestCase):
    def test_cases_pass(self):
        result = subprocess.run([sys.executable, str(CHECKER), str(ROOT / "examples/future-autonomy-cases.json")], cwd=ROOT, check=False, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_low_intervention_fixture_fails(self):
        result = subprocess.run([sys.executable, str(CHECKER), str(ROOT / "fixtures/broken/invalid-future-autonomy-cases.json")], cwd=ROOT, check=False, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)

if __name__ == "__main__": unittest.main()
