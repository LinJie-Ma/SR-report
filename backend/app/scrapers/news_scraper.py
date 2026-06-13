import logging
from datetime import datetime
from typing import Any

from bs4 import BeautifulSoup

from .base import BaseScraper

logger = logging.getLogger(__name__)

NEWS_CATEGORY_URL = "https://www.yntw.com"


class NewsScraper(BaseScraper):
    source = "云南糖网"

    def scrape(self) -> list[dict[str, Any]]:
        text = self.fetch(NEWS_CATEGORY_URL)
        if not text:
            return []
        soup = BeautifulSoup(text, "lxml")
        results: list[dict[str, Any]] = []
        seen_urls = set()

        for a in soup.select("h2 a, h3 a"):
            href = a.get("href", "")
            if not href or href in seen_urls:
                continue
            seen_urls.add(href)
            title = a.get_text(strip=True)
            if not title or len(title) < 4:
                continue

            parent = a.parent.parent if a.parent else None
            summary = None
            if parent:
                excerpt = parent.select_one(".item-excerpt, .excerpt, .summary, p")
                if excerpt:
                    summary = excerpt.get_text(strip=True)

            publish_date = datetime.now()
            time_tag = soup.select_one("time[datetime]")
            if not time_tag and parent:
                time_tag = parent.select_one("time, .item-meta time, .date")
            if time_tag:
                dt = time_tag.get("datetime", "")
                if not dt:
                    dt = time_tag.get_text(strip=True)
                try:
                    if "T" in dt:
                        publish_date = datetime.fromisoformat(dt.replace("Z", "+00:00"))
                except ValueError:
                    pass

            results.append({
                "title": title[:500],
                "content": None,
                "summary": summary[:1000] if summary else None,
                "url": href,
                "publish_date": publish_date,
                "source": self.source,
            })
        return results
