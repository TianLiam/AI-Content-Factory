"""
股票数据采集管理器 - 管理所有采集器，提供统一采集接口
"""

from typing import List, Dict, Optional, Any
from loguru import logger

from .base import StockCollector


class CollectorManager:
    """股票数据采集管理器（单例）"""
    
    _instance = None
    _collectors: Dict[str, StockCollector] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def register_collector(self, collector: StockCollector) -> None:
        """注册采集器"""
        if collector.get_id() in self._collectors:
            logger.warning(f"采集器 {collector.get_id()} 已注册")
        self._collectors[collector.get_id()] = collector
        logger.info(f"采集器注册成功: {collector.get_id()} - {collector.get_name()}")
    
    def unregister_collector(self, collector_id: str) -> None:
        """注销采集器"""
        if collector_id in self._collectors:
            del self._collectors[collector_id]
            logger.info(f"采集器注销成功: {collector_id}")
    
    def get_collector(self, collector_id: str) -> Optional[StockCollector]:
        """获取采集器"""
        return self._collectors.get(collector_id)
    
    def get_collectors(self) -> List[StockCollector]:
        """获取所有采集器"""
        return list(self._collectors.values())
    
    def get_active_collectors(self) -> List[StockCollector]:
        """获取所有激活的采集器"""
        return [c for c in self._collectors.values() if c.is_active()]
    
    async def collect_from_provider(self, provider_id: str, stock_code: str, data_type: str = "all") -> Dict[str, Any]:
        """从指定采集器采集数据"""
        collector = self.get_collector(provider_id)
        if not collector:
            raise ValueError(f"采集器 {provider_id} 不存在")
        if not collector.is_active():
            raise ValueError(f"采集器 {provider_id} 未激活")
        
        try:
            logger.info(f"开始从 {collector.get_name()} 采集股票 {stock_code} 数据")
            
            if data_type == "all":
                result = await collector.collect_all(stock_code)
            elif data_type == "stock_info":
                result = {"stock_info": await collector.collect_stock_info(stock_code)}
            elif data_type == "daily":
                result = {"daily_data": await collector.collect_daily_data(stock_code)}
            elif data_type == "minute":
                result = {"minute_data": await collector.collect_minute_data(stock_code)}
            elif data_type == "financial":
                result = {"financial_data": await collector.collect_financial_data(stock_code)}
            elif data_type == "capital_flow":
                result = {"capital_flow": await collector.collect_capital_flow(stock_code)}
            elif data_type == "news":
                result = {"news": await collector.collect_news(stock_code)}
            else:
                raise ValueError(f"不支持的数据类型: {data_type}")
            
            logger.info(f"完成从 {collector.get_name()} 采集股票 {stock_code} 数据")
            return result
            
        except Exception as e:
            logger.error(f"从 {collector.get_name()} 采集股票 {stock_code} 数据失败: {str(e)}")
            raise
    
    async def collect_from_all(self, stock_code: str, data_type: str = "all") -> List[Dict[str, Any]]:
        """从所有激活的采集器采集数据"""
        results = []
        for collector in self.get_active_collectors():
            try:
                data = await self.collect_from_provider(collector.get_id(), stock_code, data_type)
                results.append(data)
            except Exception as e:
                logger.error(f"从 {collector.get_name()} 采集失败: {str(e)}")
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


def initialize_collectors() -> None:
    """初始化所有采集器"""
    manager = get_collector_manager()
    
    from .eastmoney import EastmoneyCollector
    from .sina import SinaCollector
    from .tencent import TencentCollector
    
    manager.register_collector(EastmoneyCollector())
    manager.register_collector(SinaCollector())
    manager.register_collector(TencentCollector())
    
    logger.info("股票采集器初始化完成")
