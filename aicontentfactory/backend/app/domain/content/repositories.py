from typing import Optional
from sqlalchemy.orm import Session

from app.domain.content.models import Content
from app.domain.content.schemas import ContentCreate, ContentUpdate


class ContentRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        platform: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> tuple[list[Content], int]:
        query = self.db.query(Content)
        if platform:
            query = query.filter(Content.target_platform == platform)
        if status:
            query = query.filter(Content.status == status)
        query = query.order_by(Content.created_at.desc())
        total = query.count()
        contents = query.offset(offset).limit(limit).all()
        return contents, total

    def get(self, content_id: int) -> Optional[Content]:
        return self.db.query(Content).filter(Content.id == content_id).first()

    def create(self, data: ContentCreate) -> Content:
        content = Content(**data.model_dump())
        self.db.add(content)
        self.db.commit()
        self.db.refresh(content)
        return content

    def update(self, content: Content, data: ContentUpdate) -> Content:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(content, field, value)
        self.db.commit()
        self.db.refresh(content)
        return content

    def delete(self, content: Content) -> None:
        self.db.delete(content)
        self.db.commit()
