import subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class BatchTests(unittest.TestCase):
 def test_checker(self): self.assertEqual(subprocess.run([sys.executable,str(ROOT/'tools/check_batched_discussion.py'),str(ROOT/'examples/discussion-batch.json')]).returncode,0)
 def test_partial_answers(self):
  sys.path.insert(0,str(ROOT/'tools')); from batched_discussion import BatchedDiscussion
  b=BatchedDiscussion(({'id':'p1'},{'id':'p2'})); b.answer('p1',{'choice':'A'}); self.assertEqual(b.unanswered(),('p2',))
