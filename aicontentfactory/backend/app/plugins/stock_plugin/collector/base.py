"""
股票数据采集基类定义
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime
from loguru import logger


class StockCollector(ABC):
    """股票数据采集器基类"""
    
    def __init__(self):
        self.request_interval = 1.0
        self.max_retries = 3
        self._active = True
    
    @abstractmethod
    def get_id(self) -> str:
        """获取采集器唯一标识"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """获取采集器名称"""
        pass
    
    def is_active(self) -> bool:
        """采集器是否激活"""
        return self._active
    
    def set_active(self, active: bool) -> None:
        """设置采集器激活状态"""
        self._active = active
    
    @abstractmethod
    async def collect_stock_info(self, stock_code: str) -> Optional[dict]:
        """采集股票基本信息"""
        pass
    
    @abstractmethod
    async def collect_daily_data(self, stock_code: str, start_date: str = None, end_date: str = None) -> List[dict]:
        """采集股票日线数据"""
        pass
    
    @abstractmethod
    async def collect_minute_data(self, stock_code: str) -> List[dict]:
        """采集股票分钟线数据"""
        pass
    
    @abstractmethod
    async def collect_financial_data(self, stock_code: str) -> Optional[dict]:
        """采集股票财务数据"""
        pass
    
    @abstractmethod
    async def collect_capital_flow(self, stock_code: str) -> Optional[dict]:
        """采集资金流向数据"""
        pass
    
    @abstractmethod
    async def collect_news(self, stock_code: str, limit: int = 20) -> List[dict]:
        """采集股票新闻"""
        pass
    
    async def collect_all(self, stock_code: str) -> Dict[str, Any]:
        """采集所有数据"""
        logger.info(f"开始采集股票 {stock_code} 全部数据")
        result = {
            "stock_info": await self.collect_stock_info(stock_code),
            "daily_data": await self.collect_daily_data(stock_code),
            "minute_data": await self.collect_minute_data(stock_code),
            "financial_data": await self.collect_financial_data(stock_code),
            "capital_flow": await self.collect_capital_flow(stock_code),
            "news": await self.collect_news(stock_code),
            "collected_at": datetime.now().isoformat(),
            "source": self.get_id(),
        }
        logger.info(f"完成采集股票 {stock_code} 全部数据")
        return result
    
    def normalize_stock_info(self, raw_data: dict) -> dict:
        """标准化股票基本信息"""
        return {
            "code": raw_data.get("code", ""),
            "name": raw_data.get("name", ""),
            "market": raw_data.get("market", ""),
            "industry": raw_data.get("industry", ""),
            "sector": raw_data.get("sector", ""),
            "price": float(raw_data.get("price", 0.0)),
            "change_percent": float(raw_data.get("change_percent", 0.0)),
            "volume": int(raw_data.get("volume", 0)),
            "turnover": float(raw_data.get("turnover", 0.0)),
            "market_cap": float(raw_data.get("market_cap", 0.0)) if raw_data.get("market_cap") else None,
            "pe": float(raw_data.get("pe", 0.0)) if raw_data.get("pe") else None,
            "pb": float(raw_data.get("pb", 0.0)) if raw_data.get("pb") else None,
        }
    
    def normalize_daily_data(self, raw_data: dict) -> dict:
        """标准化日线数据"""
        return {
            "stock_code": raw_data.get("stock_code", ""),
            "trade_date": raw_data.get("trade_date", ""),
            "open": float(raw_data.get("open", 0.0)),
            "high": float(raw_data.get("high", 0.0)),
            "low": float(raw_data.get("low", 0.0)),
            "close": float(raw_data.get("close", 0.0)),
            "volume": int(raw_data.get("volume", 0)),
            "turnover": float(raw_data.get("turnover", 0.0)),
            "change_percent": float(raw_data.get("change_percent", 0.0)),
            "amplitude": float(raw_data.get("amplitude", 0.0)),
        }
    
    def normalize_minute_data(self, raw_data: dict) -> dict:
        """标准化分钟线数据"""
        return {
            "stock_code": raw_data.get("stock_code", ""),
            "trade_time": raw_data.get("trade_time", ""),
            "open": float(raw_data.get("open", 0.0)),
            "high": float(raw_data.get("high", 0.0)),
            "low": float(raw_data.get("low", 0.0)),
            "close": float(raw_data.get("close", 0.0)),
            "volume": int(raw_data.get("volume", 0)),
            "turnover": float(raw_data.get("turnover", 0.0)),
        }
    
    async def health_check(self) -> bool:
        """健康检查"""
        try:
            test_codes = ["000001", "600000"]
            for code in test_codes:
                result = await self.collect_stock_info(code)
                if result and result.get("code"):
                    return True
            return False
        except Exception as e:
            logger.error(f"健康检查失败: {str(e)}")
            return False
