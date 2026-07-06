from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.domain.signal.models import Signal
from app.domain.signal.schemas import SignalCreate, SignalUpdate


class SignalRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        platform: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> tuple[list[Signal], int]:
        query = self.db.query(Signal)
        if platform:
            query = query.filter(Signal.platform == platform)
        query = query.order_by(Signal.hot_score.desc(), Signal.created_at.desc())
        total = query.count()
        signals = query.offset(offset).limit(limit).all()
        return signals, total

    def get(self, signal_id: int) -> Optional[Signal]:
        return self.db.query(Signal).filter(Signal.id == signal_id).first()

    def create(self, data: SignalCreate) -> Signal:
        signal = Signal(**data.model_dump())
        self.db.add(signal)
        self.db.commit()
        self.db.refresh(signal)
        return signal

    def update(self, signal: Signal, data: SignalUpdate) -> Signal:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(signal, field, value)
        self.db.commit()
        self.db.refresh(signal)
        return signal

    def delete(self, signal: Signal) -> None:
        self.db.delete(signal)
        self.db.commit()

    def exists_by_url(self, url: str) -> bool:
        return self.db.query(func.count(Signal.id)).filter(Signal.url == url).scalar() > 0
