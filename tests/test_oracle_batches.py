import subprocess, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_oracle_batches.py"

class OracleBatchTests(unittest.TestCase):
    def test_batches_pass(self):
        result = subprocess.run([sys.executable, str(CHECKER), str(ROOT / "examples/oracle-batches.json")], cwd=ROOT, check=False, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_cross_item_authorization_fails(self):
        result = subprocess.run([sys.executable, str(CHECKER), str(ROOT / "fixtures/broken/invalid-oracle-batches.json")], cwd=ROOT, check=False, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)

if __name__ == "__main__": unittest.main()
