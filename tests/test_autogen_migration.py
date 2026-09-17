import subprocess, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_autogen_migration.py"
class AutoGenMigrationTests(unittest.TestCase):
    def test_decision_passes(self):
        result = subprocess.run([sys.executable,str(CHECKER),str(ROOT / "examples/autogen-migration-decision.json")],cwd=ROOT,check=False,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
    def test_invalid_decision_fails(self):
        result = subprocess.run([sys.executable,str(CHECKER),str(ROOT / "fixtures/broken/invalid-autogen-migration-decision.json")],cwd=ROOT,check=False,capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
if __name__ == "__main__": unittest.main()
