from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

from .session import Base


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
