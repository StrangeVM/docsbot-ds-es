from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from docsbot.logging import logger


def chunk_text(
    text: str,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
) -> list[str]:
    """
    Split text into token-aware chunks using recursive chunking.

    Args:
        text: Clean text to split.
        chunk_size: Maximum chunk size in tokens.
        chunk_overlap: Overlapping tokens between chunks.

    Returns:
        List of text chunks.
    """

    if not text.strip():
        logger.warning("Received empty text for chunking.")

        return []

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = text_splitter.split_text(text)

    logger.info(f"Generated {len(chunks)} chunks.")

    return chunks
