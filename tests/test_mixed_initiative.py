import subprocess, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_mixed_initiative.py"
class MixedInitiativeTests(unittest.TestCase):
    def test_valid_packets_pass(self):
        result = subprocess.run([sys.executable,str(CHECKER),str(ROOT / "examples/mixed-initiative-cases.json")],cwd=ROOT,check=False,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
    def test_stale_confirmation_fails(self):
        result = subprocess.run([sys.executable,str(CHECKER),str(ROOT / "fixtures/broken/invalid-mixed-initiative-cases.json")],cwd=ROOT,check=False,capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
if __name__ == "__main__": unittest.main()
