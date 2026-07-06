from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SignalBase(BaseModel):
    title: str = Field(..., description="Signal title")
    platform: str = Field(..., description="Source platform")
    url: str = Field(..., description="Original URL")
    hot_score: int = Field(0, description="Hot score")
    content_summary: str = Field("", description="Content summary")
    source_type: str = Field("", description="Source type")


class SignalCreate(SignalBase):
    pass


class SignalUpdate(BaseModel):
    title: Optional[str] = None
    platform: Optional[str] = None
    url: Optional[str] = None
    hot_score: Optional[int] = None
    content_summary: Optional[str] = None
    source_type: Optional[str] = None


class SignalResponse(SignalBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SignalListResponse(BaseModel):
    data: list[SignalResponse]
    total: int
    limit: int
    offset: int


class SignalCollectRequest(BaseModel):
    platforms: list[str] = Field(..., description="Platforms to collect from")
