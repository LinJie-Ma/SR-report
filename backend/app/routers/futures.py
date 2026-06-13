from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.futures import FuturesData
from ..schemas.futures import FuturesDataResponse, KlineItem

router = APIRouter(prefix="/api/v1/futures", tags=["futures"])


@router.get("", response_model=list[FuturesDataResponse])
def list_futures(
    contract_code: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    stmt = select(FuturesData)
    if contract_code:
        stmt = stmt.where(FuturesData.contract_code == contract_code)
    if start_date:
        stmt = stmt.where(FuturesData.trade_date >= start_date)
    if end_date:
        stmt = stmt.where(FuturesData.trade_date <= end_date)
    stmt = stmt.order_by(desc(FuturesData.trade_date))
    return db.execute(stmt).scalars().all()


@router.get("/kline", response_model=list[KlineItem])
def get_kline(
    contract_code: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    stmt = select(FuturesData)
    if contract_code:
        stmt = stmt.where(FuturesData.contract_code == contract_code)
    if start_date:
        stmt = stmt.where(FuturesData.trade_date >= start_date)
    if end_date:
        stmt = stmt.where(FuturesData.trade_date <= end_date)
    stmt = stmt.order_by(FuturesData.trade_date.asc())
    rows = db.execute(stmt).scalars().all()
    return [
        KlineItem(
            trade_date=row.trade_date.isoformat(),
            open=row.open,
            high=row.high,
            low=row.low,
            close=row.close,
            volume=row.volume,
        )
        for row in rows
    ]
