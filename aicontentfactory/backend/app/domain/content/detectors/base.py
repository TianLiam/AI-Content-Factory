"""
内容检测器基类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class ContentDetector(ABC):
    """内容检测器基类"""
    
    @abstractmethod
    def get_id(self) -> str:
        """获取检测器ID"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """获取检测器名称"""
        pass
    
    @abstractmethod
    def is_active(self) -> bool:
        """是否启用"""
        pass
    
    @abstractmethod
    async def detect(self, content: str, **kwargs) -> Dict[str, Any]:
        """检测内容"""
        pass
