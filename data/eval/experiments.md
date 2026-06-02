# Experiments Log — docsbot-ds-es

This file documents experiments conducted on the RAG system, with hypotheses,
results, and decisions. All experiments are measured against the baseline
defined in `baseline_results.json` using the eval dataset in
`eval_questions.json` (24 questions, bilingual, mixed conceptual/specific).

---

## Baseline (no filtering)

**Date:** 2026-06-02
**Pipeline config:** fetch + parse + recursive chunking (512 tokens, 50 overlap)
+ BGE-M3 embeddings + NumpyVectorStore + cosine similarity.

**Results file:** `baseline_results.json`

| Metric | Value |
|---|---|
| Recall@1 | 0.7917 |
| Recall@3 | 0.9167 |
| Recall@5 | 1.0000 |
| MRR | 0.8569 |
| Precision@5 | 0.5417 |
| English Recall@3 | 0.9375 |
| Spanish Recall@3 | 0.8750 |
| Specific Recall@3 | 0.8333 |
| Conceptual Recall@3 | 1.0000 |

**Knowledge base:** 312 chunks from 8 Pandas documentation pages.

**Notes:** Specific questions perform worse than conceptual ones
(unexpected). Spanish performs slightly worse than English (expected,
since source docs are in English). Recall@5 reaches 100%, suggesting
the system always retrieves the correct document within top 5 — the
opportunity is improving ranking (recall@1, MRR), not coverage.

---

## Experiment 01 — Filter executed output spans

**Date:** 2026-06-02
**Hypothesis:** Removing executed output content from Pandas documentation
(spans with classes `gh` and `go` in Pygments) would reduce noise in chunks
and improve retrieval metrics, especially for specific questions.

**Implementation:** Added a step in `parse_html_file` that removes all
`<span class="gh">` and `<span class="go">` elements from the article
before extracting text. This eliminates `Out[N]:` prompts and the actual
output content (e.g., random number tables, DatetimeIndex listings).

**Effect on data:** Reduced chunks from 312 to 178 (-43%). Removed
approximately 7,000 spans across 8 documents.

**Results file:** `experiment_01_filter_outputs.json`

| Metric | Baseline | Experiment 01 | Delta |
|---|---|---|---|
| Recall@1 | 0.7917 | 0.7500 | **-4.17 pts** |
| Recall@3 | 0.9167 | 0.8750 | **-4.17 pts** |
| Recall@5 | 1.0000 | 1.0000 | = |
| MRR | 0.8569 | 0.8257 | **-3.12 pts** |
| Precision@5 | 0.5417 | 0.5333 | -0.84 pts |
| English Recall@3 | 0.9375 | 0.9375 | = |
| **Spanish Recall@3** | 0.8750 | 0.7500 | **-12.50 pts** |
| Specific Recall@3 | 0.8333 | 0.8333 | = |
| **Conceptual Recall@3** | 1.0000 | 0.9167 | **-8.33 pts** |

**Outcome:** Metrics dropped across the board. Recall@5 unchanged
(still 100%), but ranking quality degraded.

**Possible explanations (post-hoc analysis):**

1. Output spans contained universal technical terms (`DatetimeIndex`,
   `dtype`, `NaN`, `float64`, `freq`, etc.) that helped the embedding
   model identify the topic of a chunk. Removing them reduced semantic
   signal.
2. Output content reinforced the context of the preceding input code.
   `In [5]: dates = pd.date_range(...)` is more ambiguous without the
   `Out[5]: DatetimeIndex(...)` that confirms the chunk is about date
   ranges.
3. The largest drop occurred in Spanish (-12.5 pts) and conceptual
   (-8.33 pts) questions. Hypothesis: those questions rely more on
   semantic cross-language matching, and the technical English terms
   in outputs were anchoring matches for translations.
4. Chunking redistributed content: with shorter inputs (code only),
   the recursive splitter grouped material differently, changing what
   information lands together in each chunk. This is a second-order
   effect of the filter.

**Decision:** Revert the filter. The intuition that outputs were "noise"
was visual, not measurable. The data shows they contribute useful signal
to retrieval. Filtering them is contraindicated.

**Lessons learned:**

- Visual noise ≠ retrieval noise. Embeddings extract signal from content
  that looks ugly to humans.
- Always measure before optimizing. Intuition about what is "useful" in
  text-for-embeddings can be wrong.
- Cross-lingual retrieval benefits from universal technical terms;
  filtering them disproportionately harms non-English queries.
- This negative result is itself valuable: it eliminates a "default
  optimization" assumption and documents the actual behavior of the
  system.

**Related:** Issue #8 (filter executed example outputs). Closing the
issue with reference to this experiment.