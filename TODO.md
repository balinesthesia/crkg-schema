# crkg-schema — TODO

**Document version:** v0.0 (2026-04-19)
**SemVer target:** v0.0.1 → v0.0.x → v0.1.0 → v1.0.0
**Current phase:** M0 — Infrastructure-first
**Discipline:** SDLC-aligned, hierarchical task/subtask. Stable IDs. Kill-gates per phase.

---

## How this file works

- **Task IDs** are stable (`M0-T01`). Never renumbered. Removed tasks are tombstoned in [Track Z](#track-z--tombstones).
- **Status** is one of: `TODO`, `IN PROGRESS`, `DONE`, `BLOCKED`, `PARKED`.
- **Dependency** = task IDs this task waits on. Respect order.
- **Architecture links** `[A§X.Y]` point into `ARCHITECTURE.md`.
- **SemVer bands:**
  - `v0.0.x` — infrastructure, no schema content
  - `v0.1.0` — first schema content, pre-stable, breaking changes allowed between minor versions
  - `v0.x.y` — iterating on schema
  - `v1.0.0` — schema stability commitment (post-M0, not in scope for this document)
- **No schema content** lands in M0. M0 is only toolchain, emission pipeline, fixtures harness, CI. Schema authoring starts in M1.

---

## M0 — Infrastructure-first

**Goal:** A contributor can clone the repo, run `make check` (or `just check`), and see LinkML toolchain + emission pipeline + CI pass. No schema content required. The *ground* the schema will be built on.

**Target completion:** v0.0.1 released to TestPyPI with an empty-but-valid LinkML schema.

---

## Phase 1 — Legal & Governance (target v0.0.1)

**Linked:** [A§3 Decision record]

### M0-T01 — Commit `LICENSE` (Apache-2.0)
- [x] **Status:** DONE
- **Dependency:** —
- **Notes:** Full Apache-2.0 text. Copyright line: `Copyright 2026 Kresna Sucandra and crkg-schema contributors`.

### M0-T02 — Commit `NOTICE`
- [x] **Status:** DONE
- **Dependency:** —
- **Notes:** Attribution for LinkML toolchain (BSD-3-Clause), Python (PSF), uv (MIT OR Apache-2.0). Note that schema does not redistribute any licensed clinical terminology.

### M0-T03 — Commit `SECURITY.md`
- [x] **Status:** DONE
- **Dependency:** —
- **Notes:** Private disclosure process. Email placeholder pending ops setup.

### M0-T04 — Commit `CODE_OF_CONDUCT.md`
- [x] **Status:** DONE
- **Dependency:** —
- **Notes:** Contributor Covenant 2.1 or equivalent.

### M0-T05 — Add `.github/CODEOWNERS`
- [x] **Status:** DONE
- **Dependency:** —
- **Notes:** `* @balinesthesia` for bootstrap. Expand when the contributor pool grows.

### M0-T06 — Reserve `crkg-schema` on PyPI
- [ ] **Status:** TODO
- **Dependency:** M0-T10
- **Notes:** Buildable package ready. Requires PyPI/TestPyPI credentials or trusted-publisher setup in CI to publish the v0.0.0 placeholder. Run manually or via `release.yml` once credentials are configured.

---

## Phase 2 — Python toolchain (target v0.0.1)

**Linked:** [A§3 D-05 Python floor]

### M0-T10 — Create `pyproject.toml`
- [x] **Status:** DONE
- **Dependency:** M0-T01
- **Notes:** Build backend `hatchling`. Project metadata: name `crkg-schema`, version from `schema/__init__.py`, Apache-2.0, URLs, authors. Python `>=3.13`. Dev deps: `linkml`, `pytest`, `ruff`, `mypy`.

#### M0-T10.1 — Configure hatchling
- [x] Include `schema/` as source
- [x] Include `emitted/` as package data
- [x] Include `fixtures/` as package data

#### M0-T10.2 — Configure `[tool.ruff]` and `[tool.mypy]`
- [x] Strict mypy
- [x] Ruff: E, F, I, N, UP, B, SIM

### M0-T11 — Pin Python version in `.python-version`
- [x] **Status:** DONE
- **Dependency:** M0-T10
- **Notes:** `3.13`. Not a range — specific version for reproducibility.

### M0-T12 — Commit `uv.lock`
- [x] **Status:** DONE
- **Dependency:** M0-T10
- **Notes:** Run `uv lock`. Lock file committed.

### M0-T13 — Verify `uv sync` on cold clone
- [x] **Status:** DONE
- **Dependency:** M0-T12
- **Notes:** Linux, macOS. Windows best-effort.

---

## Phase 3 — LinkML toolchain (target v0.0.1)

**Linked:** [A§3 D-01, D-04], [A§6 Emission pipeline]

### M0-T20 — Pin LinkML dependency
- [x] **Status:** DONE
- **Dependency:** M0-T10
- **Notes:** `linkml>=1.8,<2.0`. Transitively includes `linkml-runtime`.

### M0-T21 — Create minimal valid `schema/crkg.yaml`
- [x] **Status:** DONE
- **Dependency:** M0-T20
- **Notes:** LinkML schema with `name`, `id`, `prefixes`, empty `classes`. No content, just structure. This validates the LinkML toolchain works end-to-end before any domain modeling.

### M0-T22 — Verify `linkml-validate` passes on empty schema
- [x] **Status:** DONE
- **Dependency:** M0-T21
- **Notes:** `linkml-validate --schema schema/crkg.yaml` — expect no errors.

### M0-T23 — Verify JSON Schema emission on empty schema
- [x] **Status:** DONE
- **Dependency:** M0-T22
- **Notes:** `gen-json-schema schema/crkg.yaml > /tmp/crkg.schema.json` — must produce valid JSON.

### M0-T24 — Verify Pydantic emission on empty schema
- [x] **Status:** DONE
- **Dependency:** M0-T22
- **Notes:** `gen-pydantic schema/crkg.yaml > /tmp/crkg_models.py` — must produce importable Python.

---

## Phase 4 — Emission pipeline (target v0.0.1)

**Linked:** [A§6 Emission pipeline]

### M0-T30 — Create `scripts/emit.py` driver
- [x] **Status:** DONE
- **Dependency:** M0-T23, M0-T24
- **Notes:** One command runs all emission targets. Uses LinkML APIs directly (no shell outs). Writes to `emitted/`.

#### M0-T30.1 — JSON Schema emission
- [x] Per-class `.json` files in `emitted/json-schema/`
- [x] Draft 2020-12

#### M0-T30.2 — Pydantic emission
- [x] Single `emitted/pydantic/models.py`
- [x] Pydantic v2, no v1 back-compat

#### M0-T30.3 — Cypher DDL emission (custom emitter)
- [x] Consumes LinkML `SchemaView`
- [x] Emits `CREATE CONSTRAINT` and `CREATE INDEX` statements
- [x] One file per layer (core, epidemiology, formulary, ethnobotany)
- [x] Written in Python under `scripts/emitters/cypher.py`

#### M0-T30.4 — Mermaid emission (custom emitter)
- [x] One `.mmd` per schema layer
- [x] Class diagram showing inheritance + associations
- [x] Written in Python under `scripts/emitters/mermaid.py`

### M0-T31 — CI parity check
- [x] **Status:** DONE
- **Dependency:** M0-T30
- **Notes:** CI runs `scripts/emit.py`, compares output to committed `emitted/`. Any drift fails the build. Prevents hand-edited emission.

### M0-T32 — `Makefile` or `justfile`
- [x] **Status:** DONE
- **Dependency:** M0-T30
- **Notes:** Targets: `check`, `test`, `emit`, `fmt`, `lint`. `make emit` regenerates `emitted/`.

---

## Phase 5 — Fixtures harness (target v0.0.1)

**Linked:** [A§4 Repository layout — fixtures]

### M0-T40 — Create `fixtures/` directory structure
- [x] **Status:** DONE
- **Dependency:** M0-T21
- **Notes:** `fixtures/valid/` and `fixtures/invalid/`. Empty for M0 — populated as schema content lands in M1.

### M0-T41 — Fixture validation harness
- [x] **Status:** DONE
- **Dependency:** M0-T22, M0-T40
- **Notes:** `tests/test_fixtures_valid.py` iterates `fixtures/valid/` and validates each. `tests/test_fixtures_invalid.py` iterates `fixtures/invalid/` and asserts each fails validation. Both tests pass on empty fixture sets.

---

## Phase 6 — CI/CD (target v0.0.1)

**Linked:** [A§3 D-11 from `crkg` — CI platform aligned]

### M0-T50 — `.github/workflows/ci.yml`
- [x] **Status:** DONE
- **Dependency:** M0-T10, M0-T30, M0-T41
- **Notes:** Runs on every PR. Jobs: `lint` (ruff, mypy), `schema-valid` (linkml-validate), `emission-parity` (M0-T31), `fixtures-valid` (pytest), `build` (uv build). All required before merge.

### M0-T51 — `.github/workflows/release.yml`
- [x] **Status:** DONE
- **Dependency:** M0-T50
- **Notes:** Triggered on tag `v*`. Runs full CI, builds sdist + wheel, creates GitHub Release, publishes to PyPI via trusted publisher. Attaches `emitted/` tarball.

### M0-T52 — Branch protection on `main`
- [x] **Status:** DONE
- **Dependency:** M0-T50
- **Notes:** Require CI green, require PR review, require signed commits. Document in `docs/BRANCH_PROTECTION.md`.

### M0-T53 — `pre-commit` hooks
- [x] **Status:** DONE
- **Dependency:** M0-T10
- **Notes:** `.pre-commit-config.yaml` — ruff, mypy, linkml-validate, check-merge-conflict, trailing-whitespace, end-of-file-fixer, check-yaml, detect-private-key, gitleaks.

---

## Phase 7 — Documentation (target v0.0.1)

### M0-T60 — `CONTRIBUTING.md`
- [x] **Status:** DONE
- **Dependency:** M0-T50
- **Notes:** Branch naming, signed commits, PR requirements, schema-change process (every schema change = fixture update + CHANGELOG entry).

### M0-T61 — `CHANGELOG.md`
- [x] **Status:** DONE
- **Dependency:** —
- **Notes:** Keep-a-changelog format. Starts empty.

### M0-T62 — `docs/DEV_SETUP.md`
- [x] **Status:** DONE
- **Dependency:** M0-T13
- **Notes:** Cold-start contributor → `make check` passing on first PR.

### M0-T63 — PR and Issue templates
- [x] **Status:** DONE
- **Dependency:** —
- **Notes:** `.github/ISSUE_TEMPLATE/bug.md`, `.github/ISSUE_TEMPLATE/schema-proposal.md`, `.github/PULL_REQUEST_TEMPLATE.md`.

---

## Phase 8 — Release v0.0.1 (target: M0 kill-gate)

### M0-T70 — Tag and release v0.0.1
- [ ] **Status:** TODO
- **Dependency:** all M0-T01..M0-T63
- **Notes:** First tagged release. Published to TestPyPI only (not production PyPI). An empty-but-valid LinkML schema, full emission pipeline, CI green.

### M0-T71 — Verify `pip install -i https://test.pypi.org/simple/ crkg-schema` works
- [ ] **Status:** TODO
- **Dependency:** M0-T70
- **Notes:** Fresh venv, install, `import crkg_schema` succeeds, `crkg_schema.__version__ == "0.0.1"`.

---

## M0 Kill-criteria

All of the following must hold before M1 begins:

1. `LICENSE` (Apache-2.0) and `NOTICE` committed.
2. `pyproject.toml`, `uv.lock`, `.python-version` pinning 3.13 committed and green.
3. `schema/crkg.yaml` is a valid LinkML schema, even if empty.
4. `scripts/emit.py` runs end-to-end producing JSON Schema, Pydantic, Cypher DDL, and Mermaid artifacts.
5. `emitted/` is committed and CI parity check passes.
6. `tests/test_fixtures_valid.py` and `tests/test_fixtures_invalid.py` pass on empty fixture sets.
7. CI workflow green on `main`.
8. `crkg-schema` reserved on PyPI (empty v0.0.0) and v0.0.1 published to TestPyPI.
9. Cold-start contributor can reach green CI on their first PR within a working day, documented in `docs/DEV_SETUP.md`.

---

## M1 — Schema content (deferred)

Not in scope for this document. Draft when M0 is complete. Sketch:

- Phase 1: Authoring core layer (entities, identifiers, relationships) — target v0.1.0
- Phase 2: Authoring epidemiology layer — target v0.2.0
- Phase 3: Authoring formulary layer — target v0.3.0
- Phase 4: Authoring ethnobotany adapter contract — target v0.4.0
- Phase 5: Authoring fixtures for each class — rolling across all phases
- Phase 6: Coordination with `crkg` (Pydantic binding) — per phase
- Phase 7: Coordination with DeepReasoner (consumer validation) — per phase
- Phase 8: Release v0.1.0 — first PyPI production publication when Phase 1 complete

**Gate to M1:** M0 kill-criteria met AND `crkg` M0 complete. The two repositories advance together from this point.

**Schema stability commitment (v1.0.0):** not before six months of consumer usage AND one complete end-to-end run through DeepReasoner's reasoning pipeline.

---

## Track Z — Tombstones

Reserved. Removed tasks keep their IDs here with reason and date.

| ID | Original Task | Reason for Removal | Date Removed |
|---|---|---|---|
| — | — | — | — |

---

## Parked ideas

Items out of scope for now. Move to an active milestone if context justifies.

| Idea | Why parked | Likely milestone |
|---|---|---|
| OWL emission | Post-v1.0; only useful when RDF consumers materialize | M3+ |
| SHACL emission | Post-v1.0; same reason as OWL | M3+ |
| TypeScript type emission | No TS consumer exists yet | When one does |
| Rust type emission | No Rust consumer exists yet | When one does |
| Biolink model alignment | Research; would require domain review | M2 |

---

## Version log

| Version | Date | Description |
|---|---|---|
| v0.0 | 2026-04-19 | Initial TODO. M0 phases 1–8 defined. M1 sketched as deferred. No tasks started. |
