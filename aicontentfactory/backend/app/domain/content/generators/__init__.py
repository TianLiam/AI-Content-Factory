"""
内容生成器模块

包含：
- ContentGenerator: 生成器基类
- GeneratorManager: 生成器管理器
- AIContentGenerator: AI 内容生成器
"""

from .base import ContentGenerator
from .manager import GeneratorManager, get_generator_manager, reset_generator_manager
from .ai_generator import AIContentGenerator


def setup_default_generators() -> None:
    """注册默认生成器"""
    manager = get_generator_manager()
    manager.register_generator(AIContentGenerator())


__all__ = [
    "ContentGenerator",
    "GeneratorManager",
    "get_generator_manager",
    "reset_generator_manager",
    "AIContentGenerator",
    "setup_default_generators",
]
