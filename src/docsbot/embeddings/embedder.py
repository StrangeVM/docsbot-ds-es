import numpy as np
from sentence_transformers import SentenceTransformer

from docsbot.logging import logger


class Embedder:
    """
    Wrapper for loading and using the BGE-M3 embedding model.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-m3",
        device: str = "cpu",
    ) -> None:
        """
        Initialize the embedding model.

        Args:
            model_name: Name of the embedding model.
            device: Device to load the model on
                ("cpu" or "cuda").
        """

        logger.info(f"Loading embedding model " f"{model_name} on {device}...")

        self.model = SentenceTransformer(
            model_name,
            device=device,
        )

        self.embedding_dim = self.model.get_embedding_dimension()

        logger.info("Embedding model loaded successfully.")

        logger.info(f"Embedding dimension: " f"{self.embedding_dim}")

    def embed_texts(
        self,
        texts: list[str],
        batch_size: int = 16,
    ) -> np.ndarray:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of texts to embed.
            batch_size: Number of texts to process
                at once.

        Returns:
            Numpy array containing embeddings
            with shape:
            (n_texts, embedding_dimension).
        """

        if not texts:
            logger.warning("Received empty text list for embedding.")

            return np.empty(
                (0, self.embedding_dim),
                dtype=np.float32,
            )

        logger.info(f"Generating embeddings for " f"{len(texts)} texts...")

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            normalize_embeddings=True,
        )

        logger.info("Finished generating embeddings.")

        logger.info(f"Embeddings shape: " f"{embeddings.shape}")

        return embeddings

    def embed_query(
        self,
        query: str,
    ) -> np.ndarray:
        """
        Generate embedding for a single query.

        Args:
            query: Query text.

        Returns:
            Embedding vector with shape:
            (embedding_dimension,).
        """

        embedding = self.embed_texts([query])

        return embedding[0]
