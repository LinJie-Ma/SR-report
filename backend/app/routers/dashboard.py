from fastapi import APIRouter, Depends
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.enso import EnsoData
from ..models.fundamentals import Fundamental
from ..models.futures import FuturesData
from ..models.news import News
from ..models.spot import SpotPrice
from ..models.weather import WeatherData

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    latest_futures = (
        db.execute(
            select(FuturesData).order_by(desc(FuturesData.trade_date)).limit(1)
        )
        .scalars()
        .first()
    )

    spot_count = db.execute(select(func.count(SpotPrice.id))).scalar()

    news_count = db.execute(select(func.count(News.id))).scalar()

    enso_row = (
        db.execute(
            select(EnsoData)
            .where(EnsoData.indicator == "ONI")
            .order_by(desc(EnsoData.data_date))
            .limit(1)
        )
        .scalars()
        .first()
    )

    return {
        "latest_futures": {
            "contract_code": latest_futures.contract_code if latest_futures else None,
            "close": float(latest_futures.close) if latest_futures else None,
            "trade_date": latest_futures.trade_date.isoformat() if latest_futures else None,
        },
        "spot_count": spot_count,
        "news_count": news_count,
        "enso_status": enso_row.enso_status if enso_row else None,
    }


@router.get("/latest")
def latest_data(db: Session = Depends(get_db)):
    latest_futures = (
        db.execute(
            select(FuturesData).order_by(desc(FuturesData.trade_date)).limit(30)
        )
        .scalars()
        .all()
    )

    latest_spot = (
        db.execute(
            select(SpotPrice).order_by(desc(SpotPrice.price_date)).limit(10)
        )
        .scalars()
        .all()
    )

    latest_news = (
        db.execute(
            select(News).order_by(desc(News.publish_date)).limit(5)
        )
        .scalars()
        .all()
    )

    latest_weather = (
        db.execute(
            select(WeatherData).order_by(desc(WeatherData.weather_date)).limit(10)
        )
        .scalars()
        .all()
    )

    enso_status = (
        db.execute(
            select(EnsoData)
            .where(EnsoData.indicator == "ONI")
            .order_by(desc(EnsoData.data_date))
            .limit(1)
        )
        .scalars()
        .first()
    )

    return {
        "futures": [
            {
                "trade_date": f.trade_date.isoformat(),
                "close": float(f.close),
                "volume": f.volume,
                "contract_code": f.contract_code,
            }
            for f in latest_futures
        ],
        "spot": [
            {
                "region": s.region,
                "price": float(s.price),
                "price_date": s.price_date.isoformat(),
            }
            for s in latest_spot
        ],
        "news": [
            {
                "id": n.id,
                "title": n.title,
                "summary": n.summary,
                "publish_date": n.publish_date.isoformat() if n.publish_date else None,
                "source": n.source,
            }
            for n in latest_news
        ],
        "weather": [
            {
                "region": w.region,
                "weather_date": w.weather_date.isoformat(),
                "temperature_high": float(w.temperature_high) if w.temperature_high else None,
                "temperature_low": float(w.temperature_low) if w.temperature_low else None,
                "rainfall": float(w.rainfall) if w.rainfall else None,
                "weather_desc": w.weather_desc,
            }
            for w in latest_weather
        ],
        "enso": {
            "status": enso_status.enso_status if enso_status else None,
            "oni_value": float(enso_status.value) if enso_status else None,
            "data_date": enso_status.data_date.isoformat() if enso_status else None,
            "source": enso_status.source if enso_status else None,
        },
    }
