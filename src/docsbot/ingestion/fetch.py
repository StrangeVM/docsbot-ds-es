import time
from pathlib import Path
from urllib.parse import urlparse

import httpx

from docsbot.logging import logger


def fetch_pandas_docs(
    urls: list[str],
    output_dir: Path = Path("data/raw/pandas"),
    force: bool = False,
) -> list[Path]:
    """
    Download Pandas documentation pages and save them locally.

    Args:
        urls: List of URLs to download.
        output_dir: Directory where HTML files will be saved.
        force: If True, re-download existing files.

    Returns:
        List of saved file paths.
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []

    for url in urls:
        try:
            parsed_url = urlparse(url)

            filename = Path(parsed_url.path).name

            if not filename.endswith(".html"):
                filename += ".html"

            output_path = output_dir / filename

            if output_path.exists() and not force:
                logger.info(f"Skipping existing file: {output_path}")
                saved_files.append(output_path)
                continue

            logger.info(f"Downloading: {url}")

            response = httpx.get(url, timeout=30)

            response.raise_for_status()

            html = response.text

            output_path.write_text(html, encoding="utf-8")

            logger.info(f"Saved to: {output_path}")

            saved_files.append(output_path)

            time.sleep(1)

        except httpx.HTTPError as e:
            logger.error(f"Failed to download {url}: {e}")

    return saved_files
