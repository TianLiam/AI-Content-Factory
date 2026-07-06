from typing import Optional, List
from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    content: str = Field(..., description="Content to analyze")
    type: str = Field("signal", description="Analysis type")


class AnalysisResponse(BaseModel):
    hot_reasons: List[str] = []
    user_focus: List[str] = []
    keywords: List[str] = []
    structure: dict = {}
    sentiment: str = "neutral"
    target_audience: str = ""


class GenerateRequest(BaseModel):
    outline: str = Field(..., description="Article outline")
    materials: List[str] = Field([], description="Reference materials")
    target_platform: str = Field("wechat", description="Target platform")
    tone: str = Field("professional", description="Writing tone")


class GenerateResponse(BaseModel):
    content: str = Field("", description="Generated content")
    outline: str = Field("", description="Used outline")


class PolishRequest(BaseModel):
    content: str = Field(..., description="Content to polish")
    target_platform: str = Field("wechat", description="Target platform")


class PolishResponse(BaseModel):
    content: str = Field("", description="Polished content")


class DetectAIRequest(BaseModel):
    content: str = Field(..., description="Content to detect")


class DetectAIResponse(BaseModel):
    score: int = Field(0, description="Detection score")
    ai_probability: float = Field(0.0, description="AI probability")
    repeat_sentence: List[str] = []
    suggestions: List[str] = []


class ProviderInfo(BaseModel):
    id: str = Field("", description="Provider ID")
    name: str = Field("", description="Provider name")
    status: str = Field("inactive", description="Provider status")
