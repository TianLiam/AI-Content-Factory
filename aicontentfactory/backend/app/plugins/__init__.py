"""
AI Signal Platform - Plugins

插件模块，所有业务插件在此注册和管理。

包含：
- PluginRegistry: 插件注册表（单例）
- PluginInterface: 插件接口定义
- register_plugin: 插件注册装饰器
- get_plugin_router: 获取所有插件的聚合路由
"""

from .registry import (
    PluginInterface,
    PluginRegistry,
    get_plugin_registry,
    register_plugin,
    get_plugin_router,
)

__all__ = [
    "PluginInterface",
    "PluginRegistry",
    "get_plugin_registry",
    "register_plugin",
    "get_plugin_router",
]
