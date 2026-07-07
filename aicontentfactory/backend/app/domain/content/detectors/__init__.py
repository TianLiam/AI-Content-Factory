"""
内容检测器模块

包含：
- ContentDetector: 检测器基类
- DetectorManager: 检测器管理器
- AIContentDetector: AI 内容检测器
"""

from .base import ContentDetector
from .manager import DetectorManager, get_detector_manager, reset_detector_manager
from .ai_detector import AIContentDetector


def setup_default_detectors() -> None:
    """注册默认检测器"""
    manager = get_detector_manager()
    manager.register_detector(AIContentDetector())


__all__ = [
    "ContentDetector",
    "DetectorManager",
    "get_detector_manager",
    "reset_detector_manager",
    "AIContentDetector",
    "setup_default_detectors",
]
