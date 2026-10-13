"""HTTP and browser fetchers. CAPTCHA/access-denied pages are flagged, not bypassed."""
import random
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from config import USER_AGENTS


class BlockedPageError(RuntimeError):
    """Raised when a page appears to require CAPTCHA or denies access."""


def _check_allowed_scheme(url: str) -> None:
    if urlparse(url).scheme not in {"http", "https"}:
        raise ValueError("Only http:// and https:// URLs are supported.")


def detect_block_page(html: str) -> bool:
    """Conservative text-based detection; may need site-specific tuning."""
    soup = BeautifulSoup(html or "", "html.parser")
    text = soup.get_text(" ", strip=True).lower()
    signals = (
        "verify you are human", "unusual traffic", "captcha",
        "access denied", "automated requests", "checking your browser",
    )
    return any(signal in text for signal in signals)


class Fetcher:
    def __init__(self, timeout: int = 20, delay: float = 1.0):
        self.timeout = timeout
        self.delay = max(0.0, delay)
        self.session = requests.Session()

    def _throttle(self):
        if self.delay:
            time.sleep(self.delay + random.uniform(0, self.delay * 0.25))

    def fetch_requests(self, url: str) -> str:
        _check_allowed_scheme(url)
        self._throttle()
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml",
        }
        response = self.session.get(url, headers=headers, timeout=self.timeout)
        if response.status_code in (401, 403, 429):
            raise BlockedPageError(f"Server returned HTTP {response.status_code} for {url}")
        response.raise_for_status()
        if detect_block_page(response.text):
            raise BlockedPageError(f"Possible CAPTCHA/access-denied page at {url}")
        return response.text

    def fetch_selenium(self, url: str) -> str:
        _check_allowed_scheme(url)
        self._throttle()
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1440,1000")
        # Keep the browser identifiable; do not attempt to hide automation.
        driver = webdriver.Chrome(options=options)
        try:
            driver.set_page_load_timeout(self.timeout)
            driver.get(url)
            try:
                WebDriverWait(driver, min(self.timeout, 10)).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
            except TimeoutException:
                pass
            html = driver.page_source
            if detect_block_page(html):
                raise BlockedPageError(f"Possible CAPTCHA/access-denied page at {url}")
            return html
        finally:
            driver.quit()
