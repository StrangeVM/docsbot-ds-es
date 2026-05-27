from docsbot.ingestion.fetch import fetch_pandas_docs
from docsbot.ingestion.parse import parse_html_file
from docsbot.logging import setup_logging

PANDAS_DOC_URLS = [
    "https://pandas.pydata.org/docs/user_guide/10min.html",
    "https://pandas.pydata.org/docs/user_guide/dsintro.html",
    "https://pandas.pydata.org/docs/user_guide/basics.html",
    "https://pandas.pydata.org/docs/user_guide/indexing.html",
    "https://pandas.pydata.org/docs/user_guide/merging.html",
    "https://pandas.pydata.org/docs/user_guide/groupby.html",
    "https://pandas.pydata.org/docs/user_guide/missing_data.html",
    "https://pandas.pydata.org/docs/user_guide/reshaping.html",
]


def main() -> None:
    """
    Manual end-to-end ingestion test.
    """

    print("MAIN IS RUNNING")

    setup_logging()

    downloaded_files = fetch_pandas_docs(PANDAS_DOC_URLS)

    print(f"\nDownloaded {len(downloaded_files)} files.\n")

    successful_pages = 0

    for html_file in downloaded_files:
        print(f"\nProcessing: {html_file}")

        parsed_doc = parse_html_file(html_file)

        title = parsed_doc["title"]

        text = parsed_doc["text"]

        preview = text[:500]

        print("\n" + "=" * 80)

        print(f"TITLE: {title}\n")

        print(preview)

        print("\n" + "=" * 80)

        if text:
            successful_pages += 1

    print(f"\nSuccessfully processed {successful_pages}/{len(downloaded_files)} pages.")


if __name__ == "__main__":
    main()
