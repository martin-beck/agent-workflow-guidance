import subprocess, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_evaluation_plan.py"
class EvaluationPlanTests(unittest.TestCase):
    def test_valid_plan_passes(self):
        result = subprocess.run([sys.executable,str(CHECKER),str(ROOT / "examples/evaluation-scenarios.json")],cwd=ROOT,check=False,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
    def test_invalid_plan_fails_closed(self):
        result = subprocess.run([sys.executable,str(CHECKER),str(ROOT / "fixtures/broken/invalid-evaluation-scenarios.json")],cwd=ROOT,check=False,capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
if __name__ == "__main__": unittest.main()
