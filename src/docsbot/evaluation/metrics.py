from docsbot.logging import logger


def recall_at_k(
    retrieved_docs: list[str],
    expected_doc: str,
    k: int,
) -> float:
    """
    Compute Recall@K for a single query.

    Recall@K answers:
    "Was the correct document retrieved in the top-k results?"

    Args:
        retrieved_docs: Retrieved document names in ranked order.
        expected_doc: Expected correct document.
        k: Number of top results to consider.

    Returns:
        1.0 if expected_doc is in top-k results, else 0.0.
    """

    top_k_docs = retrieved_docs[:k]

    return 1.0 if expected_doc in top_k_docs else 0.0


def reciprocal_rank(
    retrieved_docs: list[str],
    expected_doc: str,
    k: int,
) -> float:
    """
    Compute Reciprocal Rank (RR) for a single query.

    Reciprocal Rank measures how high the first correct result appears.

    Examples:
        Rank 1 -> 1.0
        Rank 2 -> 0.5
        Rank 3 -> 0.333
        Not found -> 0.0

    Args:
        retrieved_docs: Retrieved document names in ranked order.
        expected_doc: Expected correct document.
        k: Number of top results to consider.

    Returns:
        Reciprocal rank score.
    """

    top_k_docs = retrieved_docs[:k]

    for rank, doc in enumerate(top_k_docs, start=1):
        if doc == expected_doc:
            return 1.0 / rank

    return 0.0


def precision_at_k(
    retrieved_docs: list[str],
    expected_doc: str,
    k: int,
) -> float:
    """
    Compute Precision@K for a single query.

    Precision@K answers:
    "What fraction of the top-k results are correct?"

    Args:
        retrieved_docs: Retrieved document names in ranked order.
        expected_doc: Expected correct document.
        k: Number of top results to consider.

    Returns:
        Precision score between 0.0 and 1.0.
    """

    top_k_docs = retrieved_docs[:k]

    if not top_k_docs:
        return 0.0

    matches = sum(1 for doc in top_k_docs if doc == expected_doc)

    return matches / len(top_k_docs)


def aggregate_metrics(
    all_results: list[dict[str, float]],
) -> dict[str, float]:
    """
    Aggregate evaluation metrics across multiple queries.

    Args:
        all_results: List of metric dictionaries for each query.

    Returns:
        Dictionary containing average metrics.
    """

    if not all_results:
        logger.warning("No evaluation results provided for aggregation.")

        return {
            "avg_recall": 0.0,
            "avg_mrr": 0.0,
            "avg_precision": 0.0,
        }

    total_queries = len(all_results)

    avg_recall = sum(result["recall"] for result in all_results) / total_queries

    avg_mrr = sum(result["mrr"] for result in all_results) / total_queries

    avg_precision = sum(result["precision"] for result in all_results) / total_queries

    metrics = {
        "avg_recall": avg_recall,
        "avg_mrr": avg_mrr,
        "avg_precision": avg_precision,
    }

    logger.info(f"Aggregated metrics across {total_queries} queries.")

    return metrics
