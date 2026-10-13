"""HTML parsing for the Quotes to Scrape practice website."""
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from models.quote import Quote


def parse_quotes(html: str, source_url: str) -> list[Quote]:
    soup = BeautifulSoup(html, "html.parser")
    scraped_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    results = []
    for item in soup.select("div.quote"):
        text_node = item.select_one("span.text")
        author_node = item.select_one("small.author")
        if not text_node or not author_node:
            continue
        tags = [tag.get_text(strip=True) for tag in item.select("a.tag")]
        results.append(Quote(
            text=text_node.get_text(" ", strip=True).strip("“”"),
            author=author_node.get_text(strip=True),
            tags=tags,
            source_url=source_url,
            scraped_at=scraped_at,
        ))
    return results


def next_page_url(html: str, current_url: str) -> str | None:
    from urllib.parse import urljoin
    soup = BeautifulSoup(html, "html.parser")
    link = soup.select_one("li.next a")
    if not link or not link.get("href"):
        return None
    return urljoin(current_url, link["href"])
