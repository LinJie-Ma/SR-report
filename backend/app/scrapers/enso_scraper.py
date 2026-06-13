import logging
from datetime import date
from typing import Any

from bs4 import BeautifulSoup

from .base import BaseScraper

logger = logging.getLogger(__name__)

ONI_URL = "https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php"

SEASON_MONTH_MAP = {
    "DJF": 1, "JFM": 2, "FMA": 3, "MAM": 4, "AMJ": 5,
    "MJJ": 6, "JJA": 7, "JAS": 8, "ASO": 9, "SON": 10,
    "OND": 11, "NDJ": 12,
}

SEASON_LABELS = ["DJF", "JFM", "FMA", "MAM", "AMJ", "MJJ", "JJA", "JAS", "ASO", "SON", "OND", "NDJ"]


class EnsoScraper(BaseScraper):
    source = "NOAA CPC"

    def scrape(self) -> list[dict[str, Any]]:
        text = self.fetch(ONI_URL)
        if not text:
            logger.warning(f"[{self.source}] 无法获取ONI数据")
            return []
        soup = BeautifulSoup(text, "lxml")
        results: list[dict[str, Any]] = []

        data_table = None
        for table in soup.find_all("table"):
            rows = table.find_all("tr")
            if len(rows) < 5:
                continue
            header_row = rows[0]
            header_cols = header_row.find_all(["td", "th"])
            header_texts = [c.get_text(strip=True) for c in header_cols]
            if len(header_texts) >= 13 and header_texts[0] == "Year":
                is_oni = all(h in header_texts[1:14] for h in SEASON_LABELS)
                if is_oni:
                    data_table = table
                    break

        if not data_table:
            logger.warning(f"[{self.source}] 未找到ONI数据表格")
            return results

        rows = data_table.find_all("tr")[1:]
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 2:
                continue
            try:
                year_str = cols[0].get_text(strip=True)
                if not year_str.isdigit():
                    continue
                year_num = int(year_str)

                max_idx = min(len(cols) - 1, 12)
                for i in range(max_idx):
                    val_str = cols[i + 1].get_text(strip=True)
                    if not val_str or val_str == "-":
                        continue
                    value = float(val_str)
                    season = SEASON_LABELS[i]
                    month_num = SEASON_MONTH_MAP[season]
                    data_date = date(year_num, month_num, 15)

                    status = "Neutral"
                    if value >= 0.5:
                        status = "El Nino"
                    elif value <= -0.5:
                        status = "La Nina"

                    results.append({
                        "data_date": data_date,
                        "indicator": "ONI",
                        "value": value,
                        "anomaly": value,
                        "enso_status": status,
                        "region": "Nino3.4",
                        "source": self.source,
                    })
            except (ValueError, IndexError) as e:
                logger.error(f"[{self.source}] 解析ONI行数据失败: {e}")
                continue

        logger.info(f"[{self.source}] 成功解析 {len(results)} 条ONI指数数据")
        return results
