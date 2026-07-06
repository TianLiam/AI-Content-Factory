from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.domain.ai import schemas, services

router = APIRouter()


@router.post("/analyze", response_model=schemas.AnalysisResponse)
async def analyze_signal(payload: schemas.AnalysisRequest, db: Session = Depends(get_db)):
    result = services.analyze_signal(db, payload)
    return {"data": result}


@router.post("/generate")
async def generate_article(payload: schemas.GenerateRequest):
    result = services.generate_article(payload)
    return {"data": result}


@router.post("/polish")
async def polish_article(payload: schemas.PolishRequest):
    result = services.polish_article(payload)
    return {"data": result}


@router.post("/detect-ai")
async def detect_ai(payload: schemas.DetectAIRequest):
    result = services.detect_ai(payload)
    return {"data": result}


@router.get("/providers")
async def list_providers():
    providers = services.list_providers()
    return {"data": providers}


@router.post("/providers/{provider_id}/test")
async def test_provider(provider_id: str):
    result = services.test_provider(provider_id)
    return {"data": result}
