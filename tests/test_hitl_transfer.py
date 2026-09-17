import subprocess, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_hitl_transfer.py"

class HitlTransferTests(unittest.TestCase):
    def test_terms_pass(self):
        result = subprocess.run([sys.executable, str(CHECKER), str(ROOT / "examples/hitl-transfer-terms.json")], cwd=ROOT, check=False, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unbounded_fixture_fails(self):
        result = subprocess.run([sys.executable, str(CHECKER), str(ROOT / "fixtures/broken/invalid-hitl-transfer-terms.json")], cwd=ROOT, check=False, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)

if __name__ == "__main__": unittest.main()
