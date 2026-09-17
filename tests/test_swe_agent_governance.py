import subprocess, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_swe_agent_governance.py"

class SweAgentGovernanceTests(unittest.TestCase):
    def test_cases_pass(self):
        result = subprocess.run([sys.executable, str(CHECKER), str(ROOT / "examples/swe-agent-governance-cases.json")], cwd=ROOT, check=False, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_score_only_fixture_fails(self):
        result = subprocess.run([sys.executable, str(CHECKER), str(ROOT / "fixtures/broken/invalid-swe-agent-governance-cases.json")], cwd=ROOT, check=False, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)

if __name__ == "__main__": unittest.main()
