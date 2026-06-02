# ADR-0002: RAG Pipeline Architecture for Pandas Documentation

* **Status:** Accepted
* **Date:** 2026-06-02
* **Authors:** Victor Rosales
* **Supersedes:** None
* **Related:** ADR-0001 (Package Management with uv)

---

# Context

The goal of this project is to build a Retrieval-Augmented Generation (RAG) system capable of retrieving relevant information from technical documentation and making it accessible to Spanish-speaking users.

A significant portion of high-quality data science and machine learning documentation is published exclusively in English. While translation tools exist, they do not solve the discovery problem: users must still know where information exists and how to find it. A retrieval system can reduce this barrier by locating the most relevant sections of documentation regardless of the language used in the query.

Sprint 2 focuses exclusively on documentation from the Pandas project. The objective is not to build a production-ready multi-library assistant, but rather to establish and validate the core retrieval architecture, evaluation methodology, and experimentation workflow that will support future expansion to additional libraries.

---

# Decision 1: Chunking Strategy

## Context

Retrieval systems operate on chunks rather than complete documents. Therefore, a decision was required regarding how documentation should be segmented before embedding generation.

Several approaches were considered:

| Strategy           | Advantages                                                   | Disadvantages                              |
| ------------------ | ------------------------------------------------------------ | ------------------------------------------ |
| Fixed-size chunks  | Simple implementation                                        | Ignores document structure                 |
| Semantic chunking  | Better context preservation                                  | More complex and computationally expensive |
| Recursive chunking | Preserves structure while maintaining chunk size constraints | May still split code examples              |

The chunking strategy directly affects retrieval quality because embeddings are generated from chunk content.

## Decision

We selected **recursive chunking** using LangChain's `RecursiveCharacterTextSplitter`.

Configuration:

* Chunk size: **512 tokens**
* Chunk overlap: **50 tokens**
* Token counting: **tiktoken cl100k_base**

The recursive splitter attempts to split content on natural boundaries before falling back to smaller separators, reducing abrupt cuts inside paragraphs.

## Consequences

### Positive

* Preserves document structure better than fixed-size splitting.
* Maintains contextual continuity through overlap.
* Produces chunks of manageable size for embedding generation.
* Easy to tune and widely adopted in RAG systems.

### Negative

* Token counting uses cl100k_base (OpenAI's tokenizer), which differs from BGE-M3's SentencePiece tokenizer. This may result in chunks slightly above or below the intended 512-token limit when measured against the actual embedding model. The discrepancy is typically small and did not warrant additional tooling complexity for Sprint 2.
* Dense code blocks can still be split at suboptimal locations.
* Chunk boundaries remain heuristic rather than semantic.

---

# Decision 2: Embedding Model Selection

## Context

The project required an embedding model capable of:

* Understanding English documentation.
* Supporting Spanish queries.
* Running locally without API costs.
* Producing high-quality semantic representations.
* Being compatible with future experimentation.

Several embedding models were evaluated conceptually, including OpenAI embeddings, E5 variants, multilingual sentence transformers, and BGE family models.

## Decision

We selected **BAAI/bge-m3** as the primary embedding model.

Reasons:

1. Native multilingual support.
2. Strong retrieval performance across public benchmarks.
3. Open-source and free to use locally.
4. Produces 1024-dimensional embeddings.
5. Compatible with CPU-only execution.

## Consequences

### Positive

* Excellent multilingual retrieval capabilities.
* No external API dependency.
* High-quality embeddings suitable for technical documentation.
* Future-proof architecture due to widespread adoption.

### Negative

* Requires approximately 2.27 GB of disk space.
* Initial model download depends on Hugging Face infrastructure.
* CPU inference is relatively slow.

---

# Decision 3: Hardware Target (CPU vs GPU)

## Context

The development environment contains an NVIDIA RTX 5070 GPU based on the Blackwell architecture (sm_120).

At the time of implementation, stable PyTorch releases did not provide reliable support for this architecture. Using GPU acceleration would require experimental builds or compiling dependencies from source.

## Decision

The embedding pipeline was designed to support configurable devices:

```python
Embedder(device="cpu")
Embedder(device="cuda")
```

CPU execution was selected as the default and primary execution path.

The architecture remains prepared for GPU acceleration once stable ecosystem support becomes available.

## Consequences

### Positive

* Pipeline works immediately on supported hardware.
* No dependency on experimental builds.
* Migration to GPU requires no architectural changes.
* Decision is fully reversible.

### Negative

* Embedding generation is slower.
* Available GPU hardware remains underutilized.
* Full corpus embedding requires several minutes on CPU.

---

# Decision 4: Vector Store Implementation

## Context

The system required storage and retrieval of dense vector embeddings.

Available options included:

| Option                      | Advantages                      | Disadvantages         |
| --------------------------- | ------------------------------- | --------------------- |
| NumPy custom implementation | Educational, transparent        | Not scalable          |
| FAISS                       | Extremely fast                  | Additional complexity |
| ChromaDB                    | Persistent, production-friendly | More dependencies     |
| Qdrant                      | Distributed and scalable        | Operational overhead  |

The corpus contained only a few hundred chunks during Sprint 2.

## Decision

We implemented a custom **NumpyVectorStore**.

Reasons:

1. Retrieval mechanics remain fully visible.
2. No external dependencies.
3. Sufficient for approximately 312 chunks.
4. Facilitates understanding before introducing production tooling.

## Consequences

### Positive

* Transparent implementation.
* Easy debugging.
* Minimal dependencies.
* Strong educational value.

### Negative

* Linear search complexity O(n).
* Not suitable for large corpora.
* No metadata filtering.
* No persistence layer.

Future migration to ChromaDB is planned for Sprint 3.

---

# Decision 5: Evaluation Methodology

## Context

Retrieval quality cannot be assessed reliably through intuition alone.

A reproducible evaluation methodology was required to:

* Establish a baseline.
* Compare future improvements.
* Detect regressions.
* Quantify multilingual performance.

## Decision

An evaluation dataset containing **24 manually labeled questions** was created.

Dataset characteristics:

* English and Spanish questions.
* Specific and conceptual question types.
* One expected source document per query.

Metrics:

* Recall@1
* Recall@3
* Recall@5
* Mean Reciprocal Rank (MRR)
* Precision@5

Evaluation occurs at the **document level**, not the chunk level.

Document-level evaluation was preferred over chunk-level evaluation for two
reasons. First, labeling 24 questions against 8 source documents was
tractable, while labeling against approximately 312 chunks would have
required an order of magnitude more manual work. Second, the practical
retrieval question is "does the system find the correct source?" rather
than "does it retrieve the exact paragraph?". Chunk-level evaluation is
deferred to a future sprint if retrieval granularity becomes a bottleneck.

Metrics were implemented in `metrics.py` as pure functions.

## Consequences

### Positive

* Fully reproducible.
* Easy comparison between experiments.
* Captures retrieval coverage and ranking quality.
* Supports language-specific analysis.

### Negative

* Dataset size is small.
* Manual labeling introduces subjectivity.
* Document-level evaluation hides chunk-level nuances.
* Statistical confidence remains limited.

---

# Baseline Results

The initial baseline was measured using the original ingestion pipeline before any filtering experiments.

| Metric      | Value  |
| ----------- | ------ |
| Recall@1    | 0.7917 |
| Recall@3    | 0.9167 |
| Recall@5    | 1.0000 |
| MRR         | 0.8569 |
| Precision@5 | 0.5417 |

### By Language

| Language | N  | Recall@3 | MRR    |
| -------- | -- | -------- | ------ |
| English  | 16 | 0.9375   | 0.8771 |
| Spanish  | 8  | 0.8750   | 0.8167 |

### By Question Type

| Type       | N  | Recall@3 | MRR    |
| ---------- | -- | -------- | ------ |
| Specific   | 12 | 0.8333   | 0.7556 |
| Conceptual | 12 | 1.0000   | 0.9583 |

These values establish the official Sprint 2 retrieval baseline.

---

# Experiments Conducted

## Experiment 01: Filtering Pygments Output Spans

### Hypothesis

Executed outputs embedded inside documentation examples introduce retrieval noise and reduce semantic quality.

By removing HTML spans with classes:

```html
<span class="gh">
<span class="go">
```

the resulting chunks should contain cleaner information and therefore improve retrieval metrics.

### Implementation

A modification was introduced in `parse.py` to remove all output spans before text extraction.

Example:

```python
for span in main_content.find_all(
    "span",
    class_=["gh", "go"],
):
    span.decompose()
```

### Results

| Metric      | Baseline | Filtered | Delta   |
| ----------- | -------- | -------- | ------- |
| Recall@1    | 0.7917   | 0.7500   | -0.0417 |
| Recall@3    | 0.9167   | 0.8750   | -0.0417 |
| Recall@5    | 1.0000   | 1.0000   | 0.0000  |
| MRR         | 0.8569   | 0.8257   | -0.0312 |
| Precision@5 | 0.5417   | 0.5333   | -0.0084 |

### Language Breakdown

| Language | Baseline MRR | Filtered MRR |
| -------- | ------------ | ------------ |
| English  | 0.8771       | 0.8771       |
| Spanish  | 0.8167       | 0.7229       |

### Interpretation

The experiment produced a measurable regression across nearly all metrics.

Contrary to expectations, the removed output spans contained useful contextual information that contributed positively to retrieval quality.

The degradation was especially noticeable for Spanish queries, suggesting that example outputs provided semantic signals helping the multilingual embedding model bridge language gaps.

One plausible explanation is that executed example outputs contain
language-agnostic technical terms such as DatetimeIndex, dtype, NaN,
float64, and freq. These terms appear identically in both English
documentation and Spanish-language queries discussing the same concepts.
As a result, they may act as lexical-semantic anchors that help the
embedding model bridge cross-lingual retrieval. Removing them likely
reduced these matching signals and disproportionately impacted Spanish
performance, where fewer alternative lexical pathways exist.

### Decision

The change was reverted.

The ingestion pipeline will preserve all content contained inside:

```html
<article class="bd-article">
```

unless future experiments demonstrate consistent improvements from selective filtering.

This experiment demonstrates the value of evaluation-driven development: an intuitively appealing change produced objectively worse results.

For complete details, see:

```text
data/eval/experiments.md
```

---

# Open Issues and Future Work

The following limitations remain unresolved:

1. The NumPy vector store does not scale beyond small datasets and should be replaced by ChromaDB in Sprint 3.
2. Hybrid retrieval (dense embeddings + BM25) has not been implemented.
3. No reranking layer currently exists.
4. Test coverage remains incomplete for some pipeline modules.
5. GPU acceleration depends on future stable PyTorch support for Blackwell GPUs.
6. The evaluation dataset contains only 24 questions and should be expanded to approximately 50–100 examples.
7. Chunk-level evaluation is not currently performed.
8. Embedding caching has not yet been implemented.

---

# References

- https://python.langchain.com/docs/modules/data_connection/document_transformers/recursive_text_splitter/
- https://huggingface.co/BAAI/bge-m3
- https://github.com/openai/tiktoken
- ADR-0001: Package Management with uv
- data/eval/experiments.md
- data/eval/baseline_results.json
- Issue #8: Filter executed example outputs from parsed documentation text
