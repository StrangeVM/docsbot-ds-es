# ADR-0001: Package management with uv

- **Status:** Accepted
- **Date:** 2026-05-19
- **Authors:** Victor Rosales

## Context

We need a package manager for this Python project to handle:

- Dependency installation (production and development).
- Virtual environment management.
- Python version pinning.
- Reproducible builds via lockfile.
- Fast CI runs (cached installs).

The Python ecosystem has multiple options:

| Tool | Pros | Cons |
|---|---|---|
| `pip` + `venv` | Standard, ubiquitous | No lockfile, slow, manual venv management |
| `poetry` | Mature, popular, lockfile | Slow, complex config, sometimes opinionated |
| `pipenv` | Lockfile, simple | Slow, less maintained |
| `pdm` | Modern, PEP-compliant | Smaller ecosystem |
| `uv` | 10-100x faster, lockfile, Python install, drop-in pip replacement | Newer (released 2024), smaller community than poetry |

## Decision

We will use **`uv`** as the sole package and Python version manager for this
project.

Reasons:

1. **Speed**: `uv sync` runs 10-100x faster than `poetry install` or `pip
   install`, which significantly reduces CI time and local iteration cycles.
2. **Lockfile**: `uv.lock` provides reproducible builds, same guarantee as
   poetry.
3. **Python management**: `uv python install` replaces `pyenv`, removing a
   dependency.
4. **Industry trajectory**: Adopted by Pydantic, Hugging Face, and other
   major Python projects in 2025-2026. Standard in the field by 2026.
5. **Built by Astral**: same team behind `ruff`, indicating consistent
   high-quality tooling.

## Consequences

### Positive

- Fast local installs and CI runs.
- Single tool replaces `pip`, `venv`, `pyenv`, `poetry`.
- Reproducibility guaranteed via `uv.lock` committed to repo.
- Less cognitive overhead for new contributors.

### Negative

- Smaller community than poetry; some niche issues may have fewer Stack
  Overflow answers.
- Newer tool; potential breaking changes in 0.x versions.
- Some legacy tooling (e.g., older `tox` configs) may need adaptation.

### Mitigations

- Pin specific uv version in CI (`astral-sh/setup-uv@v8.1.0`) to avoid
  surprise breaking changes.
- Document setup commands clearly in README for new contributors.

## References

- [uv official docs](https://docs.astral.sh/uv/)
- [Astral blog: announcing uv](https://astral.sh/blog/uv)
