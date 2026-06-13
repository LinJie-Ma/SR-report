from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    content: Optional[str] = None
    summary: Optional[str] = None
    url: Optional[str] = None
    publish_date: Optional[datetime] = None
    source: str


class NewsCreate(NewsBase):
    pass


class NewsResponse(NewsBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
