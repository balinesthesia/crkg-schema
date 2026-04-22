"""Validate every fixture in fixtures/valid/."""

import subprocess
from pathlib import Path

SCHEMA_FILE = Path(__file__).parent.parent / "schema" / "crkg.yaml"
VALID_DIR = Path(__file__).parent.parent / "fixtures" / "valid"


def _fixture_files(directory: Path) -> list[Path]:
    return [p for p in directory.iterdir() if p.suffix in (".yaml", ".yml", ".json")]


def test_all_valid_fixtures() -> None:
    if not VALID_DIR.exists():
        return
    files = _fixture_files(VALID_DIR)
    if not files:
        return  # empty set passes trivially for M0
    for fixture in files:
        result = subprocess.run(
            ["linkml-validate", "--schema", str(SCHEMA_FILE), str(fixture)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Fixture {fixture.name} failed validation: {result.stderr}"
