import logging
from datetime import date
from typing import Any

from bs4 import BeautifulSoup

from .base import BaseScraper

logger = logging.getLogger(__name__)

ONI_URL = "https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php"


class EnsoScraper(BaseScraper):
    source = "NOAA CPC"

    def scrape(self) -> list[dict[str, Any]]:
        text = self.fetch(ONI_URL)
        if not text:
            logger.warning(f"[{self.source}] 无法获取ONI数据")
            return []
        soup = BeautifulSoup(text, "lxml")
        results: list[dict[str, Any]] = []
        table = soup.find("table")
        if not table:
            logger.warning(f"[{self.source}] 未找到ONI数据表格")
            return results
        rows = table.find_all("tr")[1:]
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 10:
                continue
            try:
                season = cols[0].get_text(strip=True)
                value_str = cols[9].get_text(strip=True)
                if not value_str or value_str == "-":
                    continue
                value = float(value_str)
                year, month_codes = season.split()
                year_num = int(year)
                import re
                months = re.findall(r"[A-Z]+", month_codes)
                if len(months) < 3:
                    continue
                mid_month_map = {"DJF": 1, "JFM": 2, "FMA": 3, "MAM": 4, "AMJ": 5,
                                 "MJJ": 6, "JJA": 7, "JAS": 8, "ASO": 9, "SON": 10,
                                 "OND": 11, "NDJ": 12}
                month_num = mid_month_map.get(month_codes, 1)
                if month_codes in ("DJF", "NDJ"):
                    if month_codes == "DJF":
                        actual_year = year_num + 1
                    else:
                        actual_year = year_num
                else:
                    actual_year = year_num
                data_date = date(actual_year, month_num, 15)
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
        return results
