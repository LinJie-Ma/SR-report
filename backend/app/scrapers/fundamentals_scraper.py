import logging
from typing import Any

from .base import BaseScraper

logger = logging.getLogger(__name__)


class FundamentalsScraper(BaseScraper):
    source = "中国糖业协会"

    def scrape(self) -> list[dict[str, Any]]:
        logger.info(f"[{self.source}] 基本面数据需要从公开渠道获取，暂返回空列表")
        return []
