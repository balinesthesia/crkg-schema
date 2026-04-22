# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.1] — 2026-04-22

### Added

- Initial repository infrastructure (M0).
- Apache-2.0 license, NOTICE, SECURITY.md, CODE_OF_CONDUCT.md.
- LinkML toolchain with `schema/crkg.yaml` empty-but-valid schema.
- Emission pipeline: JSON Schema, Pydantic, Cypher DDL, Mermaid.
- CI workflow (lint, schema validation, emission parity, fixture tests, build).
- Release workflow (TestPyPI + GitHub Releases).
- Makefile targets: `check`, `test`, `emit`, `fmt`, `lint`.

[Unreleased]: https://github.com/balinesthesia/crkg-schema/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/balinesthesia/crkg-schema/releases/tag/v0.0.1
