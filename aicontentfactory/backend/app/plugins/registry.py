"""
Plugin Registry - 轻量级插件注册表

提供插件注册、发现和路由聚合功能，支持业务插件的自动挂载。

使用方式：
1. 定义插件类，实现 PluginInterface 接口
2. 在插件的 __init__.py 中调用 register_plugin()
3. 在主应用中通过 get_plugin_router() 获取所有插件路由

示例：
@register_plugin("stock_plugin", "股票决策插件")
class StockPlugin(PluginInterface):
    def get_router(self):
        from .api.router import router
        return router
    
    def get_scheduler(self):
        from .scheduler import setup_beat_schedule
        return setup_beat_schedule
    
    def get_models(self):
        from .models import __all__ as models
        return models
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Callable, Any
from fastapi import APIRouter

from app.core.logging import logger


class PluginInterface(ABC):
    """插件接口定义"""
    
    @abstractmethod
    def get_id(self) -> str:
        """获取插件唯一标识"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """获取插件显示名称"""
        pass
    
    @abstractmethod
    def is_enabled(self) -> bool:
        """插件是否启用"""
        pass
    
    @abstractmethod
    def get_router(self) -> Optional[APIRouter]:
        """获取插件的 API 路由"""
        pass
    
    @abstractmethod
    def get_scheduler(self) -> Optional[Callable]:
        """获取插件的定时任务配置函数"""
        pass
    
    @abstractmethod
    def get_models(self) -> Optional[List[str]]:
        """获取插件的数据库模型列表"""
        pass


class PluginRegistry:
    """插件注册表（单例）"""
    
    _instance = None
    _plugins: Dict[str, PluginInterface] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def register(self, plugin: PluginInterface) -> None:
        """注册插件"""
        if plugin.get_id() in self._plugins:
            logger.warning(f"Plugin {plugin.get_id()} already registered, overriding")
        self._plugins[plugin.get_id()] = plugin
        logger.info(f"Plugin registered: {plugin.get_id()} - {plugin.get_name()}")
    
    def unregister(self, plugin_id: str) -> None:
        """注销插件"""
        if plugin_id in self._plugins:
            del self._plugins[plugin_id]
            logger.info(f"Plugin unregistered: {plugin_id}")
    
    def get_plugin(self, plugin_id: str) -> Optional[PluginInterface]:
        """获取插件"""
        return self._plugins.get(plugin_id)
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """列出所有插件"""
        result = []
        for plugin_id, plugin in self._plugins.items():
            result.append({
                "id": plugin_id,
                "name": plugin.get_name(),
                "enabled": plugin.is_enabled(),
            })
        return result
    
    def get_enabled_plugins(self) -> List[PluginInterface]:
        """获取所有启用的插件"""
        return [p for p in self._plugins.values() if p.is_enabled()]
    
    def get_router(self) -> APIRouter:
        """聚合所有启用插件的路由"""
        router = APIRouter()
        for plugin in self.get_enabled_plugins():
            plugin_router = plugin.get_router()
            if plugin_router:
                router.include_router(plugin_router)
                logger.info(f"Plugin router included: {plugin.get_id()}")
        return router
    
    def setup_schedulers(self) -> None:
        """设置所有启用插件的定时任务"""
        for plugin in self.get_enabled_plugins():
            scheduler_func = plugin.get_scheduler()
            if scheduler_func:
                scheduler_func()
                logger.info(f"Plugin scheduler setup: {plugin.get_id()}")
    
    @property
    def plugins(self) -> Dict[str, PluginInterface]:
        """获取所有插件字典"""
        return self._plugins


def get_plugin_registry() -> PluginRegistry:
    """获取插件注册表单例"""
    return PluginRegistry()


def register_plugin(plugin_id: str, name: str) -> Callable:
    """插件注册装饰器"""
    def decorator(cls: type) -> type:
        if not issubclass(cls, PluginInterface):
            raise TypeError(f"Class {cls.__name__} must inherit from PluginInterface")
        
        class RegisteredPlugin(cls):
            def get_id(self) -> str:
                return plugin_id
            
            def get_name(self) -> str:
                return name
        
        instance = RegisteredPlugin()
        get_plugin_registry().register(instance)
        return cls
    
    return decorator


def get_plugin_router() -> APIRouter:
    """获取所有插件的聚合路由"""
    return get_plugin_registry().get_router()


__all__ = [
    "PluginInterface",
    "PluginRegistry",
    "get_plugin_registry",
    "register_plugin",
    "get_plugin_router",
]
