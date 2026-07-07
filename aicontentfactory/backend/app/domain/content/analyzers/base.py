"""
内容分析器基类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class ContentAnalyzer(ABC):
    """内容分析器基类"""
    
    @abstractmethod
    def get_id(self) -> str:
        """获取分析器ID"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """获取分析器名称"""
        pass
    
    @abstractmethod
    def is_active(self) -> bool:
        """是否启用"""
        pass
    
    @abstractmethod
    async def analyze(self, content: str, **kwargs) -> Dict[str, Any]:
        """分析内容"""
        pass
    
    def get_score(self, result: Dict[str, Any]) -> int:
        """获取评分（0-100）"""
        return result.get("score", 50)
