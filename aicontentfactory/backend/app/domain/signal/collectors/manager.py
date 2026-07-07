"""
信号采集管理器 - 管理所有信号采集器，提供统一的采集接口
"""

from typing import List, Dict, Optional, Any
from loguru import logger

from .base import SignalCollector


class CollectorManager:
    """信号采集管理器（单例）"""
    
    _instance = None
    _collectors: Dict[str, SignalCollector] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def register_collector(self, collector: SignalCollector) -> None:
        """注册采集器"""
        if collector.get_id() in self._collectors:
            logger.warning(f"Collector {collector.get_id()} already registered")
        self._collectors[collector.get_id()] = collector
        logger.info(f"Collector registered: {collector.get_id()} - {collector.get_name()}")
    
    def unregister_collector(self, collector_id: str) -> None:
        """注销采集器"""
        if collector_id in self._collectors:
            del self._collectors[collector_id]
            logger.info(f"Collector unregistered: {collector_id}")
    
    def get_collector(self, collector_id: str) -> Optional[SignalCollector]:
        """获取采集器"""
        return self._collectors.get(collector_id)
    
    def get_collectors(self) -> List[SignalCollector]:
        """获取所有采集器"""
        return list(self._collectors.values())
    
    def get_active_collectors(self) -> List[SignalCollector]:
        """获取所有启用的采集器"""
        return [c for c in self._collectors.values() if c.is_active()]
    
    async def collect_from_provider(self, provider_id: str, **kwargs) -> List[Dict[str, Any]]:
        """从指定采集器采集数据"""
        collector = self.get_collector(provider_id)
        if not collector:
            raise ValueError(f"Collector {provider_id} not found")
        if not collector.is_active():
            raise ValueError(f"Collector {provider_id} is not active")
        
        try:
            logger.info(f"Starting collection from {collector.get_name()}")
            raw_data = await collector.collect(**kwargs)
            results = [collector.normalize_signal(data) for data in raw_data]
            logger.info(f"Collection completed from {collector.get_name()}: {len(results)} signals")
            return results
        except Exception as e:
            logger.error(f"Collection failed from {collector.get_name()}: {str(e)}")
            raise
    
    async def collect_from_all(self, **kwargs) -> List[Dict[str, Any]]:
        """从所有启用的采集器采集数据"""
        results = []
        for collector in self.get_active_collectors():
            try:
                data = await self.collect_from_provider(collector.get_id(), **kwargs)
                results.extend(data)
            except Exception as e:
                logger.error(f"Failed to collect from {collector.get_name()}: {str(e)}")
                continue
        return results
    
    async def health_check(self) -> Dict[str, bool]:
        """健康检查所有采集器"""
        results = {}
        for collector in self.get_collectors():
            results[collector.get_id()] = await collector.health_check()
        return results
    
    def get_collector_info(self) -> List[Dict[str, Any]]:
        """获取所有采集器信息"""
        info = []
        for collector in self.get_collectors():
            info.append({
                "id": collector.get_id(),
                "name": collector.get_name(),
                "active": collector.is_active(),
            })
        return info


def get_collector_manager() -> CollectorManager:
    """获取采集器管理表单例"""
    return CollectorManager()


def reset_collector_manager() -> None:
    """重置采集器管理器"""
    CollectorManager._instance = None
    CollectorManager._collectors = {}
