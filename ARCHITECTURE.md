# crkg-schema — Architecture

**Document version:** v0.0 (2026-04-19)
**Scope:** design, not implementation — describes what `crkg-schema` will be when v1.0 is cut.

---

## 1. Design goals

1. **One schema, many languages.** Python, Rust, TypeScript, Java consumers all see the same logical model. No language is privileged.
2. **Non-opinionated about storage.** The schema describes entities and relationships; it does not prescribe Neo4j, Memgraph, or any specific graph store.
3. **Non-opinionated about terminology.** Schema uses ICD-11, SNOMED CT, LOINC, RxNorm, ATC as *value* references. It does not embed, redistribute, or bless a specific terminology version.
4. **Independently versioned.** Breaking changes to the schema are orthogonal to breaking changes in any consuming library.
5. **Extendable by pluggable adapters.** Third-party corpora (e.g., traditional-medicine systems) slot in via an adapter interface defined here, implemented elsewhere.
6. **Regulatorily reviewable.** The full schema must fit on a human-auditable page count. No reflection, no runtime codegen.

---

## 2. What a clinical reasoning KG schema needs to express

Three things. This is the entire scope of `crkg-schema`.

**Nodes** (entities)
- Clinical entities: Disease, Symptom, Phenotype, Condition
- Intervention entities: Drug, Treatment, Procedure, Protocol
- Diagnostic entities: Lab, Imaging, TestResult
- Observation entities: Sign, RiskFactor
- Context entities: Region, FormularyEntry, PopulationPrior
- Pluggable entities: EthnobotanyEntity (adapter-owned, see §7)

**Edges** (relationships)
- Clinical: `HAS_SYMPTOM`, `PRESENTS_WITH`, `CAUSED_BY`, `COMPLICATES`
- Therapeutic: `TREATED_BY`, `CONTRAINDICATED_IN`, `INTERACTS_WITH`
- Diagnostic: `MEASURED_BY`, `SUPPORTED_BY`, `REFUTED_BY`
- Epidemiological: `ENDEMIC_IN`, `PREVALENT_IN`, `RISK_ELEVATED_IN`
- Formulary: `IN_FORMULARY`, `COVERED_BY_TIER`
- Ethnobotanical: `TRADITIONAL_INDICATION_FOR`, `PREPARED_AS`

**Constraints**
- Required properties per entity type
- Cardinality on relationships
- Value-domain constraints (e.g., `ICD11Code` must match a pattern)
- Cross-property validation (e.g., if `status=validated`, `validated_by` and `validated_at` are required)

Nothing beyond this. No workflow, no clinical reasoning logic, no LLM prompt schemas, no audit trail formats. Those belong in consuming applications.

---

## 3. Why LinkML

Evaluated in decreasing order of adoption. Decision summary:

| Format | Rejected / Accepted | Reason |
|---|---|---|
| JSON Schema alone | Rejected | Describes shape, not graph semantics. Would need a custom overlay for nodes/edges — which is what LinkML already provides, formally. |
| Protobuf | Rejected | Excellent for wire formats and event logs; awkward for graph relationships with bidirectional traversal. Ental uses Protobuf for its ledger; that is the right tool for that problem, not this one. |
| SHACL | Rejected for authoring | Excellent for RDF constraint validation, but authoring is verbose and assumes RDF mental model. Kept as an **emission target** for RDF consumers. |
| OWL | Rejected for authoring | Semantically rigorous, practically painful to maintain. Kept as emission target. |
| Cypher DDL | Rejected | Neo4j-specific. Would defeat goal 2. Kept as emission target. |
| **LinkML** | **Accepted** | Authoring format. YAML, graph-aware (classes, slots, associations), emits JSON Schema, Pydantic, OWL, SHACL, Cypher, Mermaid from one source. Biomedical community adoption (Biolink, Monarch). |

### Decision record

- **D-01** (Schema authoring format): **LinkML** — Locked 2026-04-19
- **D-02** (Emission targets at v1.0): JSON Schema, Pydantic v2, Cypher DDL, Mermaid — Locked 2026-04-19
- **D-03** (Deferred emission targets): OWL, SHACL, TypeScript types, Rust types — Post-v1.0
- **D-04** (LinkML toolchain pin): `linkml>=1.8,<2.0` — Locked 2026-04-19, revisited at v1.0
- **D-05** (Python floor): `>=3.13` — Locked 2026-04-19

---

## 4. Repository layout

```
crkg-schema/
├── README.md
├── ARCHITECTURE.md
├── TODO.md
├── LICENSE                       Apache-2.0
├── NOTICE                        third-party attributions
├── CONTRIBUTING.md               (Phase 7 of M0)
├── SECURITY.md                   (Phase 7 of M0)
├── pyproject.toml                packaging, linkml deps, emission entry points
├── uv.lock
├── .python-version               3.13
├── .pre-commit-config.yaml
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                linkml validate + emission parity check
│   │   └── release.yml           tag → PyPI + GitHub release
│   └── CODEOWNERS
│
├── schema/                       LinkML YAML — SOURCE OF TRUTH
│   ├── crkg.yaml                 top-level import
│   ├── core/
│   │   ├── entities.yaml         Disease, Drug, Symptom, Lab, ...
│   │   ├── relationships.yaml    HAS_SYMPTOM, TREATED_BY, ...
│   │   ├── identifiers.yaml      ICD11Code, SNOMEDCode, LOINCCode, ...
│   │   └── enums.yaml            DomainVocabulary, CodeSystem, ...
│   ├── epidemiology/
│   │   ├── region.yaml           Region, ENDEMIC_IN
│   │   └── prior.yaml            PopulationPrior
│   ├── formulary/
│   │   └── formulary.yaml        FormularyEntry, IN_FORMULARY, COVERED_BY_TIER
│   └── ethnobotany/
│       └── adapter.yaml          EthnobotanyEntity + adapter contract
│
├── emitted/                      GENERATED — do not edit by hand
│   ├── json-schema/              per-class .json files
│   ├── pydantic/                 crkg_schema/models.py
│   ├── cypher/                   schema.cypher (constraints + indexes)
│   └── mermaid/                  *.mmd per subsystem
│
├── fixtures/
│   ├── valid/                    example instances, one per class
│   └── invalid/                  adversarial instances, must fail validation
│
├── tests/
│   ├── test_schema_valid.py      schema itself is well-formed
│   ├── test_fixtures_valid.py    valid fixtures validate
│   ├── test_fixtures_invalid.py  invalid fixtures reject
│   └── test_emission_parity.py   emitted artifacts match LinkML semantics
│
└── scripts/
    ├── emit.py                   run all emission targets
    └── release.py                version bump + artifact packaging
```

---

## 5. Schema layers

The schema is organized in four layers. Consumers may import the layers they need.

### 5.1 Core layer

Foundation types used by every other layer.

**Entities**: `Disease`, `Symptom`, `Drug`, `Treatment`, `Lab`, `Imaging`, `Procedure`, `Protocol`, `Phenotype`.

**Identifiers**: `ICD11Code`, `ICD10Code`, `SNOMEDCTCode`, `LOINCCode`, `RxNormCode`, `ATCCode`, `OMIMID`, `MeSHID`. Each is a typed string with a validation pattern.

**Core relationships**: `HAS_SYMPTOM` (Disease → Symptom), `TREATED_BY` (Disease → Treatment), `CONTRAINDICATED_IN` (Drug → Condition), `CAUSED_BY` (Disease → Etiology), `MEASURED_BY` (Symptom → Lab/Imaging).

**Core enums**: `DomainVocabulary` (CVS, RSP, RNL, HEM, INF, MET, NEU, GIT, END, IMM — aligned with Biokhor's registry), `CodeSystem`, `EvidenceDirection`, `ConfidenceBasis`.

### 5.2 Epidemiology layer

Regional and population context. Required for any location-aware prior.

**Entities**: `Region` (ISO 3166-2 preferred), `PopulationPrior`.

**Relationships**: `ENDEMIC_IN` (Disease → Region, with prevalence and seasonal multipliers), `PREVALENT_IN`, `RISK_ELEVATED_IN`.

### 5.3 Formulary layer

National drug formulary information. Designed to support BPJS/FORNAS-style coverage metadata without hard-coding any specific national formulary.

**Entities**: `FormularyEntry`, `FormularyTier`.

**Relationships**: `IN_FORMULARY` (Drug → FormularyEntry), `COVERED_BY_TIER` (FormularyEntry → FormularyTier).

### 5.4 Ethnobotany layer (adapter contract only)

The schema defines *what* an ethnobotany adapter emits. It does not define *where* the data comes from or how it is sourced.

**Entity**: `EthnobotanyEntity` — a single entry with fields for plant common name, scientific binomial (linked to a species identifier when available), indication, preparation method, source manuscript reference, provenance hash, license identifier.

**Relationships**: `TRADITIONAL_INDICATION_FOR` (EthnobotanyEntity → Disease/Symptom), `PREPARED_AS` (EthnobotanyEntity → Preparation).

**Adapter contract** (see §7) is the programmatic binding that an external corpus (proprietary or open) implements to populate this layer.

---

## 6. Emission pipeline

One LinkML source, many outputs. The emission is idempotent and runs in CI.

```
         schema/crkg.yaml
                │
                ├── linkml-generate jsonschema → emitted/json-schema/
                ├── linkml-generate pydantic   → emitted/pydantic/
                ├── linkml-generate shacl      → (deferred, post-v1.0)
                ├── linkml-generate owl        → (deferred, post-v1.0)
                ├── custom emitter: cypher-ddl → emitted/cypher/
                └── custom emitter: mermaid    → emitted/mermaid/
```

**Custom emitters** (Cypher DDL, Mermaid) live in `scripts/emitters/`. They consume the LinkML `SchemaView` and produce target-specific output. They are **not** plugins to the LinkML tool itself; keeping them inline keeps the dependency graph flat.

**CI gate**: on every push, the emission runs and the output is compared against the committed `emitted/` directory. Drift fails CI. This prevents an author editing emitted files directly and desynchronizing from the schema.

**Release artifact**: `emitted/` is checked into the repo and included in the sdist/wheel. Consumers do not need a LinkML runtime to use the schema.

---

## 7. Ethnobotany adapter contract

One of the explicit goals of `crkg-schema` is to let proprietary traditional-medicine corpora contribute to clinical reasoning graphs without forcing their internal provenance model into the schema. The adapter contract makes this possible.

### What the schema defines

- The **shape** of an `EthnobotanyEntity` — fields, types, required attributes.
- The **provenance envelope** — every `EthnobotanyEntity` must carry a `source_reference` (free-form URI or identifier), a `license_identifier` (SPDX or free-form), a `provenance_hash` (opaque string, format left to implementer), and a `retrieved_at` timestamp.
- The **adapter interface** — an abstract contract expressed in LinkML as a class with `list_entities()` and `get_entity(id)` conceptual operations. The *binding* to a specific language happens in consumer libraries (`crkg` provides the Python Protocol).

### What the schema does not define

- Where the data comes from
- How the corpus is stored internally
- What cryptographic signing scheme the provenance uses
- Any restrictions on the license identifier (consumers decide what licenses they accept)

### Why this matters

- Proprietary corpora (internal, licensed, or for-pay) can contribute data without exposing their internals.
- Open, public corpora can contribute via a trivial filesystem-backed adapter.
- The graph consuming the entities treats all adapters identically.
- No consuming library needs to special-case any corpus.

The concrete Python Protocol implementing this contract lives in [`crkg`](https://github.com/balinesthesia/crkg) as `TraditionalMedicineAdapter`, not in this repo. `crkg-schema` stays language-agnostic.

---

## 8. Relationship to consuming projects

```
                 ┌────────────────────────────────────────────┐
                 │              crkg-schema                   │
                 │  (this repo; Apache-2.0; schema only)      │
                 └───────────────────┬────────────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
      ┌──────────────┐      ┌──────────────┐       ┌──────────────┐
      │     crkg     │      │ any future   │       │  any future  │
      │  (Python)    │      │  Rust port   │       │   TS port    │
      │  Apache-2.0  │      │   (none yet) │       │   (none yet) │
      └──────┬───────┘      └──────────────┘       └──────────────┘
             │
             │ first concrete consumer
             ▼
      ┌──────────────┐
      │  CDSS apps   │      clinical-rs, multiomics-rs, hl7-rs are siblings, not
      │  and research│      dependencies; they may emit data shaped by this schema
      │   tooling    │      but do not import the schema package
      └──────────────┘
```

- Schema → library → application. One-way. No circular imports, no runtime coupling back.
- A consumer may skip the Python library (`crkg`) and use the emitted JSON Schema directly; that is a fully supported path.

---

## 9. Non-functional targets (post-M1)

- LinkML validation of a 100K-entity corpus: **< 30 s** wall-clock on commodity hardware.
- Emission pipeline cold run: **< 60 s**.
- Schema package sdist size: **< 2 MB** (schema + emitted artifacts + fixtures).
- Public API surface: documented with 100% docstring coverage on the Pydantic models.

Numbers above are aspirational until we have a real corpus to measure. v0.x measurements become v1.0 commitments only after validation.

---

## 10. What this document does not cover

- The `crkg` library's architecture (see [`crkg/ARCHITECTURE.md`](https://github.com/balinesthesia/crkg/blob/main/ARCHITECTURE.md))
- Ingestion pipelines (lives in `crkg`)
- Graph store adapter details (lives in `crkg`)
- Migration from DeepReasoner's `/mkg/` (lives in `crkg/TODO.md`)
- SaMD regulatory posture (lives in the consuming CDSS application)
- Clinical validation of schema content (lives in research protocols per application)

---

## Version log

| Version | Date | Description |
|---|---|---|
| v0.0 | 2026-04-19 | Initial architecture. Design goals, LinkML decision record (D-01..D-05), schema layers sketched, emission pipeline defined, adapter contract specified. No schema content yet. |
