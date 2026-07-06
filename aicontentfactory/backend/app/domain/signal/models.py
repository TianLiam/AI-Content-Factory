from sqlalchemy import Column, Integer, String, Text

from app.infrastructure.database.base import BaseModel


class Signal(BaseModel):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    platform = Column(String(50), nullable=False, index=True)
    url = Column(String(1000), nullable=False)
    hot_score = Column(Integer, default=0)
    content_summary = Column(Text)
    source_type = Column(String(50), default="")

    def __repr__(self) -> str:
        return f"<Signal(id={self.id}, title={self.title}, platform={self.platform})>"
