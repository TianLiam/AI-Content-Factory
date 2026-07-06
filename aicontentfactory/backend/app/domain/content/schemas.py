from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ContentBase(BaseModel):
    title: str = Field(..., description="Content title")
    target_platform: str = Field(..., description="Target platform")
    status: str = Field("draft", description="Content status")


class ContentCreate(ContentBase):
    outline: Optional[str] = Field("", description="Content outline")
    content: Optional[str] = Field("", description="Content body")


class ContentUpdate(BaseModel):
    title: Optional[str] = None
    target_platform: Optional[str] = None
    status: Optional[str] = None
    outline: Optional[str] = None
    content: Optional[str] = None


class ContentResponse(ContentBase):
    id: int
    outline: str = ""
    content: str = ""
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ContentListResponse(BaseModel):
    data: list[ContentResponse]
    total: int
    limit: int
    offset: int


class ContentAnalysisResponse(BaseModel):
    content_id: int
    hot_reasons: List[str] = []
    user_focus: List[str] = []
    keywords: List[str] = []
    structure: dict = {}
    sentiment: str = "neutral"
    target_audience: str = ""
