import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CrossProjectTuiTests(unittest.TestCase):
    def test_positive_trace(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/check_cross_project_tui.py"), str(ROOT / "examples/cross-project-tui.json")])
        self.assertEqual(result.returncode, 0)

    def test_hostile_mutation_rejected(self):
        value = json.loads((ROOT / "examples/cross-project-tui.json").read_text())
        value["discussion_points"][0]["response"]["point_id"] = "storage"
        fixture = ROOT / "examples/.cross-project-tui-hostile.json"
        fixture.write_text(json.dumps(value))
        try:
            result = subprocess.run([sys.executable, str(ROOT / "tools/check_cross_project_tui.py"), str(fixture)])
            self.assertNotEqual(result.returncode, 0)
        finally:
            fixture.unlink()


if __name__ == "__main__":
    unittest.main()
