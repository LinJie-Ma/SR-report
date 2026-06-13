from datetime import date, datetime

from sqlalchemy import String, Date, DateTime, DECIMAL, func
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class EnsoData(Base):
    __tablename__ = "enso_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data_date: Mapped[date] = mapped_column(Date, nullable=False)
    indicator: Mapped[str] = mapped_column(String(30), nullable=False)
    value: Mapped[float] = mapped_column(DECIMAL(10, 4), nullable=False)
    anomaly: Mapped[float | None] = mapped_column(DECIMAL(10, 4))
    enso_status: Mapped[str | None] = mapped_column(String(20))
    region: Mapped[str | None] = mapped_column(String(30))
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
