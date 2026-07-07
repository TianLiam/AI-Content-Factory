"""
素材标签器模块
"""

from .base import MaterialTagger, TaggerManager, get_tagger_manager
from .ai_tagger import AIMaterialTagger


def setup_default_taggers() -> None:
    """注册默认标签器"""
    manager = get_tagger_manager()
    manager.register_tagger(AIMaterialTagger())


__all__ = [
    "MaterialTagger",
    "TaggerManager",
    "get_tagger_manager",
    "AIMaterialTagger",
    "setup_default_taggers",
]
