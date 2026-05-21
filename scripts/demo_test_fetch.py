from docsbot.ingestion.fetch import fetch_pandas_docs
from docsbot.logging import setup_logging

TEST_URLS = [
    "https://pandas.pydata.org/docs/user_guide/10min.html",
    "https://pandas.pydata.org/docs/user_guide/groupby.html",
]


def main() -> None:
    """
    Manual test for fetch_pandas_docs.
    """

    setup_logging()

    saved_files = fetch_pandas_docs(TEST_URLS)

    print(f"\nDownloaded {len(saved_files)} files:\n")

    for file_path in saved_files:
        print(file_path)


if __name__ == "__main__":
    main()
