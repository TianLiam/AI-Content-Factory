from typing import Optional
from sqlalchemy.orm import Session

from app.domain.signal.repositories import SignalRepository
from app.domain.signal.schemas import SignalCreate, SignalUpdate
from app.core.exceptions import NotFoundException


def list_signals(
    db: Session,
    platform: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
) -> tuple:
    repo = SignalRepository(db)
    return repo.list(platform, limit, offset)


def get_signal(db: Session, signal_id: int):
    repo = SignalRepository(db)
    signal = repo.get(signal_id)
    if not signal:
        raise NotFoundException(detail="Signal not found")
    return signal


def create_signal(db: Session, payload: SignalCreate):
    repo = SignalRepository(db)
    if repo.exists_by_url(payload.url):
        raise Exception("Signal already exists")
    return repo.create(payload)


def update_signal(db: Session, signal_id: int, payload: SignalUpdate):
    repo = SignalRepository(db)
    signal = repo.get(signal_id)
    if not signal:
        raise NotFoundException(detail="Signal not found")
    return repo.update(signal, payload)


def delete_signal(db: Session, signal_id: int):
    repo = SignalRepository(db)
    signal = repo.get(signal_id)
    if not signal:
        raise NotFoundException(detail="Signal not found")
    repo.delete(signal)


def collect_signals(db: Session, platforms: list[str]) -> int:
    return 0
