from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.weather import WeatherData
from ..schemas.weather import WeatherDataResponse

router = APIRouter(prefix="/api/v1/weather", tags=["weather"])


@router.get("", response_model=list[WeatherDataResponse])
def list_weather(
    region: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    stmt = select(WeatherData)
    if region:
        stmt = stmt.where(WeatherData.region == region)
    if start_date:
        stmt = stmt.where(WeatherData.weather_date >= start_date)
    if end_date:
        stmt = stmt.where(WeatherData.weather_date <= end_date)
    stmt = stmt.order_by(desc(WeatherData.weather_date))
    return db.execute(stmt).scalars().all()
