from datetime import date, datetime

from sqlalchemy import String, Date, DateTime, DECIMAL, func
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    region: Mapped[str] = mapped_column(String(50), nullable=False)
    weather_date: Mapped[date] = mapped_column(Date, nullable=False)
    temperature_high: Mapped[float | None] = mapped_column(DECIMAL(5, 1))
    temperature_low: Mapped[float | None] = mapped_column(DECIMAL(5, 1))
    rainfall: Mapped[float | None] = mapped_column(DECIMAL(10, 2))
    weather_desc: Mapped[str | None] = mapped_column(String(100))
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
