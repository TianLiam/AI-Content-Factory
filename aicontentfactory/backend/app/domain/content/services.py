"""
内容服务模块

提供内容的 CRUD 操作和分析、生成、检测功能。
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.domain.content.repositories import ContentRepository
from app.domain.content.schemas import ContentCreate, ContentUpdate, ContentAnalysisResponse
from app.domain.content.analyzers import get_analyzer_manager
from app.domain.content.generators import get_generator_manager, setup_default_generators
from app.domain.content.detectors import get_detector_manager, setup_default_detectors
from app.core.exceptions import NotFoundException
from loguru import logger


def list_contents(
    db: Session,
    platform: Optional[str] = None,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    limit: int = 10,
    offset: int = 0,
) -> tuple:
    """获取内容列表"""
    repo = ContentRepository(db)
    return repo.list(
        platform=platform,
        status=status,
        keyword=keyword,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset,
    )


def get_content(db: Session, content_id: int):
    """获取内容详情"""
    repo = ContentRepository(db)
    content = repo.get(content_id)
    if not content:
        raise NotFoundException(detail="Content not found")
    return content


def create_content(db: Session, payload: ContentCreate):
    """创建内容"""
    repo = ContentRepository(db)
    return repo.create(payload)


def update_content(db: Session, content_id: int, payload: ContentUpdate):
    """更新内容"""
    repo = ContentRepository(db)
    content = repo.get(content_id)
    if not content:
        raise NotFoundException(detail="Content not found")
    return repo.update(content, payload)


def delete_content(db: Session, content_id: int):
    """删除内容"""
    repo = ContentRepository(db)
    content = repo.get(content_id)
    if not content:
        raise NotFoundException(detail="Content not found")
    repo.delete(content)


async def analyze_content(db: Session, content_id: int) -> ContentAnalysisResponse:
    """分析内容"""
    repo = ContentRepository(db)
    content = repo.get(content_id)
    if not content:
        raise NotFoundException(detail="Content not found")
    
    analyzer_manager = get_analyzer_manager()
    results = await analyzer_manager.analyze_all(content.content)
    
    return ContentAnalysisResponse(
        content_id=content_id,
        analysis_results=results,
    )


async def generate_content(db: Session, content_id: int) -> str:
    """生成内容"""
    repo = ContentRepository(db)
    content = repo.get(content_id)
    if not content:
        raise NotFoundException(detail="Content not found")
    
    setup_default_generators()
    generator_manager = get_generator_manager()
    
    try:
        result = await generator_manager.generate_with_provider("ai", content.title)
        content.content = result
        repo.update(content, ContentUpdate(content=result))
        return result
    except Exception as e:
        logger.error(f"Content generation failed: {str(e)}")
        return "Content generation failed"


async def polish_content(db: Session, content_id: int) -> str:
    """润色内容"""
    repo = ContentRepository(db)
    content = repo.get(content_id)
    if not content:
        raise NotFoundException(detail="Content not found")
    
    setup_default_generators()
    generator_manager = get_generator_manager()
    
    try:
        result = await generator_manager.polish_with_provider("ai", content.content)
        content.content = result
        repo.update(content, ContentUpdate(content=result))
        return result
    except Exception as e:
        logger.error(f"Content polishing failed: {str(e)}")
        return content.content


async def detect_ai_content(db: Session, content_id: int) -> Dict[str, Any]:
    """检测 AI 内容"""
    repo = ContentRepository(db)
    content = repo.get(content_id)
    if not content:
        raise NotFoundException(detail="Content not found")
    
    setup_default_detectors()
    detector_manager = get_detector_manager()
    
    try:
        result = await detector_manager.detect_with_provider("ai", content.content)
        return result
    except Exception as e:
        logger.error(f"AI detection failed: {str(e)}")
        return {"score": 0, "ai_probability": 0.0, "repeat_sentence": [], "suggestions": []}


def export_content(db: Session, content_id: int, format: str) -> dict:
    """导出内容"""
    repo = ContentRepository(db)
    content = repo.get(content_id)
    if not content:
        raise NotFoundException(detail="Content not found")
    
    return {
        "format": format,
        "content": content.content,
        "title": content.title,
        "created_at": content.created_at.isoformat() if content.created_at else None,
    }


def get_analyzer_info(db: Session = None) -> List[dict]:
    """获取分析器信息"""
    manager = get_analyzer_manager()
    return [
        {"id": a.get_id(), "name": a.get_name(), "active": a.is_active()}
        for a in manager.get_analyzers()
    ]


def get_generator_info(db: Session = None) -> List[dict]:
    """获取生成器信息"""
    setup_default_generators()
    manager = get_generator_manager()
    return [
        {"id": g.get_id(), "name": g.get_name(), "active": g.is_active()}
        for g in manager.get_generators()
    ]


def get_detector_info(db: Session = None) -> List[dict]:
    """获取检测器信息"""
    setup_default_detectors()
    manager = get_detector_manager()
    return [
        {"id": d.get_id(), "name": d.get_name(), "active": d.is_active()}
        for d in manager.get_detectors()
    ]
