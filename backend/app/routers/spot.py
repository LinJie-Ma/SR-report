from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.spot import SpotPrice
from ..schemas.spot import SpotPriceResponse

router = APIRouter(prefix="/api/v1/spot", tags=["spot"])


@router.get("", response_model=list[SpotPriceResponse])
def list_spot(
    region: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    stmt = select(SpotPrice)
    if region:
        stmt = stmt.where(SpotPrice.region == region)
    if start_date:
        stmt = stmt.where(SpotPrice.price_date >= start_date)
    if end_date:
        stmt = stmt.where(SpotPrice.price_date <= end_date)
    stmt = stmt.order_by(desc(SpotPrice.price_date))
    return db.execute(stmt).scalars().all()
