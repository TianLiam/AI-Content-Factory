"""
素材标签管理器
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class MaterialTagger(ABC):
    """素材标签器基类"""
    
    @abstractmethod
    def get_id(self) -> str:
        """获取标签器ID"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """获取标签器名称"""
        pass
    
    @abstractmethod
    def is_active(self) -> bool:
        """是否启用"""
        pass
    
    @abstractmethod
    async def extract_tags(self, content: str, **kwargs) -> List[str]:
        """从内容中提取标签"""
        pass
    
    @abstractmethod
    async def suggest_tags(self, content: str, **kwargs) -> List[str]:
        """建议标签"""
        pass


class TaggerManager:
    """素材标签器管理器（单例）"""
    
    _instance = None
    _taggers: Dict[str, MaterialTagger] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def register_tagger(self, tagger: MaterialTagger) -> None:
        """注册标签器"""
        if tagger.get_id() in self._taggers:
            from loguru import logger
            logger.warning(f"Tagger {tagger.get_id()} already registered")
        self._taggers[tagger.get_id()] = tagger
    
    def get_tagger(self, tagger_id: str) -> Optional[MaterialTagger]:
        """获取标签器"""
        return self._taggers.get(tagger_id)
    
    async def extract_tags_from_content(self, content: str, **kwargs) -> List[str]:
        """从内容中提取标签"""
        all_tags = []
        for tagger in self._taggers.values():
            if tagger.is_active():
                tags = await tagger.extract_tags(content, **kwargs)
                all_tags.extend(tags)
        return list(set(all_tags))
    
    async def suggest_tags_for_content(self, content: str, **kwargs) -> List[str]:
        """建议标签"""
        all_tags = []
        for tagger in self._taggers.values():
            if tagger.is_active():
                tags = await tagger.suggest_tags(content, **kwargs)
                all_tags.extend(tags)
        return list(set(all_tags))


def get_tagger_manager() -> TaggerManager:
    """获取标签器管理表单例"""
    return TaggerManager()
