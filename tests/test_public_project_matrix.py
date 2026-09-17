import subprocess, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_public_project_matrix.py"
class PublicMatrixTests(unittest.TestCase):
    def test_matrix_passes(self):
        result = subprocess.run([sys.executable,str(CHECKER),str(ROOT / "examples/public-project-matrix.json")],cwd=ROOT,check=False,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
if __name__ == "__main__": unittest.main()
