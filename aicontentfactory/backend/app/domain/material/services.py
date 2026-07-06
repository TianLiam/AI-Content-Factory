from typing import Optional
from sqlalchemy.orm import Session

from app.domain.material.repositories import MaterialRepository
from app.domain.material.schemas import MaterialCreate, MaterialUpdate
from app.core.exceptions import NotFoundException


def list_materials(
    db: Session,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    keyword: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
) -> tuple:
    repo = MaterialRepository(db)
    return repo.list(category, tag, keyword, limit, offset)


def get_material(db: Session, material_id: int):
    repo = MaterialRepository(db)
    material = repo.get(material_id)
    if not material:
        raise NotFoundException(detail="Material not found")
    return material


def create_material(db: Session, payload: MaterialCreate):
    repo = MaterialRepository(db)
    return repo.create(payload)


def update_material(db: Session, material_id: int, payload: MaterialUpdate):
    repo = MaterialRepository(db)
    material = repo.get(material_id)
    if not material:
        raise NotFoundException(detail="Material not found")
    return repo.update(material, payload)


def delete_material(db: Session, material_id: int):
    repo = MaterialRepository(db)
    material = repo.get(material_id)
    if not material:
        raise NotFoundException(detail="Material not found")
    repo.delete(material)


def add_tags_to_material(db: Session, material_id: int, tags: list[str]):
    repo = MaterialRepository(db)
    material = repo.get(material_id)
    if not material:
        raise NotFoundException(detail="Material not found")
    return repo.add_tags(material, tags)


def remove_tag_from_material(db: Session, material_id: int, tag_id: int):
    repo = MaterialRepository(db)
    material = repo.get(material_id)
    if not material:
        raise NotFoundException(detail="Material not found")
    return repo.remove_tag(material, tag_id)
