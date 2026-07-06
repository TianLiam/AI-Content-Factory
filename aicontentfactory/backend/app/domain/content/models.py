from sqlalchemy import Column, Integer, String, Text

from app.infrastructure.database.base import BaseModel


class Content(BaseModel):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    target_platform = Column(String(50), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="draft", index=True)
    outline = Column(Text, default="")
    content = Column(Text, default="")

    def __repr__(self) -> str:
        return f"<Content(id={self.id}, title={self.title}, platform={self.target_platform})>"
