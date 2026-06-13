import logging
from abc import ABC, abstractmethod
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    source: str = ""
    timeout: int = 30

    def __init__(self):
        self.client = httpx.Client(timeout=self.timeout, follow_redirects=True)

    def fetch(self, url: str) -> str | None:
        try:
            resp = self.client.get(url)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            logger.error(f"[{self.source}] 请求失败 {url}: {e}")
            return None

    @abstractmethod
    def scrape(self) -> list[dict[str, Any]]:
        ...
