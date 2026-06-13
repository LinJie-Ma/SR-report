from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class WeatherDataBase(BaseModel):
    region: str
    weather_date: date
    temperature_high: Optional[float] = None
    temperature_low: Optional[float] = None
    rainfall: Optional[float] = None
    weather_desc: Optional[str] = None
    source: str


class WeatherDataCreate(WeatherDataBase):
    pass


class WeatherDataResponse(WeatherDataBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
