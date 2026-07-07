"""
信号服务模块

提供信号的 CRUD 操作和采集功能。
"""

from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.signal.repositories import SignalRepository
from app.domain.signal.schemas import SignalCreate, SignalUpdate
from app.domain.signal.collectors import get_collector_manager, setup_default_collectors
from app.core.exceptions import NotFoundException
from loguru import logger


def list_signals(
    db: Session,
    platform: Optional[str] = None,
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    sort_by: str = "hot_score",
    sort_order: str = "desc",
    limit: int = 10,
    offset: int = 0,
) -> tuple:
    """获取信号列表"""
    repo = SignalRepository(db)
    return repo.list(
        platform=platform,
        keyword=keyword,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset,
    )


def get_signal(db: Session, signal_id: int):
    """获取信号详情"""
    repo = SignalRepository(db)
    signal = repo.get(signal_id)
    if not signal:
        raise NotFoundException(detail="Signal not found")
    return signal


def create_signal(db: Session, payload: SignalCreate):
    """创建信号"""
    repo = SignalRepository(db)
    if repo.exists_by_url(payload.url):
        raise Exception("Signal already exists")
    return repo.create(payload)


def update_signal(db: Session, signal_id: int, payload: SignalUpdate):
    """更新信号"""
    repo = SignalRepository(db)
    signal = repo.get(signal_id)
    if not signal:
        raise NotFoundException(detail="Signal not found")
    return repo.update(signal, payload)


def delete_signal(db: Session, signal_id: int):
    """删除信号"""
    repo = SignalRepository(db)
    signal = repo.get(signal_id)
    if not signal:
        raise NotFoundException(detail="Signal not found")
    repo.delete(signal)


async def collect_signals(db: Session, platforms: List[str] = None) -> int:
    """采集信号数据"""
    setup_default_collectors()
    manager = get_collector_manager()
    
    if platforms:
        total_count = 0
        for platform in platforms:
            try:
                data = await manager.collect_from_provider(platform)
                repo = SignalRepository(db)
                count = 0
                for item in data:
                    create_payload = SignalCreate(
                        title=item["title"],
                        platform=item["platform"],
                        url=item["url"],
                        hot_score=item["hot_score"],
                        content_summary=item["content_summary"],
                        source_type=item["source_type"],
                        author=item["author"],
                        view_count=item["view_count"],
                        like_count=item["like_count"],
                        comment_count=item["comment_count"],
                        status=item["status"],
                    )
                    try:
                        repo.create(create_payload)
                        count += 1
                    except Exception:
                        continue
                total_count += count
                logger.info(f"Collected {count} signals from {platform}")
            except Exception as e:
                logger.error(f"Failed to collect from {platform}: {str(e)}")
        return total_count
    else:
        data = await manager.collect_from_all()
        repo = SignalRepository(db)
        count = 0
        for item in data:
            create_payload = SignalCreate(
                title=item["title"],
                platform=item["platform"],
                url=item["url"],
                hot_score=item["hot_score"],
                content_summary=item["content_summary"],
                source_type=item["source_type"],
                author=item["author"],
                view_count=item["view_count"],
                like_count=item["like_count"],
                comment_count=item["comment_count"],
                status=item["status"],
            )
            try:
                repo.create(create_payload)
                count += 1
            except Exception:
                continue
        return count


def get_collector_info(db: Session = None) -> List[dict]:
    """获取采集器信息"""
    setup_default_collectors()
    manager = get_collector_manager()
    return manager.get_collector_info()
