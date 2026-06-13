from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.news import News
from ..schemas.news import NewsResponse

router = APIRouter(prefix="/api/v1/news", tags=["news"])


@router.get("", response_model=list[NewsResponse])
def list_news(
    keyword: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    stmt = select(News)
    if keyword:
        stmt = stmt.where(News.title.contains(keyword))
    stmt = stmt.order_by(desc(News.publish_date), desc(News.created_at))
    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()
