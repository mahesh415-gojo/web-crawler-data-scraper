"""Concurrent crawl orchestration."""
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse

from services.fetcher import Fetcher, BlockedPageError
from services.parser import parse_quotes, next_page_url

logger = logging.getLogger(__name__)


def build_page_urls(start_url: str, pages: int) -> list[str]:
    """Build page URLs for the Quotes to Scrape pagination pattern."""
    if pages < 1:
        raise ValueError("--pages must be at least 1")
    urls = [start_url]
    # Practice site uses /page/2/, /page/3/, etc.
    parsed = urlparse(start_url)
    path = parsed.path.rstrip("/")
    if path.endswith("/page/1"):
        path = path[:-len("/page/1")]
    for page_no in range(2, pages + 1):
        page_path = f"{path}/page/{page_no}/"
        urls.append(urlunparse((parsed.scheme, parsed.netloc, page_path, "", parsed.query, "")))
    return urls


def _scrape_one(url: str, mode: str, timeout: int, delay: float):
    fetcher = Fetcher(timeout=timeout, delay=delay)
    try:
        if mode == "selenium":
            html = fetcher.fetch_selenium(url)
        elif mode == "requests":
            html = fetcher.fetch_requests(url)
        else:
            try:
                html = fetcher.fetch_requests(url)
                parsed = parse_quotes(html, url)
                if parsed:
                    return parsed
                logger.info("No records found with Requests; trying Selenium for %s", url)
            except Exception as exc:
                logger.info("Requests fetch failed for %s (%s); trying Selenium", url, exc)
            html = fetcher.fetch_selenium(url)
        return parse_quotes(html, url)
    except BlockedPageError as exc:
        logger.warning("Skipping blocked/CAPTCHA page: %s", exc)
        return []
    except Exception:
        logger.exception("Failed to scrape %s", url)
        return []


def crawl(start_url: str, pages: int = 3, workers: int = 3,
          mode: str = "auto", timeout: int = 20, delay: float = 1.0):
    if workers < 1:
        raise ValueError("--workers must be at least 1")
    if mode not in {"requests", "selenium", "auto"}:
        raise ValueError("mode must be requests, selenium, or auto")
    urls = build_page_urls(start_url, pages)
    records = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_scrape_one, url, mode, timeout, delay): url
            for url in urls
        }
        for future in as_completed(futures):
            records.extend(future.result())
    # De-duplicate by quote + author.
    unique = {}
    for record in records:
        unique[(record.text, record.author)] = record
    return list(unique.values())
