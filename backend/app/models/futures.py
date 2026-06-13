from datetime import date, datetime

from sqlalchemy import String, Date, DateTime, DECIMAL, BigInteger, func
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class FuturesData(Base):
    __tablename__ = "futures_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contract_code: Mapped[str] = mapped_column(String(20), nullable=False)
    trade_date: Mapped[date] = mapped_column(Date, nullable=False)
    open: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    high: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    low: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    close: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    volume: Mapped[int] = mapped_column(BigInteger, nullable=False)
    open_interest: Mapped[int] = mapped_column(BigInteger, nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
