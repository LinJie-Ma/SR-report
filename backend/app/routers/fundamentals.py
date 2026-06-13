from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.fundamentals import Fundamental
from ..schemas.fundamentals import FundamentalResponse

router = APIRouter(prefix="/api/v1/fundamentals", tags=["fundamentals"])


@router.get("", response_model=list[FundamentalResponse])
def list_fundamentals(db: Session = Depends(get_db)):
    stmt = select(Fundamental).order_by(desc(Fundamental.created_at))
    return db.execute(stmt).scalars().all()
