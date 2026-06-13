from fastapi import APIRouter, Depends
from sqlalchemy import desc, select, func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.enso import EnsoData
from ..schemas.enso import EnsoDataResponse, EnsoLatestResponse

router = APIRouter(prefix="/api/v1/enso", tags=["enso"])


@router.get("", response_model=list[EnsoDataResponse])
def list_enso(db: Session = Depends(get_db)):
    stmt = select(EnsoData).order_by(desc(EnsoData.data_date))
    return db.execute(stmt).scalars().all()


@router.get("/latest", response_model=EnsoLatestResponse)
def get_latest_enso(db: Session = Depends(get_db)):
    oni_row = (
        db.execute(
            select(EnsoData)
            .where(EnsoData.indicator == "ONI")
            .order_by(desc(EnsoData.data_date))
            .limit(1)
        )
        .scalars()
        .first()
    )
    soi_row = (
        db.execute(
            select(EnsoData)
            .where(EnsoData.indicator == "SOI")
            .order_by(desc(EnsoData.data_date))
            .limit(1)
        )
        .scalars()
        .first()
    )
    return EnsoLatestResponse(
        enso_status=oni_row.enso_status if oni_row else None,
        latest_oni=float(oni_row.value) if oni_row else None,
        latest_oni_date=oni_row.data_date if oni_row else None,
        latest_soi=float(soi_row.value) if soi_row else None,
        latest_soi_date=soi_row.data_date if soi_row else None,
        source=oni_row.source if oni_row else None,
    )
