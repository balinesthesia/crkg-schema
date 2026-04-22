# crkg-schema

**Language-agnostic data contracts for clinical reasoning knowledge graphs.**

---

## Status

- **Version:** v0.0 (scaffold — no schema content yet)
- **License:** Apache-2.0
- **Posture:** Public, open source, independently versioned
- **Stage:** Pre-schema. M0 infrastructure in progress.
- **Companion library:** [`crkg`](https://github.com/balinesthesia/crkg) (Python, depends on this package)

---

## What `crkg-schema` is

`crkg-schema` is the single source of truth for the data model underlying clinical reasoning knowledge graphs. The model is authored in [LinkML](https://linkml.io/) and emitted into multiple target formats so that consumers in any language can validate, generate, and query data consistently.

Emission targets (all generated from one LinkML YAML source):

1. **JSON Schema** (Draft 2020-12) — runtime validation in any language
2. **Pydantic v2 models** — Python consumers
3. **Cypher DDL** — Neo4j bootstrap (constraints, indexes)
4. **Mermaid class diagrams** — documentation
5. **OWL / SHACL** — optional, for RDF consumers (post-M1)

This package ships the schema source, the emitted artifacts, and a validator. It does not ship a graph store, ingestion logic, or Python helpers beyond the emitted Pydantic models — those live in [`crkg`](https://github.com/balinesthesia/crkg).

## What `crkg-schema` is not

- Not a graph database, not a driver, not a loader
- Not tied to Neo4j, Memgraph, or any specific backend (the Cypher DDL emission is a convenience, not a coupling)
- Not a clinical terminology server (uses terminologies like ICD-11, SNOMED CT, LOINC, RxNorm as values, does not redistribute them)
- Not an application schema for any specific CDSS product — it is a substrate other projects build on

## Why LinkML

LinkML was chosen after evaluating JSON Schema, Protobuf, and SHACL for this role. The decision record is in [`ARCHITECTURE.md §3`](ARCHITECTURE.md#3-why-linkml). In short:

- One YAML source → many target formats (JSON Schema, Pydantic, Cypher, OWL, SHACL, Mermaid) via `linkml` toolchain
- First-class support for slots, classes, inheritance, and associations — the vocabulary a graph schema needs
- Genuine biomedical community adoption (Monarch Initiative, Biolink model, OBO foundry, NCATS projects)
- Permissive licensing (CC0 schema language, Apache-2.0 toolchain)
- Non-opinionated about storage — the same schema describes RDF graphs, Neo4j property graphs, or relational tables

## Version policy

Schema versioning is independent from consuming libraries.

- **v0.0.x** — placeholder and scaffold. Schema content is not yet authored.
- **v0.1.x** — pre-1.0, **may break between minor versions**. Consumers pin `>=0.1,<0.2`.
- **v1.0.0** — schema stability commitment. Breaking changes from this point bump the major version. Deprecations carry through at least one minor version before removal.

Each release ships:

- `schema/` — LinkML YAML source
- `emitted/json-schema/` — JSON Schema per class
- `emitted/pydantic/` — Pydantic v2 model module
- `emitted/cypher/` — Cypher constraint and index DDL
- `emitted/mermaid/` — class diagram sources
- `fixtures/valid/` — example instances per class
- `fixtures/invalid/` — adversarial instances that must fail validation

Consumers pick the artifacts they need. Most Python consumers install the Pydantic models via `pip install crkg-schema`; everyone else consumes the JSON Schema files from the release tarball.

## Installation

> **Note:** During v0.0.x (infrastructure-only), releases are published to **TestPyPI** only.
> Production PyPI publishing will start at v0.1.0 once schema content lands.

```bash
# From TestPyPI (v0.0.x)
pip install --index-url https://test.pypi.org/simple/ crkg-schema

# From PyPI (v0.1.0+)
pip install crkg-schema

# Or with uv
uv add crkg-schema

# Non-Python consumers: download release artifacts
# curl -L https://github.com/balinesthesia/crkg-schema/releases/download/v0.1.0/crkg-schema-0.1.0.tar.gz
```

## Relationship to other projects

- [`crkg`](https://github.com/balinesthesia/crkg) — Python library. Depends on `crkg-schema` for Pydantic models and Cypher DDL. First consumer.
- [`clinical-rs`](https://github.com/balinesthesia/clinical-rs) — Rust workspace for clinical data engineering. Independent. May emit data shaped by `crkg-schema` in future Rust ports.
- [`multiomics-rs`](https://github.com/balinesthesia/multiomics-rs) — Rust workspace for molecular reference databases. Independent. Same possible future binding.
- [`Zluidr/hl7-rs`](https://github.com/Zluidr/hl7-rs) — Rust HL7 v2 / FHIR / SATUSEHAT crates. Independent. Could emit Arrow records shaped by `crkg-schema` types at hospital ingestion boundaries.

None of these projects is a runtime dependency of `crkg-schema`. The dependency graph flows only inward (everyone depends on the schema; the schema depends on nothing of ours).

## Third-party data licensing

The schema describes data structures. It does not ship any clinical or molecular data. When consumers populate the schema with data from licensed sources (SNOMED CT, DrugBank, ICD-11, RxNorm, etc.), they remain responsible for compliance with those licenses. See [`NOTICE`](NOTICE) for the full attribution posture.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Issues and PRs welcome; follow the branch naming and signed-commit guidelines in that file.

## Documents

- [`README.md`](README.md) — this file
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — modeling philosophy, LinkML decision record, emission pipeline, schema layers, adapter contracts
- [`TODO.md`](TODO.md) — atomic M0 tasks, dependency-ordered, with SemVer gates
- [`LICENSE`](LICENSE) — Apache-2.0
- [`NOTICE`](NOTICE) — third-party attributions

## Version log

- **v0.0 (2026-04-19):** Initial scaffold. README, ARCHITECTURE, TODO, LICENSE, NOTICE. No schema content. M0 infrastructure starting.
