from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class EnsoDataBase(BaseModel):
    data_date: date
    indicator: str
    value: float
    anomaly: Optional[float] = None
    enso_status: Optional[str] = None
    region: Optional[str] = None
    source: str


class EnsoDataCreate(EnsoDataBase):
    pass


class EnsoDataResponse(EnsoDataBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class EnsoLatestResponse(BaseModel):
    enso_status: Optional[str] = None
    latest_oni: Optional[float] = None
    latest_oni_date: Optional[date] = None
    latest_soi: Optional[float] = None
    latest_soi_date: Optional[date] = None
    source: Optional[str] = None
