import json
from pathlib import Path

from docsbot.embeddings.embedder import Embedder
from docsbot.evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)
from docsbot.ingestion.chunk import chunk_text
from docsbot.ingestion.parse import parse_html_file
from docsbot.logging import logger, setup_logging
from docsbot.retrieval.store import NumpyVectorStore


def average_metric(
    results: list[dict],
    metric_name: str,
) -> float:
    """
    Compute the average value of a metric.

    Args:
        results: List of evaluation result dictionaries.
        metric_name: Metric key to average.

    Returns:
        Average metric value.
    """

    if not results:
        return 0.0

    return sum(result[metric_name] for result in results) / len(results)


def build_knowledge_base() -> tuple[
    list[str],
    list[dict],
]:
    """
    Build the knowledge base from local HTML files.

    Returns:
        Tuple containing:
        - all_texts
        - all_metadata
    """

    html_files = sorted(Path("data/raw/pandas").glob("*.html"))

    all_texts: list[str] = []
    all_metadata: list[dict] = []

    total_chunks = 0

    logger.info(f"Found {len(html_files)} HTML files.")

    for html_file in html_files:
        logger.info(f"Processing file: {html_file.name}")

        parsed_document = parse_html_file(html_file)

        title = parsed_document["title"]
        text = parsed_document["text"]
        source_url = parsed_document["source_url"]

        chunks = chunk_text(text)

        for chunk in chunks:
            all_texts.append(chunk)

            all_metadata.append(
                {
                    "title": title,
                    "source_url": source_url,
                }
            )

        total_chunks += len(chunks)

    logger.info(f"Processed {len(html_files)} files into {total_chunks} chunks.")

    return all_texts, all_metadata


def print_report(
    all_results: list[dict],
) -> None:
    """
    Print the final evaluation report.

    Args:
        all_results: List of evaluation results.
    """

    overall_recall_1 = average_metric(
        all_results,
        "recall_1",
    )

    overall_recall_3 = average_metric(
        all_results,
        "recall_3",
    )

    overall_recall_5 = average_metric(
        all_results,
        "recall_5",
    )

    overall_mrr = average_metric(
        all_results,
        "mrr",
    )

    overall_precision_5 = average_metric(
        all_results,
        "precision_5",
    )

    english_results = [result for result in all_results if result["language"] == "en"]

    spanish_results = [result for result in all_results if result["language"] == "es"]

    specific_results = [result for result in all_results if result["type"] == "specific"]

    conceptual_results = [result for result in all_results if result["type"] == "conceptual"]

    print("\n")
    print("=" * 80)
    print("BASELINE RAG EVALUATION REPORT")
    print("=" * 80)

    print(f"\nTotal questions evaluated: {len(all_results)}")

    print("\nOVERALL METRICS")
    print("-" * 80)

    print(f"Recall@1: {overall_recall_1:.4f}")

    print(f"Recall@3: {overall_recall_3:.4f}")

    print(f"Recall@5: {overall_recall_5:.4f}")

    print(f"MRR: {overall_mrr:.4f}")

    print(f"Precision@5: {overall_precision_5:.4f}")

    print("\nBY LANGUAGE")
    print("-" * 80)

    print(
        f"English (N={len(english_results)}): "
        f"Recall@3="
        f"{average_metric(english_results, 'recall_3'):.4f} | "
        f"MRR="
        f"{average_metric(english_results, 'mrr'):.4f}"
    )

    print(
        f"Spanish (N={len(spanish_results)}): "
        f"Recall@3="
        f"{average_metric(spanish_results, 'recall_3'):.4f} | "
        f"MRR="
        f"{average_metric(spanish_results, 'mrr'):.4f}"
    )

    print("\nBY TYPE")
    print("-" * 80)

    print(
        f"Specific (N={len(specific_results)}): "
        f"Recall@3="
        f"{average_metric(specific_results, 'recall_3'):.4f} | "
        f"MRR="
        f"{average_metric(specific_results, 'mrr'):.4f}"
    )

    print(
        f"Conceptual (N={len(conceptual_results)}): "
        f"Recall@3="
        f"{average_metric(conceptual_results, 'recall_3'):.4f} | "
        f"MRR="
        f"{average_metric(conceptual_results, 'mrr'):.4f}"
    )

    print("=" * 80)


def main() -> None:
    """
    Run the full RAG evaluation pipeline.
    """

    setup_logging()

    logger.info("Loading evaluation dataset...")

    eval_path = Path("data/eval/eval_questions.json")

    eval_dataset = json.loads(eval_path.read_text(encoding="utf-8"))

    logger.info(f"Loaded {len(eval_dataset)} evaluation questions.")

    logger.info("Building knowledge base...")

    all_texts, all_metadata = build_knowledge_base()

    logger.info("Loading embedding model...")

    embedder = Embedder()

    logger.info("Generating embeddings for all chunks...")

    embeddings = embedder.embed_texts(all_texts)

    logger.info("Creating vector store...")

    store = NumpyVectorStore()

    store.add(
        embeddings=embeddings,
        texts=all_texts,
        metadata=all_metadata,
    )

    logger.info(f"Vector store contains {len(store)} chunks.")

    logger.info("Starting evaluation...")

    all_results: list[dict] = []

    for item in eval_dataset:
        question = item["question"]
        expected_doc = item["expected_doc"]
        language = item["language"]
        question_type = item["type"]

        logger.info(f"Evaluating question: {question}")

        query_embedding = embedder.embed_query(question)

        search_results = store.search(
            query_embedding=query_embedding,
            top_k=5,
        )

        retrieved_docs = [result["metadata"]["source_url"] for result in search_results]

        recall_1 = recall_at_k(
            retrieved_docs=retrieved_docs,
            expected_doc=expected_doc,
            k=1,
        )

        recall_3 = recall_at_k(
            retrieved_docs=retrieved_docs,
            expected_doc=expected_doc,
            k=3,
        )

        recall_5 = recall_at_k(
            retrieved_docs=retrieved_docs,
            expected_doc=expected_doc,
            k=5,
        )

        mrr = reciprocal_rank(
            retrieved_docs=retrieved_docs,
            expected_doc=expected_doc,
            k=5,
        )

        precision_5 = precision_at_k(
            retrieved_docs=retrieved_docs,
            expected_doc=expected_doc,
            k=5,
        )

        result = {
            "question": question,
            "expected_doc": expected_doc,
            "language": language,
            "type": question_type,
            "recall_1": recall_1,
            "recall_3": recall_3,
            "recall_5": recall_5,
            "mrr": mrr,
            "precision_5": precision_5,
        }

        all_results.append(result)

    logger.info("Evaluation completed.")

    output_path = Path("data/eval/baseline_results.json")

    output_path.write_text(
        json.dumps(
            all_results,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    logger.info(f"Saved evaluation results to {output_path}")

    print_report(all_results)


if __name__ == "__main__":
    main()
