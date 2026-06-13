from datetime import datetime

from pydantic import BaseModel


class FundamentalBase(BaseModel):
    data_type: str
    value: float
    period: str
    region: str
    source: str


class FundamentalCreate(FundamentalBase):
    pass


class FundamentalResponse(FundamentalBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
