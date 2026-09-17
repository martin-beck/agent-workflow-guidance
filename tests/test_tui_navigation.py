import subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TuiNavigationTests(unittest.TestCase):
 def test_positive(self): self.assertEqual(subprocess.run([sys.executable,str(ROOT/'tools/check_tui_navigation.py'),str(ROOT/'examples/tui-navigation.json')]).returncode,0)
 def test_session_navigation_preserves_anchor_and_highlight(self):
  sys.path.insert(0,str(ROOT/'tools'))
  from discussion_tui import DiscussionPoint, DiscussionSession
  session=DiscussionSession((DiscussionPoint('p1','design:42','bounded',True),DiscussionPoint('p2','work-plan:8','dependency')))
  self.assertEqual(session.highlight,'bounded'); self.assertEqual(session.unresolved_ids,('p1',)); self.assertEqual(session.switch_document('work-plan'),'design:42'); self.assertEqual(session.move(1).point_id,'p2')
