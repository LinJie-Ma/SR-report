from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select, func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.futures import FuturesData
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


@router.get("/trend")
def get_spot_trend(
    region: str = Query(...),
    days: int = Query(30, ge=7, le=90),
    db: Session = Depends(get_db),
):
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    spot_stmt = (
        select(SpotPrice)
        .where(SpotPrice.region == region)
        .where(SpotPrice.price_date >= start_date)
        .where(SpotPrice.price_date <= end_date)
        .order_by(SpotPrice.price_date.asc())
    )
    spot_rows = db.execute(spot_stmt).scalars().all()

    futures_stmt = (
        select(FuturesData)
        .where(FuturesData.contract_code == "SR0")
        .where(FuturesData.trade_date >= start_date)
        .where(FuturesData.trade_date <= end_date)
        .order_by(FuturesData.trade_date.asc())
    )
    futures_rows = db.execute(futures_stmt).scalars().all()

    return {
        "spot": [
            {"date": s.price_date.isoformat(), "price": float(s.price)}
            for s in spot_rows
        ],
        "futures": [
            {"date": f.trade_date.isoformat(), "close": float(f.close)}
            for f in futures_rows
        ],
    }
