import json
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_contracts import load_json, validate  # noqa: E402


def check(example: str, schema_name: str) -> list[str]:
    schema = load_json(ROOT / "schema" / schema_name)
    return validate(load_json(ROOT / "examples" / example), schema, schema, ROOT / "schema")


def test_endpoint_candidate_contract_is_valid_and_redacted():
    assert check("remote-endpoint-candidates.json", "remote-endpoint-candidates.schema.json") == []
    text = (ROOT / "examples/remote-endpoint-candidates.json").read_text()
    assert "private" not in text.lower()


def test_ssh_enrollment_contract_is_valid_and_has_no_private_key():
    assert check("remote-ssh-enrollment.json", "remote-ssh-enrollment.schema.json") == []
    value = json.loads((ROOT / "examples/remote-ssh-enrollment.json").read_text())
    assert "private_key" not in value
