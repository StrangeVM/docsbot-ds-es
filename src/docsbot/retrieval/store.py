from typing import Any

import numpy as np

from docsbot.logging import logger


class NumpyVectorStore:
    """
    Simple in-memory vector store using numpy.
    """

    def __init__(self) -> None:
        """
        Initialize empty vector store.
        """

        self.embeddings: np.ndarray | None = None
        self.texts: list[str] = []
        self.metadata: list[dict] = []

        logger.info("Initialized empty vector store.")

    def add(
        self,
        embeddings: np.ndarray,
        texts: list[str],
        metadata: list[dict[str, Any]],
    ) -> None:
        """
        Add embeddings and associated data
        to the store.

        Args:
            embeddings: Embedding vectors.
            texts: Original texts.
            metadata: Metadata for each text.
        """

        if not (len(embeddings) == len(texts) == len(metadata)):
            raise ValueError("Embeddings, texts, and metadata must have the same length.")

        if self.embeddings is None:
            self.embeddings = embeddings

        else:
            self.embeddings = np.vstack([self.embeddings, embeddings])

        self.texts.extend(texts)
        self.metadata.extend(metadata)

        logger.info(f"Added {len(texts)} documents. Store now contains {len(self)} documents.")

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Search for the most similar documents.

        Assumes embeddings are L2-normalized;
        uses dot product as cosine similarity.

        Args:
            query_embedding: Query embedding vector.
            top_k: Number of results to return.

        Returns:
            List of search results sorted
            by similarity score.
        """

        if self.embeddings is None:
            logger.warning("Search called on empty vector store.")

            return []

        scores = self.embeddings @ query_embedding

        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []

        for i in top_indices:
            results.append(
                {
                    "text": self.texts[i],
                    "metadata": self.metadata[i],
                    "score": float(scores[i]),
                }
            )

        logger.info(f"Retrieved top {len(results)} results.")

        return results

    def __len__(self) -> int:
        """
        Return number of stored documents.
        """

        return len(self.texts)
