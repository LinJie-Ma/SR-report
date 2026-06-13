import json
import logging
import re
from datetime import date, timedelta
from typing import Any

from .base import BaseScraper

logger = logging.getLogger(__name__)


class FuturesScraper(BaseScraper):
    source = "新浪财经"

    def _parse_day_kline(self, text: str, code: str) -> list[dict[str, Any]]:
        json_match = re.search(r'\(\s*(\[.*\])\s*\)', text, re.DOTALL)
        if json_match:
            try:
                records = json.loads(json_match.group(1))
                results: list[dict[str, Any]] = []
                for r in records:
                    results.append({
                        "trade_date": date.fromisoformat(r["d"]),
                        "open": float(r["o"]),
                        "high": float(r["h"]),
                        "low": float(r["l"]),
                        "close": float(r["c"]),
                        "volume": int(r["v"]),
                        "open_interest": int(r.get("p", 0)),
                    })
                return results
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                logger.error(f"[{self.source}] JSON解析失败: {e}")

        pattern = re.compile(rf'"{code}"\s*:\s*"(.*?)"')
        match = pattern.search(text)
        if not match:
            return []
        data_str = match.group(1)
        items = data_str.split("|")
        results: list[dict[str, Any]] = []
        for item in items:
            parts = item.split(",")
            if len(parts) < 6:
                continue
            try:
                results.append({
                    "trade_date": date.fromisoformat(parts[0]),
                    "open": float(parts[1]),
                    "high": float(parts[2]),
                    "low": float(parts[3]),
                    "close": float(parts[4]),
                    "volume": int(parts[5]),
                    "open_interest": int(parts[6]) if len(parts) > 6 else 0,
                })
            except (ValueError, IndexError):
                continue
        return results

    def scrape(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        codes = ["SR0", "SR2509", "SR2601", "SR2605"]
        for code in codes:
            url = f"https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20{code}=/InnerFuturesNewService.getDailyKLine?symbol={code}"
            text = self.fetch(url)
            if not text:
                continue
            items = self._parse_day_kline(text, code)
            end_date = date.today() + timedelta(days=1)
            start_date = end_date - timedelta(days=90)
            items = [i for i in items if start_date <= i["trade_date"] <= end_date]
            for item in items:
                item["contract_code"] = code
                item["source"] = self.source
            results.extend(items)
        return results
