"""
股票决策插件 - Stock Decision Plugin

提供股票数据采集、分析和智能决策功能。

核心功能：
- 多源股票数据采集（东方财富、新浪、腾讯）
- 股票实时行情、日线、分钟线数据管理
- 资金流向、市场情绪、板块分析
- 智能决策引擎，基于多因子评分生成买卖建议
"""

from fastapi import APIRouter
from typing import Optional, List, Callable

from app.plugins import PluginInterface, register_plugin


@register_plugin("stock_plugin", "股票决策插件")
class StockPlugin(PluginInterface):
    """股票决策插件实现"""
    
    _enabled = True
    
    def is_enabled(self) -> bool:
        """插件是否启用"""
        return self._enabled
    
    def get_router(self) -> Optional[APIRouter]:
        """获取插件的 API 路由"""
        from .api.router import router
        return router
    
    def get_scheduler(self) -> Optional[Callable]:
        """获取插件的定时任务配置函数"""
        return None
    
    def get_models(self) -> Optional[List[str]]:
        """获取插件的数据库模型列表"""
        from .models import __all__ as models
        return models


__all__ = [
    "StockPlugin",
]
