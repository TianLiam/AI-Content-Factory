"""
股票决策策略管理器 - 管理所有策略和决策引擎
"""

from typing import List, Dict, Optional, Any
from loguru import logger

from .base import DecisionStrategy
from .decision_engine import DecisionEngine


class StrategyManager:
    """股票决策策略管理器（单例）"""
    
    _instance = None
    _strategies: Dict[str, DecisionStrategy] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._engine = DecisionEngine()
        return cls._instance
    
    @property
    def engine(self) -> DecisionEngine:
        """获取决策引擎"""
        return self._engine
    
    def register_strategy(self, strategy: DecisionStrategy) -> None:
        """注册策略"""
        if strategy.get_id() in self._strategies:
            logger.warning(f"策略 {strategy.get_id()} 已注册")
        self._strategies[strategy.get_id()] = strategy
        logger.info(f"策略注册成功: {strategy.get_id()} - {strategy.get_name()}")
    
    def unregister_strategy(self, strategy_id: str) -> None:
        """注销策略"""
        if strategy_id in self._strategies:
            del self._strategies[strategy_id]
            logger.info(f"策略注销成功: {strategy_id}")
    
    def get_strategy(self, strategy_id: str) -> Optional[DecisionStrategy]:
        """获取策略"""
        return self._strategies.get(strategy_id)
    
    def get_strategies(self) -> List[DecisionStrategy]:
        """获取所有策略"""
        return list(self._strategies.values())
    
    async def analyze(self, stock_data: Dict[str, Any], strategy_id: str = None) -> Dict[str, Any]:
        """执行分析"""
        if strategy_id and strategy_id in self._strategies:
            strategy = self._strategies[strategy_id]
            logger.info(f"使用策略 {strategy.get_name()} 进行分析")
            return strategy.analyze(stock_data)
        else:
            logger.info("使用默认决策引擎进行分析")
            return self._engine.analyze(stock_data)
    
    async def analyze_batch(self, stock_codes: List[str], stock_data_map: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """批量分析"""
        results = {}
        for stock_code in stock_codes:
            if stock_code in stock_data_map:
                try:
                    result = await self.analyze(stock_data_map[stock_code])
                    results[stock_code] = result
                except Exception as e:
                    logger.error(f"分析股票 {stock_code} 失败: {str(e)}")
                    results[stock_code] = {"error": str(e)}
        return results
    
    def get_strategy_info(self) -> List[Dict[str, Any]]:
        """获取所有策略信息"""
        info = []
        for strategy in self._strategies.values():
            info.append({
                "id": strategy.get_id(),
                "name": strategy.get_name(),
                "description": strategy.get_description(),
            })
        return info


def get_strategy_manager() -> StrategyManager:
    """获取策略管理表单例"""
    return StrategyManager()


def initialize_strategies() -> None:
    """初始化所有策略"""
    manager = get_strategy_manager()
    logger.info("股票决策策略初始化完成")
