from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.domain.material.models import Material, Tag
from app.domain.material.schemas import MaterialCreate, MaterialUpdate


class MaterialRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        keyword: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> tuple[list[Material], int]:
        query = self.db.query(Material)
        if category:
            query = query.filter(Material.category == category)
        if tag:
            query = query.join(Material.tags).filter(Tag.name == tag)
        if keyword:
            query = query.filter(
                or_(
                    Material.title.contains(keyword),
                    Material.content.contains(keyword),
                )
            )
        query = query.order_by(Material.created_at.desc())
        total = query.count()
        materials = query.offset(offset).limit(limit).all()
        return materials, total

    def get(self, material_id: int) -> Optional[Material]:
        return self.db.query(Material).filter(Material.id == material_id).first()

    def create(self, data: MaterialCreate) -> Material:
        material = Material(**data.model_dump(exclude={"tags"}))
        if data.tags:
            for tag_name in data.tags:
                tag = self._get_or_create_tag(tag_name)
                material.tags.append(tag)
        self.db.add(material)
        self.db.commit()
        self.db.refresh(material)
        return material

    def update(self, material: Material, data: MaterialUpdate) -> Material:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(material, field, value)
        self.db.commit()
        self.db.refresh(material)
        return material

    def delete(self, material: Material) -> None:
        self.db.delete(material)
        self.db.commit()

    def add_tags(self, material: Material, tags: list[str]) -> Material:
        for tag_name in tags:
            tag = self._get_or_create_tag(tag_name)
            if tag not in material.tags:
                material.tags.append(tag)
        self.db.commit()
        self.db.refresh(material)
        return material

    def remove_tag(self, material: Material, tag_id: int) -> Material:
        tag = self.db.query(Tag).filter(Tag.id == tag_id).first()
        if tag and tag in material.tags:
            material.tags.remove(tag)
            self.db.commit()
            self.db.refresh(material)
        return material

    def _get_or_create_tag(self, name: str) -> Tag:
        tag = self.db.query(Tag).filter(Tag.name == name).first()
        if not tag:
            tag = Tag(name=name)
            self.db.add(tag)
            self.db.commit()
        return tag
