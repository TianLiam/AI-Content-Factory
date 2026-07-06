from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class MaterialBase(BaseModel):
    title: str = Field(..., description="Material title")
    category: str = Field(..., description="Material category")
    content: str = Field(..., description="Material content")
    source_url: str = Field("", description="Source URL")
    source_platform: str = Field("", description="Source platform")


class MaterialCreate(MaterialBase):
    tags: Optional[List[str]] = Field([], description="Tags")


class MaterialUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None
    source_url: Optional[str] = None
    source_platform: Optional[str] = None


class MaterialResponse(MaterialBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[str] = []

    class Config:
        from_attributes = True


class MaterialListResponse(BaseModel):
    data: list[MaterialResponse]
    total: int
    limit: int
    offset: int


class MaterialAddTags(BaseModel):
    tags: List[str] = Field(..., description="Tags to add")
