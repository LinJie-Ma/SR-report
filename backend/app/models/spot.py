from datetime import date, datetime

from sqlalchemy import String, Date, DateTime, DECIMAL, func
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class SpotPrice(Base):
    __tablename__ = "spot_prices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    region: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    price_date: Mapped[date] = mapped_column(Date, nullable=False)
    variety: Mapped[str] = mapped_column(String(50), nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
