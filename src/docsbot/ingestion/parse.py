import re
from pathlib import Path

from bs4 import BeautifulSoup

from docsbot.logging import logger


def parse_html_file(html_path: Path) -> dict[str, str]:
    """
    Parse a Pandas HTML documentation file and extract clean text.

    Args:
        html_path: Path to the HTML file.

    Returns:
        Dictionary containing title, text, and source_url.
    """

    if not html_path.exists():
        raise FileNotFoundError(f"File does not exist: {html_path}")

    logger.info(f"Parsing HTML file: {html_path}")

    html_content = html_path.read_text(encoding="utf-8")

    soup = BeautifulSoup(
        html_content,
        "lxml",
    )

    main_content = soup.find(
        "article",
        class_="bd-article",
    )

    if main_content is None:
        logger.warning(f"Could not find main article content in: {html_path}")

        return {
            "title": html_path.stem,
            "text": "",
            "source_url": html_path.name,
        }

    for tag in main_content.find_all(["footer"]):
        tag.decompose()

    title_tag = main_content.find("h1")

    title = title_tag.get_text(strip=True) if title_tag else html_path.stem

    text = main_content.get_text(
        separator=" ",
        strip=True,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return {
        "title": title,
        "text": text,
        "source_url": html_path.name,
    }
