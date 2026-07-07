"""
信号采集器模块

包含：
- SignalCollector: 采集器基类
- CollectorManager: 采集器管理器
- WeChatCollector: 微信公众号采集器
- ToutiaoCollector: 今日头条采集器
- ZhihuCollector: 知乎采集器
"""

from .base import SignalCollector
from .manager import CollectorManager, get_collector_manager, reset_collector_manager
from .wechat import WeChatCollector
from .toutiao import ToutiaoCollector
from .zhihu import ZhihuCollector


def setup_default_collectors() -> None:
    """注册默认采集器"""
    manager = get_collector_manager()
    manager.register_collector(WeChatCollector())
    manager.register_collector(ToutiaoCollector())
    manager.register_collector(ZhihuCollector())


__all__ = [
    "SignalCollector",
    "CollectorManager",
    "get_collector_manager",
    "reset_collector_manager",
    "WeChatCollector",
    "ToutiaoCollector",
    "ZhihuCollector",
    "setup_default_collectors",
]
