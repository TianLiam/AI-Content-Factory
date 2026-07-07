"""
股票决策策略基类定义
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class DecisionStrategy(ABC):
    """股票决策策略基类"""
    
    def __init__(self):
        self.name = ""
        self.description = ""
    
    @abstractmethod
    def get_id(self) -> str:
        """获取策略唯一标识"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """获取策略名称"""
        pass
    
    @abstractmethod
    def calculate_score(self, stock_data: Dict[str, Any]) -> float:
        """计算策略评分"""
        pass
    
    @abstractmethod
    def analyze(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行策略分析"""
        pass
    
    def get_description(self) -> str:
        """获取策略描述"""
        return self.description
    
    def validate_input(self, stock_data: Dict[str, Any]) -> bool:
        """验证输入数据"""
        required_fields = ["stock_info", "daily_data", "indicators"]
        for field in required_fields:
            if field not in stock_data or not stock_data[field]:
                return False
        return True
