"""
内容分析器管理器
"""

from typing import List, Dict, Optional, Any
from loguru import logger

from .base import ContentAnalyzer


class AnalyzerManager:
    """内容分析器管理器（单例）"""
    
    _instance = None
    _analyzers: Dict[str, ContentAnalyzer] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def register_analyzer(self, analyzer: ContentAnalyzer) -> None:
        """注册分析器"""
        if analyzer.get_id() in self._analyzers:
            logger.warning(f"Analyzer {analyzer.get_id()} already registered")
        self._analyzers[analyzer.get_id()] = analyzer
        logger.info(f"Analyzer registered: {analyzer.get_id()} - {analyzer.get_name()}")
    
    def unregister_analyzer(self, analyzer_id: str) -> None:
        """注销分析器"""
        if analyzer_id in self._analyzers:
            del self._analyzers[analyzer_id]
            logger.info(f"Analyzer unregistered: {analyzer_id}")
    
    def get_analyzer(self, analyzer_id: str) -> Optional[ContentAnalyzer]:
        """获取分析器"""
        return self._analyzers.get(analyzer_id)
    
    def get_analyzers(self) -> List[ContentAnalyzer]:
        """获取所有分析器"""
        return list(self._analyzers.values())
    
    def get_active_analyzers(self) -> List[ContentAnalyzer]:
        """获取所有启用的分析器"""
        return [a for a in self._analyzers.values() if a.is_active()]
    
    async def analyze_with_provider(self, analyzer_id: str, content: str, **kwargs) -> Dict[str, Any]:
        """使用指定分析器分析内容"""
        analyzer = self.get_analyzer(analyzer_id)
        if not analyzer:
            raise ValueError(f"Analyzer {analyzer_id} not found")
        if not analyzer.is_active():
            raise ValueError(f"Analyzer {analyzer_id} is not active")
        
        try:
            logger.info(f"Analyzing content with {analyzer.get_name()}")
            result = await analyzer.analyze(content, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Analysis failed with {analyzer.get_name()}: {str(e)}")
            raise
    
    async def analyze_all(self, content: str, **kwargs) -> Dict[str, Any]:
        """使用所有启用的分析器分析内容"""
        results = {}
        for analyzer in self.get_active_analyzers():
            try:
                result = await self.analyze_with_provider(analyzer.get_id(), content, **kwargs)
                results[analyzer.get_id()] = result
            except Exception as e:
                logger.error(f"Failed to analyze with {analyzer.get_name()}: {str(e)}")
                results[analyzer.get_id()] = {"error": str(e)}
        return results


def get_analyzer_manager() -> AnalyzerManager:
    """获取分析器管理表单例"""
    return AnalyzerManager()


def reset_analyzer_manager() -> None:
    """重置分析器管理器"""
    AnalyzerManager._instance = None
    AnalyzerManager._analyzers = {}
