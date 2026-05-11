# docsbot-ds-es

> Sistema RAG en español para Q&A sobre documentación de Pandas, scikit-learn y NumPy.

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Managed with uv](https://img.shields.io/badge/managed%20with-uv-blueviolet)](https://github.com/astral-sh/uv)

> ⚠️ **Estado:** En desarrollo activo. Sprint 1/4 — setup del proyecto.

---

## 🎯 Problema

La documentación oficial de las librerías más usadas de Data Science (Pandas, scikit-learn, NumPy) está **únicamente en inglés**. Para juniors hispanohablantes, esto representa una barrera diaria que ralentiza el aprendizaje y la productividad.

Las traducciones existentes están desactualizadas y los chatbots generales (ChatGPT, Gemini) suelen alucinar APIs que no existen, mezclando versiones o inventando parámetros.

## 💡 Solución

Un sistema RAG (Retrieval-Augmented Generation) que:

- Indexa la documentación oficial actualizada de Pandas, scikit-learn y NumPy.
- Responde preguntas técnicas en **español natural**.
- Cita siempre la URL exacta de la documentación que respaldó la respuesta (anti-alucinación).
- Permite copiar snippets de código verificados.

## 🏗️ Arquitectura (planificada)

```
[Pregunta usuario]
       ↓
[Embedding query] ──────► [Vector store: ChromaDB]
       ↓                          ↑
[Hybrid retrieval]                │
   (dense + BM25)            [Indexador]
       ↓                          ↑
[Re-ranking]              [Docs oficiales]
       ↓                  (Pandas/sklearn/numpy)
[LLM con context]
       ↓
[Respuesta + citas]
```

## 🔧 Stack técnico

| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.11+ |
| Gestión de paquetes | `uv` |
| Linter + formatter | `ruff` |
| Tests | `pytest` + `pytest-cov` |
| Vector store | ChromaDB *(planeado)* |
| Embeddings | `sentence-transformers` *(planeado)* |
| LLM | OpenAI / local con Ollama *(planeado)* |
| UI | Streamlit *(planeado)* |
| CI/CD | GitHub Actions *(planeado)* |

## 📊 Resultados

*Pendientes — disponibles al final del Sprint 2 (evaluación cuantitativa de estrategias de retrieval).*

## 🚀 Cómo correrlo localmente

### Pre-requisitos

- Python 3.11 o superior
- [uv](https://github.com/astral-sh/uv) instalado

### Setup

```bash
# Clonar el repo
git clone https://github.com/StrangeVM/docsbot-ds-es.git
cd docsbot-ds-es

# Instalar dependencias (incluye dev)
uv sync --all-extras

# Instalar pre-commit hooks
uv run pre-commit install

# Verificar que todo funciona
uv run pytest
```

## 🧪 Desarrollo

```bash
# Correr tests
uv run pytest

# Correr tests con coverage
uv run pytest --cov

# Lintear y formatear código
uv run ruff check .
uv run ruff format .

# Correr todos los pre-commit hooks manualmente
uv run pre-commit run --all-files
```

## 📁 Estructura del proyecto

```
docsbot-ds-es/
├── src/docsbot/         # Código del paquete (instalable)
├── tests/               # Tests con pytest
├── notebooks/           # Notebooks de exploración
├── scripts/             # Scripts ejecutables
├── configs/             # Configuración (YAML/TOML)
├── data/
│   ├── raw/             # Docs descargados (gitignored)
│   └── processed/       # Embeddings, chunks (gitignored)
├── pyproject.toml       # Configuración del proyecto
├── uv.lock              # Lockfile de dependencias
└── .pre-commit-config.yaml
```

## 🗺️ Roadmap

- [x] **Sprint 1 — Setup profesional**: estructura, `uv`, ruff, pre-commit, pytest, CI/CD.
- [ ] **Sprint 2 — Pipeline de ingesta y evaluación**: scraping de docs, chunking, embeddings, eval dataset.
- [ ] **Sprint 3 — RAG avanzado**: hybrid search, re-ranking, structured output con citas.
- [ ] **Sprint 4 — Deploy y agentes**: Streamlit UI, deploy en Hugging Face Spaces, agente con tool use.

## 📝 Decisiones técnicas

Las decisiones de arquitectura y trade-offs están documentados en [`docs/decisions/`](./docs/decisions/) (ADRs — Architecture Decision Records). *Próximamente.*

## 🤝 Autor

**Víctor Rosales** — [LinkedIn](https://www.linkedin.com/in/victor-manuel-rosales-villalpando/) · [GitHub](https://github.com/StrangeVM)

## 📄 Licencia

[MIT](LICENSE)
