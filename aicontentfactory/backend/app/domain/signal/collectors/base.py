"""
信号采集基类 - 继承自 SignalProvider，添加更多功能
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from datetime import datetime

from app.domain.ai.providers.base import SignalProvider


class SignalCollector(SignalProvider, ABC):
    """信号采集器基类"""
    
    def __init__(self):
        self.request_interval = 1.0
        self.max_retries = 3
    
    @abstractmethod
    async def collect(self, **kwargs) -> list[dict]:
        """采集信号数据"""
        pass
    
    async def collect_batch(self, topics: List[str] = None, **kwargs) -> list[dict]:
        """批量采集信号数据"""
        results = []
        if topics:
            for topic in topics:
                data = await self.collect(topic=topic, **kwargs)
                results.extend(data)
        else:
            results = await self.collect(**kwargs)
        return results
    
    def normalize_signal(self, raw_data: dict) -> dict:
        """标准化信号数据格式"""
        return {
            "title": raw_data.get("title", ""),
            "platform": self.get_id(),
            "url": raw_data.get("url", ""),
            "hot_score": raw_data.get("hot_score", 0),
            "content_summary": raw_data.get("content_summary", ""),
            "source_type": raw_data.get("source_type", "article"),
            "author": raw_data.get("author", ""),
            "view_count": raw_data.get("view_count", 0),
            "like_count": raw_data.get("like_count", 0),
            "comment_count": raw_data.get("comment_count", 0),
            "status": "pending",
            "collected_at": datetime.now().isoformat(),
            "raw_data": raw_data,
        }
    
    async def health_check(self) -> bool:
        """健康检查"""
        try:
            result = await self.collect()
            return len(result) >= 0
        except Exception:
            return False
