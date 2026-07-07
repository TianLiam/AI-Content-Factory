"""
素材服务模块

提供素材的 CRUD 操作和标签管理功能。
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.domain.material.repositories import MaterialRepository
from app.domain.material.schemas import MaterialCreate, MaterialUpdate
from app.domain.material.taggers import get_tagger_manager, setup_default_taggers
from app.domain.material.organizers import get_organizer_manager
from app.core.exceptions import NotFoundException
from loguru import logger


def list_materials(
    db: Session,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    keyword: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    limit: int = 10,
    offset: int = 0,
) -> tuple:
    """获取素材列表"""
    repo = MaterialRepository(db)
    return repo.list(
        category=category,
        tag=tag,
        keyword=keyword,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset,
    )


def get_material(db: Session, material_id: int):
    """获取素材详情"""
    repo = MaterialRepository(db)
    material = repo.get(material_id)
    if not material:
        raise NotFoundException(detail="Material not found")
    return material


def create_material(db: Session, payload: MaterialCreate):
    """创建素材"""
    repo = MaterialRepository(db)
    return repo.create(payload)


def update_material(db: Session, material_id: int, payload: MaterialUpdate):
    """更新素材"""
    repo = MaterialRepository(db)
    material = repo.get(material_id)
    if not material:
        raise NotFoundException(detail="Material not found")
    return repo.update(material, payload)


def delete_material(db: Session, material_id: int):
    """删除素材"""
    repo = MaterialRepository(db)
    material = repo.get(material_id)
    if not material:
        raise NotFoundException(detail="Material not found")
    repo.delete(material)


def add_tags_to_material(db: Session, material_id: int, tags: list[str]):
    """添加标签到素材"""
    repo = MaterialRepository(db)
    material = repo.get(material_id)
    if not material:
        raise NotFoundException(detail="Material not found")
    return repo.add_tags(material, tags)


def remove_tag_from_material(db: Session, material_id: int, tag_id: int):
    """从素材移除标签"""
    repo = MaterialRepository(db)
    material = repo.get(material_id)
    if not material:
        raise NotFoundException(detail="Material not found")
    return repo.remove_tag(material, tag_id)


async def extract_tags_from_content(db: Session, content: str) -> List[str]:
    """从内容中提取标签"""
    setup_default_taggers()
    tagger_manager = get_tagger_manager()
    return await tagger_manager.extract_tags_from_content(content)


async def suggest_tags_for_content(db: Session, content: str) -> List[str]:
    """为内容建议标签"""
    setup_default_taggers()
    tagger_manager = get_tagger_manager()
    return await tagger_manager.suggest_tags_for_content(content)


def get_tagger_info(db: Session = None) -> List[dict]:
    """获取标签器信息"""
    setup_default_taggers()
    manager = get_tagger_manager()
    return [
        {"id": t.get_id(), "name": t.get_name(), "active": t.is_active()}
        for t in manager._taggers.values()
    ]


def get_organizer_info(db: Session = None) -> List[dict]:
    """获取组织器信息"""
    manager = get_organizer_manager()
    return [
        {"id": o.get_id(), "name": o.get_name(), "active": o.is_active()}
        for o in manager._organizers.values()
    ]
