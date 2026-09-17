import subprocess, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_clarification_gate.py"
class ClarificationGateTests(unittest.TestCase):
    def test_valid_cases_pass(self):
        result = subprocess.run([sys.executable,str(CHECKER),str(ROOT / "examples/clarification-cases.json")],cwd=ROOT,check=False,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
    def test_invalid_cases_fail_closed(self):
        result = subprocess.run([sys.executable,str(CHECKER),str(ROOT / "fixtures/broken/invalid-clarification-cases.json")],cwd=ROOT,check=False,capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
if __name__ == "__main__": unittest.main()
