import numpy as np

from docsbot.logging import setup_logging
from docsbot.retrieval.store import NumpyVectorStore


def normalize(arr: np.ndarray) -> np.ndarray:
    """
    Normalize each vector to have length 1.

    Args:
        arr: Array of vectors.

    Returns:
        Normalized array.
    """

    norms = np.linalg.norm(
        arr,
        axis=1,
        keepdims=True,
    )

    return arr / norms


def main() -> None:
    """
    Demo script for testing NumpyVectorStore.
    """

    # ---------------------------------------------------------
    # 1. Configurar logging
    # ---------------------------------------------------------
    setup_logging()

    # ---------------------------------------------------------
    # 2. Crear el store vacío
    # ---------------------------------------------------------
    store = NumpyVectorStore()

    # ---------------------------------------------------------
    # 3. Verificar tamaño inicial
    # ---------------------------------------------------------
    print("\nInitial store size:")
    print(len(store))

    # ---------------------------------------------------------
    # 4. Crear embeddings sintéticos normalizados
    # ---------------------------------------------------------
    np.random.seed(42)

    embeddings = np.random.randn(3, 8)

    embeddings = normalize(embeddings)

    print("\nSynthetic embeddings shape:")
    print(embeddings.shape)

    # ---------------------------------------------------------
    # 5. Crear textos y metadata
    # ---------------------------------------------------------
    texts = [
        "Pandas DataFrame basics",
        "How to handle missing values",
        "GroupBy operations in pandas",
    ]

    metadata = [
        {
            "title": "DataFrame Basics",
            "source_url": "basics.html",
        },
        {
            "title": "Missing Data",
            "source_url": "missing_data.html",
        },
        {
            "title": "GroupBy Guide",
            "source_url": "groupby.html",
        },
    ]

    # ---------------------------------------------------------
    # 6. Agregar datos al store
    # ---------------------------------------------------------
    store.add(
        embeddings=embeddings,
        texts=texts,
        metadata=metadata,
    )

    # ---------------------------------------------------------
    # 7. Verificar tamaño después del add
    # ---------------------------------------------------------
    print("\nStore size after add:")
    print(len(store))

    # ---------------------------------------------------------
    # 8. Crear query embedding sintético
    # ---------------------------------------------------------
    query_embedding = np.random.randn(1, 8)

    query_embedding = normalize(query_embedding)

    query_embedding = query_embedding[0]

    # ---------------------------------------------------------
    # 9. Buscar top_k resultados
    # ---------------------------------------------------------
    results = store.search(
        query_embedding=query_embedding,
        top_k=2,
    )

    print("\nSearch Results:")
    print("=" * 60)

    for idx, result in enumerate(results, start=1):
        print(f"\nResult {idx}")

        print(f"Text: {result['text']}")

        print(f"Metadata: {result['metadata']}")

        print(f"Score: {result['score']:.4f}")

    # ---------------------------------------------------------
    # 10. Probar búsqueda en store vacío
    # ---------------------------------------------------------
    empty_store = NumpyVectorStore()

    empty_results = empty_store.search(
        query_embedding=query_embedding,
        top_k=2,
    )

    print("\nEmpty store search:")
    print(empty_results)

    # ---------------------------------------------------------
    # 11. Probar validación de longitudes
    # ---------------------------------------------------------
    print("\nTesting validation error:")

    try:
        bad_embeddings = normalize(np.random.randn(2, 8))

        bad_texts = [
            "Only one text",
        ]

        bad_metadata = [
            {"title": "Test 1"},
            {"title": "Test 2"},
        ]

        store.add(
            embeddings=bad_embeddings,
            texts=bad_texts,
            metadata=bad_metadata,
        )

    except ValueError as e:
        print(f"Caught expected ValueError: {e}")


if __name__ == "__main__":
    main()
