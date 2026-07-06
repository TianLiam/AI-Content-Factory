from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.domain.material import schemas, services

router = APIRouter()


@router.get("/", response_model=schemas.MaterialListResponse)
async def list_materials(
    category: str | None = Query(None, description="Filter by category"),
    tag: str | None = Query(None, description="Filter by tag"),
    keyword: str | None = Query(None, description="Search keyword"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    materials, total = services.list_materials(db, category, tag, keyword, limit, offset)
    return {"data": materials, "total": total, "limit": limit, "offset": offset}


@router.get("/{material_id}", response_model=schemas.MaterialResponse)
async def get_material(material_id: int, db: Session = Depends(get_db)):
    material = services.get_material(db, material_id)
    return {"data": material}


@router.post("/", response_model=schemas.MaterialResponse)
async def create_material(
    payload: schemas.MaterialCreate, db: Session = Depends(get_db)
):
    material = services.create_material(db, payload)
    return {"data": material}


@router.put("/{material_id}", response_model=schemas.MaterialResponse)
async def update_material(
    material_id: int, payload: schemas.MaterialUpdate, db: Session = Depends(get_db)
):
    material = services.update_material(db, material_id, payload)
    return {"data": material}


@router.delete("/{material_id}")
async def delete_material(material_id: int, db: Session = Depends(get_db)):
    services.delete_material(db, material_id)
    return {"message": "Material deleted successfully"}


@router.post("/{material_id}/tags")
async def add_tags_to_material(
    material_id: int, payload: schemas.MaterialAddTags, db: Session = Depends(get_db)
):
    material = services.add_tags_to_material(db, material_id, payload.tags)
    return {"data": material}


@router.delete("/{material_id}/tags/{tag_id}")
async def remove_tag_from_material(material_id: int, tag_id: int, db: Session = Depends(get_db)):
    services.remove_tag_from_material(db, material_id, tag_id)
    return {"message": "Tag removed successfully"}
