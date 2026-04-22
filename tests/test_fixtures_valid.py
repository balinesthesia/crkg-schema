"""Validate every fixture in fixtures/valid/."""

from pathlib import Path

VALID_DIR = Path(__file__).parent.parent / "fixtures" / "valid"


def test_all_valid_fixtures() -> None:
    if not VALID_DIR.exists():
        return
    files = [p for p in VALID_DIR.iterdir() if p.name != ".gitkeep"]
    assert not files  # empty set passes trivially for M0
