from pathlib import Path

from docsbot.embeddings.embedder import Embedder
from docsbot.ingestion.chunk import chunk_text
from docsbot.ingestion.parse import parse_html_file
from docsbot.logging import setup_logging
from docsbot.retrieval.store import NumpyVectorStore


def main() -> None:
    """
    End-to-end RAG demo pipeline.
    """

    # =========================================================
    # 1. Setup logging
    # =========================================================
    setup_logging()

    # =========================================================
    # 2. INGESTA OFFLINE
    # =========================================================

    # Directorio donde están los HTML descargados
    data_dir = Path("data/raw/pandas")

    # Obtener todos los archivos .html
    html_files = list(data_dir.glob("*.html"))

    print("\nFound HTML files:")
    print(f"{len(html_files)} files")

    # ---------------------------------------------------------
    # Listas paralelas para construir el knowledge base
    # ---------------------------------------------------------
    all_texts: list[str] = []

    all_metadata: list[dict] = []

    total_chunks = 0

    # ---------------------------------------------------------
    # Procesar cada archivo HTML
    # ---------------------------------------------------------
    for html_file in html_files:
        # Parsear HTML
        parsed = parse_html_file(html_file)

        title = parsed["title"]

        text = parsed["text"]

        source_url = parsed["source_url"]

        # Chunking
        chunks = chunk_text(text)

        # -----------------------------------------------------
        # Guardar cada chunk + metadata
        # -----------------------------------------------------
        for chunk in chunks:
            all_texts.append(chunk)

            all_metadata.append(
                {
                    "title": title,
                    "source_url": source_url,
                }
            )

        total_chunks += len(chunks)

    # ---------------------------------------------------------
    # Resumen de ingesta
    # ---------------------------------------------------------
    print("\nIngestion Summary")
    print("=" * 80)

    print(f"Processed files: {len(html_files)}")

    print(f"Total chunks: {total_chunks}")

    # =========================================================
    # 3. EMBEDDINGS
    # =========================================================

    print("\nLoading embedding model...")
    print("=" * 80)

    embedder = Embedder()

    print("\nGenerating embeddings...")
    print("=" * 80)

    embeddings = embedder.embed_texts(all_texts)

    print("\nEmbeddings shape:")
    print(embeddings.shape)

    # =========================================================
    # 4. VECTOR STORE
    # =========================================================

    print("\nCreating vector store...")
    print("=" * 80)

    store = NumpyVectorStore()

    store.add(
        embeddings=embeddings,
        texts=all_texts,
        metadata=all_metadata,
    )

    print(f"\nStore size: {len(store)}")

    # =========================================================
    # 5. CONSULTAS
    # =========================================================

    questions = [
        "How do I fill missing values in a DataFrame?",
        "How can I group data by a column?",
        "What is a DataFrame?",
    ]

    for question in questions:
        print("\n")
        print("=" * 80)

        print(f"QUESTION:\n{question}")

        print("=" * 80)

        # -----------------------------------------------------
        # Embeddear query
        # -----------------------------------------------------
        query_embedding = embedder.embed_query(question)

        # -----------------------------------------------------
        # Buscar top chunks
        # -----------------------------------------------------
        results = store.search(
            query_embedding=query_embedding,
            top_k=3,
        )

        # -----------------------------------------------------
        # Mostrar resultados
        # -----------------------------------------------------
        for idx, result in enumerate(
            results,
            start=1,
        ):
            print("\n" + "-" * 80)

            print(f"Result #{idx}")

            print(f"Score: {result['score']:.4f}")

            print(f"Title: " f"{result['metadata']['title']}")

            print(f"Source: " f"{result['metadata']['source_url']}")

            chunk_text_preview = result["text"]

            snippet = (
                chunk_text_preview[:200] + "..."
                if len(chunk_text_preview) > 200
                else chunk_text_preview
            )

            print("\nSnippet:")

            print(snippet)

    print("\n")
    print("=" * 80)

    print("RAG demo completed successfully.")

    print("=" * 80)


if __name__ == "__main__":
    main()
