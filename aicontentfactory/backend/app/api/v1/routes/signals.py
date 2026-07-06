from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.domain.signal import schemas, services

router = APIRouter()


@router.get("/", response_model=schemas.SignalListResponse)
async def list_signals(
    platform: str | None = Query(None, description="Filter by platform"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    signals, total = services.list_signals(db, platform, limit, offset)
    return {"data": signals, "total": total, "limit": limit, "offset": offset}


@router.get("/{signal_id}", response_model=schemas.SignalResponse)
async def get_signal(signal_id: int, db: Session = Depends(get_db)):
    signal = services.get_signal(db, signal_id)
    return {"data": signal}


@router.post("/", response_model=schemas.SignalResponse)
async def create_signal(
    payload: schemas.SignalCreate, db: Session = Depends(get_db)
):
    signal = services.create_signal(db, payload)
    return {"data": signal}


@router.put("/{signal_id}", response_model=schemas.SignalResponse)
async def update_signal(
    signal_id: int, payload: schemas.SignalUpdate, db: Session = Depends(get_db)
):
    signal = services.update_signal(db, signal_id, payload)
    return {"data": signal}


@router.delete("/{signal_id}")
async def delete_signal(signal_id: int, db: Session = Depends(get_db)):
    services.delete_signal(db, signal_id)
    return {"message": "Signal deleted successfully"}


@router.post("/collect")
async def collect_signals(
    platforms: schemas.SignalCollectRequest, db: Session = Depends(get_db)
):
    result = services.collect_signals(db, platforms.platforms)
    return {"message": f"Collected {result} signals"}
