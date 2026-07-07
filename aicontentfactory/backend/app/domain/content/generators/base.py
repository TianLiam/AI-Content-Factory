"""
内容生成器基类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class ContentGenerator(ABC):
    """内容生成器基类"""
    
    @abstractmethod
    def get_id(self) -> str:
        """获取生成器ID"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """获取生成器名称"""
        pass
    
    @abstractmethod
    def is_active(self) -> bool:
        """是否启用"""
        pass
    
    @abstractmethod
    async def generate(self, topic: str, **kwargs) -> str:
        """生成内容"""
        pass
    
    @abstractmethod
    async def polish(self, content: str, **kwargs) -> str:
        """润色内容"""
        pass
