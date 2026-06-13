from fastapi import APIRouter

from ..scheduler import _save

router = APIRouter(prefix="/api/v1/scrape", tags=["scrape"])


@router.post("/trigger")
def trigger_scrape(data_type: str = "all"):
    from ..scrapers.enso_scraper import EnsoScraper
    from ..scrapers.fundamentals_scraper import FundamentalsScraper
    from ..scrapers.futures_scraper import FuturesScraper
    from ..scrapers.news_scraper import NewsScraper
    from ..scrapers.spot_scraper import SpotScraper
    from ..scrapers.weather_scraper import WeatherScraper

    scrapers = {
        "futures": (FuturesScraper, False),
        "spot": (SpotScraper, False),
        "news": (NewsScraper, False),
        "weather": (WeatherScraper, False),
        "enso": (EnsoScraper, True),
        "fundamentals": (FundamentalsScraper, False),
    }

    results = {}
    if data_type == "all":
        targets = scrapers.items()
    elif data_type in scrapers:
        targets = [(data_type, scrapers[data_type])]
    else:
        return {"error": f"未知的数据类型: {data_type}"}

    for name, (scraper_cls, check_changes) in targets:
        scraper = scraper_cls()
        _save(scraper, name, check_changes=check_changes)
        results[name] = "done"

    return {"message": "采集触发完成", "results": results}
