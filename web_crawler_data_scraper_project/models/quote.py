"""Structured model for one quote record."""
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class Quote:
    text: str
    author: str
    tags: List[str]
    source_url: str
    scraped_at: str

    def to_dict(self) -> dict:
        return asdict(self)
