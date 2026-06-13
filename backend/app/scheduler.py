import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from .config import SCRAPE_INTERVALS

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def start_scheduler():
    from .scrapers.futures_scraper import FuturesScraper
    from .scrapers.spot_scraper import SpotScraper
    from .scrapers.news_scraper import NewsScraper
    from .scrapers.weather_scraper import WeatherScraper
    from .scrapers.enso_scraper import EnsoScraper
    from .scrapers.fundamentals_scraper import FundamentalsScraper

    def run_futures():
        scraper = FuturesScraper()
        _save(scraper, "futures")

    def run_spot():
        scraper = SpotScraper()
        _save(scraper, "spot")

    def run_news():
        scraper = NewsScraper()
        _save(scraper, "news")

    def run_weather():
        scraper = WeatherScraper()
        _save(scraper, "weather")

    def run_fundamentals():
        scraper = FundamentalsScraper()
        _save(scraper, "fundamentals")

    def run_enso():
        scraper = EnsoScraper()
        _save(scraper, "enso", check_changes=True)

    futures_cfg = SCRAPE_INTERVALS.get("futures", {})
    scheduler.add_job(run_futures, CronTrigger(**futures_cfg), id="futures")

    spot_cfg = SCRAPE_INTERVALS.get("spot", {})
    scheduler.add_job(run_spot, CronTrigger(**spot_cfg), id="spot")

    news_cfg = SCRAPE_INTERVALS.get("news", {})
    scheduler.add_job(run_news, CronTrigger(**news_cfg), id="news")

    weather_cfg = SCRAPE_INTERVALS.get("weather", {})
    scheduler.add_job(run_weather, CronTrigger(**weather_cfg), id="weather")

    fundamentals_cfg = SCRAPE_INTERVALS.get("fundamentals", {})
    scheduler.add_job(run_fundamentals, CronTrigger(**fundamentals_cfg), id="fundamentals")

    enso_cfg = SCRAPE_INTERVALS.get("enso", {})
    scheduler.add_job(run_enso, CronTrigger(**enso_cfg), id="enso")

    scheduler.start()
    logger.info("定时调度器已启动")


def _save(scraper, data_type: str, check_changes: bool = False):
    from .database import SessionLocal

    db = SessionLocal()
    try:
        data = scraper.scrape()
        if not data:
            logger.info(f"[{data_type}] 无新数据")
            return

        model_map = _get_model_map()
        model = model_map.get(data_type)
        if not model:
            return

        for item in data:
            existing = _check_exists(db, model, item)
            if existing:
                if check_changes:
                    _update_if_changed(db, model, existing, item)
                continue
            db.add(model(**item))

        db.commit()
        logger.info(f"[{data_type}] 采集完成，新增 {len(data)} 条记录")
    except Exception as e:
        db.rollback()
        logger.error(f"[{data_type}] 采集异常: {e}")
    finally:
        db.close()


def _get_model_map():
    from .models.futures import FuturesData
    from .models.spot import SpotPrice
    from .models.news import News
    from .models.weather import WeatherData
    from .models.enso import EnsoData
    from .models.fundamentals import Fundamental

    return {
        "futures": FuturesData,
        "spot": SpotPrice,
        "news": News,
        "weather": WeatherData,
        "enso": EnsoData,
        "fundamentals": Fundamental,
    }


def _check_exists(db, model, item: dict):
    from sqlalchemy import select

    if model.__tablename__ == "futures_data":
        stmt = select(model).where(
            model.contract_code == item["contract_code"],
            model.trade_date == item["trade_date"],
        )
    elif model.__tablename__ == "spot_prices":
        stmt = select(model).where(
            model.region == item["region"],
            model.price_date == item["price_date"],
        )
    elif model.__tablename__ == "news":
        stmt = select(model).where(model.title == item["title"])
    elif model.__tablename__ == "weather_data":
        stmt = select(model).where(
            model.region == item["region"],
            model.weather_date == item["weather_date"],
        )
    elif model.__tablename__ == "enso_data":
        stmt = select(model).where(
            model.indicator == item["indicator"],
            model.data_date == item["data_date"],
            model.source == item["source"],
        )
    elif model.__tablename__ == "fundamentals":
        stmt = select(model).where(
            model.data_type == item["data_type"],
            model.period == item["period"],
            model.region == item["region"],
        )
    else:
        return None
    return db.execute(stmt).scalars().first()


def _update_if_changed(db, model, existing, item: dict):
    changed = False
    for key, val in item.items():
        if key in ("id", "created_at"):
            continue
        if getattr(existing, key, None) != val:
            setattr(existing, key, val)
            changed = True
    if changed:
        db.add(existing)
