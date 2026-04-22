"""CI parity check: emitted/ must be in sync with schema."""

import subprocess
import sys
from pathlib import Path

EMIT_SCRIPT = Path(__file__).parent.parent / "scripts" / "emit.py"


def test_emission_parity() -> None:
    result = subprocess.run(
        [sys.executable, str(EMIT_SCRIPT), "--check"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
