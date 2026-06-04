# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

* Hybrid search (dense + BM25 retrieval).
* ChromaDB integration for scalable vector storage.
* Retrieval re-ranking layer.
* Expanded evaluation dataset and retrieval experiments.

## [0.2.0] - 2026-06-03

### Added

* Documentation ingestion pipeline with HTML fetching, parsing, and recursive
  chunking.
* HTML parsing using BeautifulSoup with structured extraction of Pandas
  documentation content.
* Recursive chunking strategy using LangChain and tiktoken for token-aware text
  splitting.
* Multilingual embedding module with BGE-M3 and configurable CPU/GPU support.
* Custom `NumpyVectorStore` implementation using vectorized cosine similarity
  search.
* Evaluation framework with `recall_at_k`, `reciprocal_rank`,
  `precision_at_k`, and aggregate metrics.
* Evaluation dataset containing 24 labeled questions (16 English, 8 Spanish;
  12 specific, 12 conceptual).
* Demo scripts for ingestion, chunking, embeddings, retrieval, evaluation, and
  end-to-end RAG execution.
* End-to-end retrieval pipeline integrating fetch, parse, chunk, embed, store,
  and search modules into a single workflow.
* Quantitative baseline results stored in
  `data/eval/baseline_results.json` (Recall@3: 0.9167, MRR: 0.8569).
* Experiment tracking document in `data/eval/experiments.md`.
* ADR-0002 documenting the RAG pipeline architecture and engineering
  decisions.

### Changed

* Project Python version standardized on Python 3.12 for compatibility with
  stable PyTorch releases.
* PyTorch installation configured to use CPU wheels through a dedicated package
  index.
* Ruff version in pre-commit hooks aligned with the project dependency version
  (`0.15.15`).

### Fixed

* Resolved version drift between pre-commit Ruff configuration and project
  Ruff dependency, eliminating formatting inconsistencies between local
  development and CI.

### Dependencies

* `pytest-cov` upgraded from `>=5.0.0` to `>=7.1.0`.
* `ruff` upgraded from `>=0.7.0` to `>=0.15.15`.
* `pydantic-settings` upgraded from `>=2.6.0` to `>=2.14.1`.

### Experiments

* Experiment 01 evaluated removal of Pygments output spans (`gh`, `go`) from
  parsed documentation to reduce retrieval noise.
* Retrieval quality regressed after filtering outputs
  (`Recall@3: 0.9167 → 0.8750`, `MRR: 0.8569 → 0.8257`).
* Change was reverted and documented in `data/eval/experiments.md`.

## [0.1.0] - 2026-05-13

### Added

* Project setup with `uv` and `src/` layout.
* Linting and formatting with `ruff`.
* Pre-commit hooks (trailing whitespace, end-of-file fixer, YAML/TOML
  validation, large files check, private key detection, ruff, ruff-format).
* Test suite with `pytest` and `pytest-cov`.
* Initial smoke tests for package import and version.
* GitHub Actions CI workflow with matrix testing on Python 3.11, 3.12, 3.13.
* GitHub Actions pre-commit workflow.
* Centralized logging with `loguru`, including console and file handlers with
  rotation.
* Typed configuration management with `pydantic-settings`, including
  `SecretStr` for sensitive values.
* `.env.example` template for configuration.
* `.gitattributes` for consistent LF line endings across platforms.
* ADR-0001 documenting choice of `uv` as package manager.
* Dependabot configuration for weekly dependency updates.
* Professional README with problem statement, architecture diagram, stack,
  setup instructions, and roadmap.
* MIT License.

### Infrastructure

* Repository structure: `src/`, `tests/`, `notebooks/`, `scripts/`,
  `configs/`, `data/`, `docs/adr/`, `.github/workflows/`.
* Python 3.11+ requirement.

[Unreleased]: https://github.com/StrangeVM/docsbot-ds-es/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/StrangeVM/docsbot-ds-es/releases/tag/v0.2.0
[0.1.0]: https://github.com/StrangeVM/docsbot-ds-es/releases/tag/v0.1.0
