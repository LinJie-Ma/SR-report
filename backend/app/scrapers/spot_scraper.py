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

        region_headers = [
            (r'^广西[：:]', '广西'),
            (r'^云南[：:]', '云南'),
            (r'^广东[：:]', '广东'),
            (r'^内蒙古[：:]', '内蒙古'),
            (r'^新疆[：:]', '新疆'),
            (r'^海南[：:]', '海南'),
            (r'^四川[^：:]*[：:]', '四川成都'),
            (r'^河南[^：:]*[：:]', '河南郑州'),
            (r'^天津[：:]', '天津'),
            (r'^河北[^：:]*[：:]', '河北'),
            (r'^辽宁[^：:]*[：:]', '辽宁'),
            (r'^山东[^：:]*[：:]', '山东'),
            (r'^福建[^：:]*[：:]', '福建'),
            (r'^北京[：:]', '北京'),
            (r'^上海[：:]', '上海'),
            (r'^江苏[^：:]*[：:]', '江苏'),
            (r'^浙江[^：:]*[：:]', '浙江'),
            (r'^湖北[^：:]*[：:]', '湖北'),
            (r'^甘肃[^：:]*[：:]', '甘肃'),
            (r'^陕西[^：:]*[：:]', '陕西'),
            (r'^重庆[：:]', '重庆'),
        ]

        price_re = re.compile(r'(\d{4})\s*[-~至]\s*(\d{4})\s*元/吨')

        current_region = None
        seen_regions = set()

        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue

            for header_pattern, region_name in region_headers:
                if re.search(header_pattern, line):
                    current_region = region_name
                    break

            price_match = price_re.search(line)
            if price_match:
                low = int(price_match.group(1))
                high = int(price_match.group(2))
                avg_price = (low + high) / 2

                region = None
                has_region = False
                for header_pattern, region_name in region_headers:
                    if re.search(header_pattern, line):
                        region = region_name
                        has_region = True
                        break

                if not has_region and current_region:
                    region = current_region

                if region and region not in seen_regions:
                    seen_regions.add(region)
                    results.append({
                        "region": region,
                        "price": float(avg_price),
                        "price_date": article_date,
                        "variety": "白砂糖",
                        "source": self.source,
                    })
        return results

    def _collect_links(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "lxml")
        links: list[str] = []
        for a in soup.select("h2 a, h3 a"):
            href = a.get("href", "")
            if href and "/2026/" in href and href not in links:
                links.append(href)
        return links

    def scrape(self) -> list[dict[str, Any]]:
        links: list[str] = []
        for page in range(1, 5):
            url = f"{SPOT_CATEGORY_URL}/page/{page}" if page > 1 else SPOT_CATEGORY_URL
            html = self.fetch(url)
            if not html:
                break
            page_links = self._collect_links(html)
            if not page_links:
                break
            links.extend(page_links)
            logger.info(f"[{self.source}] 现货分类第{page}页: {len(page_links)}篇文章")
        logger.info(f"[{self.source}] 共收集到 {len(links)} 篇现货文章")
        results: list[dict[str, Any]] = []
        for url in links:
            logger.info(f"[{self.source}] 解析现货文章: {url}")
            html = self.fetch(url)
            if html:
                items = self._parse_article(html)
                if items:
                    results.extend(items)
        logger.info(f"[{self.source}] 共解析出 {len(results)} 条现货价格")
        return results
