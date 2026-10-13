"""Small safety helpers for target URLs."""
from urllib.parse import urlparse


def validate_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("Please provide a complete http:// or https:// URL.")
    return url
