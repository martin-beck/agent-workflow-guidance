import subprocess, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_openhands_mapping.py"

class OpenHandsMappingTests(unittest.TestCase):
    def test_mapping_passes(self):
        result = subprocess.run([sys.executable, str(CHECKER), str(ROOT / "examples/openhands-mapping.json")], cwd=ROOT, check=False, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_runtime_claim_fails(self):
        result = subprocess.run([sys.executable, str(CHECKER), str(ROOT / "fixtures/broken/invalid-openhands-mapping.json")], cwd=ROOT, check=False, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)

if __name__ == "__main__":
    unittest.main()
