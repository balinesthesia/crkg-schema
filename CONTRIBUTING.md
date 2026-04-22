# Contributing to crkg-schema

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Getting started

```bash
git clone https://github.com/balinesthesia/crkg-schema.git
cd crkg-schema
uv sync --extra dev
make check
```

## Branch naming

- `fix/<short-desc>` — bug fixes
- `feat/<short-desc>` — new schema features
- `docs/<short-desc>` — documentation
- `infra/<short-desc>` — tooling or CI changes

## Commits

All commits must be **signed** (`git commit -S`).

## Pull requests

- Every PR must pass `make check` (lint + type-check + test).
- Schema changes require:
  1. Updated fixture examples in `fixtures/valid/` and/or `fixtures/invalid/`
  2. An entry in `CHANGELOG.md`
  3. Regenerated `emitted/` artifacts (`make emit`)
- Request review from at least one code owner.

## Schema change process

1. Edit the LinkML YAML under `schema/`
2. Run `make emit` to regenerate all targets
3. Add or update fixtures that exercise the new classes/slots
4. Ensure CI passes before merging

## Release

Releases are cut from `main` by pushing a `v*` tag. CI handles the rest.
