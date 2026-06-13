import logging
import re
from datetime import date, datetime
from typing import Any

from bs4 import BeautifulSoup

from .base import BaseScraper

logger = logging.getLogger(__name__)

SPOT_CATEGORY_URL = "https://www.yntw.com/category/xhbj"


class SpotScraper(BaseScraper):
    source = "云南糖网"

    def _parse_article(self, html: str) -> list[dict[str, Any]]:
        soup = BeautifulSoup(html, "lxml")
        body = soup.select_one(".entry-content, .single-content, .post-content, article")
        if not body:
            return []
        text = body.get_text()
        results: list[dict[str, Any]] = []

        date_match = re.search(r'(\d{4})[年.-](\d{1,2})[月.-](\d{1,2})', text)
        if date_match:
            article_date = date(int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3)))
        else:
            article_date = date.today()

        patterns = [
            (r'(广西|云南|广东|内蒙古|新疆|海南)(?:[^：:]*?)[：:].*?(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨', 2),
            (r'(四川[^：:]*?)[：:]?\s*(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨', 2),
            (r'(河南[^：:]*?)[：:]?\s*(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨', 2),
            (r'(天津)[：:]?\s*(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨', 2),
            (r'(河北[^：:]*?)[：:]?\s*(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨', 2),
            (r'(辽宁[^：:]*?)[：:]?\s*(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨', 2),
            (r'(山东[^：:]*?)[：:]?\s*(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨', 2),
            (r'(福建[^：:]*?)[：:]?\s*(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨', 2),
            (r'(北京)[：:]?\s*(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨', 2),
            (r'(上海)[：:]?\s*(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨', 2),
            (r'(江苏[^：:]*?)[：:]?\s*(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨', 2),
            (r'(浙江[^：:]*?)[：:]?\s*(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨', 2),
            (r'(湖北[^：:]*?)[：:]?\s*(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨', 2),
            (r'(湖南[^：:]*?)[：:]?\s*(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨', 2),
            (r'(陕西[^：:]*?)[：:]?\s*(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨', 2),
            (r'(重庆)[：:]?\s*(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨', 2),
            (r'(甘肃[^：:]*?)[：:]?\s*(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨', 2),
        ]

        for line in text.split("\n"):
            line = line.strip()
            if "元/吨" not in line:
                continue
            for pattern, group_count in patterns:
                m = re.search(pattern, line)
                if m:
                    region = m.group(1).strip()
                    low = int(m.group(2))
                    high = int(m.group(3))
                    avg_price = (low + high) / 2
                    results.append({
                        "region": region,
                        "price": float(avg_price),
                        "price_date": article_date,
                        "variety": "白砂糖",
                        "source": self.source,
                    })
                    break
        return results

    def scrape(self) -> list[dict[str, Any]]:
        text = self.fetch(SPOT_CATEGORY_URL)
        if not text:
            return []
        soup = BeautifulSoup(text, "lxml")
        links: list[str] = []
        for a in soup.select("h2 a, h3 a, .post-title a, .entry-title a"):
            href = a.get("href", "")
            if href and "/2026/" in href and href not in links:
                links.append(href)
        if not links:
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/2026/06/" in href and href.endswith(".html") and href not in links:
                    links.append(href)
        results: list[dict[str, Any]] = []
        for url in links[:5]:
            logger.info(f"[{self.source}] 解析现货文章: {url}")
            html = self.fetch(url)
            if html:
                items = self._parse_article(html)
                results.extend(items)
        return results
