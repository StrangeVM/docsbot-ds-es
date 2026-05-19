# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Sprint 2: documentation scraping pipeline, chunking strategies, embeddings,
  vector store setup, golden eval dataset.

## [0.1.0] - 2026-05-13

### Added

- Project setup with `uv` and `src/` layout.
- Linting and formatting with `ruff`.
- Pre-commit hooks (trailing whitespace, end-of-file fixer, YAML/TOML
  validation, large files check, private key detection, ruff, ruff-format).
- Test suite with `pytest` and `pytest-cov`.
- Initial smoke tests for package import and version.
- GitHub Actions CI workflow with matrix testing on Python 3.11, 3.12, 3.13.
- GitHub Actions pre-commit workflow.
- Centralized logging with `loguru`, including console and file handlers with
  rotation.
- Typed configuration management with `pydantic-settings`, including
  `SecretStr` for sensitive values.
- `.env.example` template for configuration.
- `.gitattributes` for consistent LF line endings across platforms.
- ADR-0001 documenting choice of `uv` as package manager.
- Dependabot configuration for weekly dependency updates.
- Professional README with problem statement, architecture diagram, stack,
  setup instructions, and roadmap.
- MIT License.

### Infrastructure

- Repository structure: `src/`, `tests/`, `notebooks/`, `scripts/`,
  `configs/`, `data/`, `docs/adr/`, `.github/workflows/`.
- Python 3.11+ requirement.

[Unreleased]: https://github.com/StrangeVM/docsbot-ds-es/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/StrangeVM/docsbot-ds-es/releases/tag/v0.1.0
