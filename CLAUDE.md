# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project stage

`crkg-schema` is the LinkML source-of-truth for clinical-reasoning-graph data contracts. It is currently **v0.0 scaffold**: infrastructure is in place but `schema/crkg.yaml` has `classes: {}` — no schema content is authored yet. Most feature work in M0 is filling in that YAML, then regenerating the `emitted/` artifacts.

## Commands

Development runs through `uv` + `make` (see `docs/DEV_SETUP.md`). Python 3.13 is required (pinned in `.python-version`).

```bash
uv sync --extra dev              # one-time: install dev deps (linkml, pytest, ruff, mypy)

make check                       # fmt + lint + mypy --strict + pytest (full local gate)
make emit                        # regenerate emitted/ from schema/crkg.yaml
make test                        # pytest only
make fmt                         # ruff format
make lint                        # ruff check + mypy (scripts/ tests/)

uv run pytest tests/test_fixtures_valid.py::test_all_valid_fixtures   # single test
uv run linkml-validate --schema schema/crkg.yaml                      # schema well-formedness
uv run python scripts/emit.py --check                                 # emission-parity gate (CI)
```

Pre-commit (`pre-commit install`) runs ruff, mypy --strict on `scripts/` + `tests/`, `linkml-validate`, and gitleaks. Commits must be **signed** (`git commit -S`); `main` requires linear history, so prefer rebase over merge.

## Architecture

### One source, many emissions

The entire repository exists to propagate one LinkML YAML file into multiple language/format targets. Treat `schema/crkg.yaml` and its future `schema/core/`, `schema/epidemiology/`, `schema/formulary/`, `schema/ethnobotany/` imports as the *only* authored schema artifacts. Everything under `emitted/` is generated — never hand-edit. CI's `emission-parity` job (`scripts/emit.py --check`) fails the build if `emitted/` drifts from what the schema would produce, so any schema change requires `make emit` + committing the regenerated artifacts in the same PR.

`scripts/emit.py` orchestrates four emitters:

- **JSON Schema** + **Pydantic v2** come from the stock `linkml.generators` (`JsonSchemaGenerator`, `PydanticGenerator`).
- **Cypher DDL** (`scripts/emitters/cypher.py`) and **Mermaid class diagrams** (`scripts/emitters/mermaid.py`) are custom emitters that consume `linkml_runtime.utils.schemaview.SchemaView` directly. They intentionally live in-tree rather than as LinkML plugins to keep the dependency graph flat.
- Both custom emitters partition classes into layers via the LinkML `in_subset` annotation (`core`, `epidemiology`, `formulary`, `ethnobotany`), falling back to `core`. When adding schema content, set `in_subset` appropriately or it will silently land in the core layer's emitted files.

OWL/SHACL/TS/Rust targets are deferred post-v1.0 per ARCHITECTURE.md §3 (D-03). Don't add them speculatively.

### Schema layers and dependency direction

Four schema layers are defined in ARCHITECTURE.md §5: `core` (entities, identifiers, enums, core edges), `epidemiology` (Region, PopulationPrior, ENDEMIC_IN), `formulary` (FormularyEntry, IN_FORMULARY), `ethnobotany` (adapter contract only — the schema defines the *shape* and *provenance envelope* of `EthnobotanyEntity`; actual corpora are loaded by adapters implemented in consumer libs).

Dependency flow is strictly one-way: `crkg-schema` → `crkg` (Python lib) → CDSS apps. The schema must not import or reference any consumer. Sibling projects (`clinical-rs`, `multiomics-rs`, `hl7-rs`) are independent and not runtime dependencies.

### Package layout quirk

`src/crkg_schema/` is nearly empty on purpose — the package is mostly-data. `pyproject.toml` uses `hatchling.build.targets.wheel.force-include` to ship `schema/`, `emitted/`, and `fixtures/` inside the wheel under `crkg_schema/`. When adding runtime Python code, put it under `src/crkg_schema/`; don't place importable code under `scripts/` (which is dev-only and not packaged).

Version is read from `src/crkg_schema/__init__.py` via `hatch.version`. Releases are cut by pushing a `v*` tag; `.github/workflows/release.yml` handles PyPI + GitHub release.

### Versioning contract

Pre-1.0 (`v0.x`) **may break between minor versions**; consumers pin `>=0.1,<0.2`. `v1.0` locks schema stability with deprecation-through-one-minor. Breaking-change decisions belong in `ARCHITECTURE.md`'s decision record (D-01..D-05 pattern) before any schema edit.

### Non-goals — do not add

Per ARCHITECTURE.md §2 and §10, this repo is not the place for: graph-store logic, ingestion pipelines, reasoning logic, LLM prompt schemas, audit-trail formats, clinical terminology redistribution, or adapter *implementations*. Those belong in `crkg` (the Python consumer) or application repos. If a change feels like it adds one of these, stop and reconsider.
