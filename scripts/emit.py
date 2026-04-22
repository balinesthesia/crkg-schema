#!/usr/bin/env python
"""Run all emission targets from the LinkML schema."""

import argparse
import re
import shutil
import sys
from pathlib import Path

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.pydanticgen import PydanticGenerator

# Allow importing sibling emitters/ directory when run as a script
sys.path.insert(0, str(Path(__file__).parent))

from emitters.cypher import emit_cypher
from emitters.mermaid import emit_mermaid

SCHEMA_FILE = Path(__file__).parent.parent / "schema" / "crkg.yaml"
EMITTED_DIR = Path(__file__).parent.parent / "emitted"


def _clean(target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)


def _emit_json_schema() -> None:
    gen = JsonSchemaGenerator(SCHEMA_FILE)
    out = gen.serialize()
    (EMITTED_DIR / "json-schema" / "crkg.json").write_text(out)


def _emit_pydantic() -> None:
    gen = PydanticGenerator(SCHEMA_FILE)
    out = gen.serialize()
    # Normalize absolute source_file paths so emission parity passes on any CI runner
    out = re.sub(
        r"('source_file'\s*:\s*)'[^']*schema/crkg\.yaml'",
        r"\1'schema/crkg.yaml'",
        out,
    )
    (EMITTED_DIR / "pydantic" / "models.py").write_text(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit all targets from the LinkML schema.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if emitted/ would change (CI parity check).",
    )
    args = parser.parse_args()

    for subdir in ("json-schema", "pydantic", "cypher", "mermaid"):
        _clean(EMITTED_DIR / subdir)

    _emit_json_schema()
    print("Emitted JSON Schema")

    _emit_pydantic()
    print("Emitted Pydantic models")

    emit_cypher(SCHEMA_FILE, EMITTED_DIR / "cypher")
    print("Emitted Cypher DDL")

    emit_mermaid(SCHEMA_FILE, EMITTED_DIR / "mermaid")
    print("Emitted Mermaid diagrams")

    if args.check:
        import subprocess

        result = subprocess.run(
            ["git", "diff", "--exit-code", "--", "emitted/"],
            cwd=EMITTED_DIR.parent,
        )
        if result.returncode != 0:
            print("ERROR: emitted/ is out of sync with schema. Run `make emit`.")
            return 1
        print("Emitted artifacts are in sync.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
