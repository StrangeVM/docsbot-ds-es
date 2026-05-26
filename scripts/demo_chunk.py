from pathlib import Path

from docsbot.ingestion.chunk import chunk_text
from docsbot.ingestion.parse import parse_html_file
from docsbot.logging import setup_logging


def main() -> None:
    """
    Manual chunking demo.
    """

    setup_logging()

    html_path = Path("data/raw/pandas/10min.html")

    parsed_doc = parse_html_file(html_path)

    text = parsed_doc["text"]

    chunks = chunk_text(
        text=text,
        chunk_size=512,
        chunk_overlap=50,
    )

    print("\n" + "=" * 80)

    print(f"TITLE: {parsed_doc['title']}")

    print(f"TOTAL CHUNKS: {len(chunks)}")

    print("=" * 80)

    preview_chunks = chunks[:3]

    for index, chunk in enumerate(
        preview_chunks,
        start=1,
    ):
        print(f"\nCHUNK {index}")

        print("-" * 80)

        print(chunk)

        print("-" * 80)


if __name__ == "__main__":
    main()
