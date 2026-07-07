"""
素材组织器基类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class MaterialOrganizer(ABC):
    """素材组织器基类"""
    
    @abstractmethod
    def get_id(self) -> str:
        """获取组织器ID"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """获取组织器名称"""
        pass
    
    @abstractmethod
    def is_active(self) -> bool:
        """是否启用"""
        pass
    
    @abstractmethod
    async def organize(self, materials: list[dict], **kwargs) -> list[dict]:
        """组织素材"""
        pass
    
    @abstractmethod
    def categorize(self, material: dict) -> str:
        """分类素材"""
        pass


class OrganizerManager:
    """素材组织器管理器（单例）"""
    
    _instance = None
    _organizers: Dict[str, MaterialOrganizer] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def register_organizer(self, organizer: MaterialOrganizer) -> None:
        """注册组织器"""
        if organizer.get_id() in self._organizers:
            from loguru import logger
            logger.warning(f"Organizer {organizer.get_id()} already registered")
        self._organizers[organizer.get_id()] = organizer
    
    def get_organizer(self, organizer_id: str) -> Optional[MaterialOrganizer]:
        """获取组织器"""
        return self._organizers.get(organizer_id)
    
    async def organize_all(self, materials: list[dict], **kwargs) -> list[dict]:
        """使用所有组织器组织素材"""
        results = materials.copy()
        for organizer in self._organizers.values():
            if organizer.is_active():
                results = await organizer.organize(results, **kwargs)
        return results


def get_organizer_manager() -> OrganizerManager:
    """获取组织器管理表单例"""
    return OrganizerManager()
