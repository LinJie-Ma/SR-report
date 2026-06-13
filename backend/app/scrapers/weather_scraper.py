import logging
from datetime import date
from typing import Any

from .base import BaseScraper

logger = logging.getLogger(__name__)


class WeatherScraper(BaseScraper):
    source = "中国天气网"

    def scrape(self) -> list[dict[str, Any]]:
        logger.info(f"[{self.source}] 天气数据采集需要配置API或解析页面，暂返回空列表")
        return []
