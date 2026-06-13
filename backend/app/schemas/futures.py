from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class FuturesDataBase(BaseModel):
    contract_code: str
    trade_date: date
    open: float
    high: float
    low: float
    close: float
    volume: int
    open_interest: int
    source: str


class FuturesDataCreate(FuturesDataBase):
    pass


class FuturesDataResponse(FuturesDataBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class KlineItem(BaseModel):
    trade_date: str
    open: float
    high: float
    low: float
    close: float
    volume: int
