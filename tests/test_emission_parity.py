"""CI parity check: emitted/ must be in sync with schema."""

import sys
from pathlib import Path

EMIT_SCRIPT = Path(__file__).parent.parent / "scripts" / "emit.py"


def test_emission_parity() -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("emit", EMIT_SCRIPT)
    assert spec is not None and spec.loader is not None
    emit_module = importlib.util.module_from_spec(spec)
    sys.modules["emit"] = emit_module
    spec.loader.exec_module(emit_module)

    old_argv = sys.argv
    try:
        sys.argv = [str(EMIT_SCRIPT), "--check"]
        ret = emit_module.main()
    finally:
        sys.argv = old_argv

    assert ret == 0
