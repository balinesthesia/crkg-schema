"""Test that the LinkML schema itself is well-formed."""

import subprocess
from pathlib import Path

SCHEMA_FILE = Path(__file__).parent.parent / "schema" / "crkg.yaml"


def test_schema_validates() -> None:
    result = subprocess.run(
        ["linkml-validate", "--schema", str(SCHEMA_FILE)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
