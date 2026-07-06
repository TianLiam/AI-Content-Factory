from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.domain.content import schemas, services

router = APIRouter()


@router.get("/", response_model=schemas.ContentListResponse)
async def list_contents(
    platform: str | None = Query(None, description="Filter by target platform"),
    status: str | None = Query(None, description="Filter by status"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    contents, total = services.list_contents(db, platform, status, limit, offset)
    return {"data": contents, "total": total, "limit": limit, "offset": offset}


@router.get("/{content_id}", response_model=schemas.ContentResponse)
async def get_content(content_id: int, db: Session = Depends(get_db)):
    content = services.get_content(db, content_id)
    return {"data": content}


@router.post("/", response_model=schemas.ContentResponse)
async def create_content(
    payload: schemas.ContentCreate, db: Session = Depends(get_db)
):
    content = services.create_content(db, payload)
    return {"data": content}


@router.put("/{content_id}", response_model=schemas.ContentResponse)
async def update_content(
    content_id: int, payload: schemas.ContentUpdate, db: Session = Depends(get_db)
):
    content = services.update_content(db, content_id, payload)
    return {"data": content}


@router.delete("/{content_id}")
async def delete_content(content_id: int, db: Session = Depends(get_db)):
    services.delete_content(db, content_id)
    return {"message": "Content deleted successfully"}


@router.post("/{content_id}/analyze", response_model=schemas.ContentAnalysisResponse)
async def analyze_content(content_id: int, db: Session = Depends(get_db)):
    analysis = services.analyze_content(db, content_id)
    return {"data": analysis}


@router.post("/{content_id}/generate")
async def generate_content(content_id: int, db: Session = Depends(get_db)):
    result = services.generate_content(db, content_id)
    return {"message": result}


@router.post("/{content_id}/polish", response_model=schemas.ContentResponse)
async def polish_content(content_id: int, db: Session = Depends(get_db)):
    content = services.polish_content(db, content_id)
    return {"data": content}


@router.post("/{content_id}/detect-ai")
async def detect_ai_content(content_id: int, db: Session = Depends(get_db)):
    result = services.detect_ai_content(db, content_id)
    return {"data": result}


@router.post("/{content_id}/export")
async def export_content(content_id: int, format: str = Query("markdown"), db: Session = Depends(get_db)):
    content = services.export_content(db, content_id, format)
    return {"data": content}
