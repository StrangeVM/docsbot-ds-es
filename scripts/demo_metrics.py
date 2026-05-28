from docsbot.evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)
from docsbot.logging import setup_logging


def main() -> None:
    """
    Manual demo for retrieval evaluation metrics.
    """

    setup_logging()

    # ============================================================
    # Example retrieval results
    # ============================================================

    retrieved_docs = [
        "dsintro.html",
        "missing_data.html",
        "basics.html",
    ]

    expected_doc = "missing_data.html"

    print("\n" + "=" * 60)
    print("RETRIEVAL RESULTS")
    print("=" * 60)

    print(f"Retrieved docs: {retrieved_docs}")
    print(f"Expected doc:   {expected_doc}")

    # ============================================================
    # Recall@K
    # ============================================================

    recall_k1 = recall_at_k(
        retrieved_docs=retrieved_docs,
        expected_doc=expected_doc,
        k=1,
    )

    recall_k3 = recall_at_k(
        retrieved_docs=retrieved_docs,
        expected_doc=expected_doc,
        k=3,
    )

    print("\n" + "=" * 60)
    print("RECALL@K")
    print("=" * 60)

    print(f"Recall@1: {recall_k1}")
    print(f"Recall@3: {recall_k3}")

    # ============================================================
    # Reciprocal Rank
    # ============================================================

    rr = reciprocal_rank(
        retrieved_docs=retrieved_docs,
        expected_doc=expected_doc,
        k=3,
    )

    print("\n" + "=" * 60)
    print("RECIPROCAL RANK")
    print("=" * 60)

    print(f"RR@3: {rr}")

    # ============================================================
    # Precision@K
    # ============================================================

    precision = precision_at_k(
        retrieved_docs=retrieved_docs,
        expected_doc=expected_doc,
        k=3,
    )

    print("\n" + "=" * 60)
    print("PRECISION@K")
    print("=" * 60)

    print(f"Precision@3: {precision}")

    print("\nDone.")


if __name__ == "__main__":
    main()
