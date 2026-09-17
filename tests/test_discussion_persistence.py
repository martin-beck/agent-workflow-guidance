import subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PersistenceTests(unittest.TestCase):
 def test_positive(self): self.assertEqual(subprocess.run([sys.executable,str(ROOT/'tools/check_discussion_persistence.py'),str(ROOT/'examples/discussion-persistence.json')]).returncode,0)
