from datetime import date, datetime

from pydantic import BaseModel


class SpotPriceBase(BaseModel):
    region: str
    price: float
    price_date: date
    variety: str
    source: str


class SpotPriceCreate(SpotPriceBase):
    pass


class SpotPriceResponse(SpotPriceBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
