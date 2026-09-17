import subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TuiIntegrationTests(unittest.TestCase):
 def test_positive(self): self.assertEqual(subprocess.run([sys.executable,str(ROOT/'tools/check_tui_integration.py'),str(ROOT/'examples/tui-integration.json')]).returncode,0)
