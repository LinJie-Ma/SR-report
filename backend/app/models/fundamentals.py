from datetime import datetime

from sqlalchemy import String, DateTime, DECIMAL, func
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class Fundamental(Base):
    __tablename__ = "fundamentals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data_type: Mapped[str] = mapped_column(String(30), nullable=False)
    value: Mapped[float] = mapped_column(DECIMAL(15, 2), nullable=False)
    period: Mapped[str] = mapped_column(String(20), nullable=False)
    region: Mapped[str] = mapped_column(String(30), nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
