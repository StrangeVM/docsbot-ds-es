from docsbot.embeddings.embedder import Embedder
from docsbot.logging import setup_logging


def main() -> None:
    """
    Manual embedding demo script.
    """

    setup_logging()

    embedder = Embedder()

    texts = [
        "pandas DataFrame",
        "how to fill missing values",
        "el gato come pescado",
    ]

    embeddings = embedder.embed_texts(texts)

    print("\n" + "=" * 80)

    print("EMBEDDING RESULTS")

    print("=" * 80)

    print(f"\nEmbeddings shape: {embeddings.shape}")

    print("\nFirst embedding (first 10 values):")

    print(embeddings[0][:10])

    print("\nEmbedding dtype:")

    print(embeddings.dtype)

    print("\nDone.")


if __name__ == "__main__":
    main()
