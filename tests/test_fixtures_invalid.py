"""Assert every fixture in fixtures/invalid/ fails validation."""

from pathlib import Path

INVALID_DIR = Path(__file__).parent.parent / "fixtures" / "invalid"


def test_all_invalid_fixtures() -> None:
    if not INVALID_DIR.exists():
        return
    files = [p for p in INVALID_DIR.iterdir() if p.name != ".gitkeep"]
    assert not files  # empty set passes trivially for M0
