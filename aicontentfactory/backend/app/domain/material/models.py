from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database.base import BaseModel

material_tag_association = Table(
    "material_tag_association",
    BaseModel.metadata,
    Column("material_id", Integer, ForeignKey("materials.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Material(BaseModel):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    content = Column(Text, nullable=False)
    source_url = Column(String(1000), default="")
    source_platform = Column(String(50), default="")

    tags = relationship(
        "Tag",
        secondary=material_tag_association,
        back_populates="materials",
    )

    def __repr__(self) -> str:
        return f"<Material(id={self.id}, title={self.title}, category={self.category})>"


class Tag(BaseModel):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)

    materials = relationship(
        "Material",
        secondary=material_tag_association,
        back_populates="tags",
    )

    def __repr__(self) -> str:
        return f"<Tag(id={self.id}, name={self.name})>"
