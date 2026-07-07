"""
股票数据采集器模块导出
"""

from .base import StockCollector
from .manager import CollectorManager, get_collector_manager
from .eastmoney import EastmoneyCollector
from .sina import SinaCollector
from .tencent import TencentCollector

__all__ = [
    "StockCollector",
    "CollectorManager",
    "get_collector_manager",
    "EastmoneyCollector",
    "SinaCollector",
    "TencentCollector",
]
