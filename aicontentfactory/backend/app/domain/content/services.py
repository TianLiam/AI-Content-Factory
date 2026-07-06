from typing import Optional
from sqlalchemy.orm import Session

from app.domain.content.repositories import ContentRepository
from app.domain.content.schemas import ContentCreate, ContentUpdate, ContentAnalysisResponse
from app.core.exceptions import NotFoundException


def list_contents(
    db: Session,
    platform: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
) -> tuple:
    repo = ContentRepository(db)
    return repo.list(platform, status, limit, offset)


def get_content(db: Session, content_id: int):
    repo = ContentRepository(db)
    content = repo.get(content_id)
    if not content:
        raise NotFoundException(detail="Content not found")
    return content


def create_content(db: Session, payload: ContentCreate):
    repo = ContentRepository(db)
    return repo.create(payload)


def update_content(db: Session, content_id: int, payload: ContentUpdate):
    repo = ContentRepository(db)
    content = repo.get(content_id)
    if not content:
        raise NotFoundException(detail="Content not found")
    return repo.update(content, payload)


def delete_content(db: Session, content_id: int):
    repo = ContentRepository(db)
    content = repo.get(content_id)
    if not content:
        raise NotFoundException(detail="Content not found")
    repo.delete(content)


def analyze_content(db: Session, content_id: int) -> ContentAnalysisResponse:
    repo = ContentRepository(db)
    content = repo.get(content_id)
    if not content:
        raise NotFoundException(detail="Content not found")
    return ContentAnalysisResponse(content_id=content_id)


def generate_content(db: Session, content_id: int) -> str:
    return "Content generation is in progress"


def polish_content(db: Session, content_id: int):
    repo = ContentRepository(db)
    content = repo.get(content_id)
    if not content:
        raise NotFoundException(detail="Content not found")
    return content


def detect_ai_content(db: Session, content_id: int) -> dict:
    return {"score": 0, "ai_probability": 0.0, "repeat_sentence": [], "suggestions": []}


def export_content(db: Session, content_id: int, format: str) -> dict:
    repo = ContentRepository(db)
    content = repo.get(content_id)
    if not content:
        raise NotFoundException(detail="Content not found")
    return {"format": format, "content": content.content}
