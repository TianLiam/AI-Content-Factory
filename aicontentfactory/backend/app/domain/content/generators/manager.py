"""
内容生成器管理器
"""

from typing import List, Dict, Optional, Any
from loguru import logger

from .base import ContentGenerator


class GeneratorManager:
    """内容生成器管理器（单例）"""
    
    _instance = None
    _generators: Dict[str, ContentGenerator] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def register_generator(self, generator: ContentGenerator) -> None:
        """注册生成器"""
        if generator.get_id() in self._generators:
            logger.warning(f"Generator {generator.get_id()} already registered")
        self._generators[generator.get_id()] = generator
        logger.info(f"Generator registered: {generator.get_id()} - {generator.get_name()}")
    
    def unregister_generator(self, generator_id: str) -> None:
        """注销生成器"""
        if generator_id in self._generators:
            del self._generators[generator_id]
            logger.info(f"Generator unregistered: {generator_id}")
    
    def get_generator(self, generator_id: str) -> Optional[ContentGenerator]:
        """获取生成器"""
        return self._generators.get(generator_id)
    
    def get_generators(self) -> List[ContentGenerator]:
        """获取所有生成器"""
        return list(self._generators.values())
    
    def get_active_generators(self) -> List[ContentGenerator]:
        """获取所有启用的生成器"""
        return [g for g in self._generators.values() if g.is_active()]
    
    async def generate_with_provider(self, generator_id: str, topic: str, **kwargs) -> str:
        """使用指定生成器生成内容"""
        generator = self.get_generator(generator_id)
        if not generator:
            raise ValueError(f"Generator {generator_id} not found")
        if not generator.is_active():
            raise ValueError(f"Generator {generator_id} is not active")
        
        try:
            logger.info(f"Generating content with {generator.get_name()}")
            result = await generator.generate(topic, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Generation failed with {generator.get_name()}: {str(e)}")
            raise
    
    async def polish_with_provider(self, generator_id: str, content: str, **kwargs) -> str:
        """使用指定生成器润色内容"""
        generator = self.get_generator(generator_id)
        if not generator:
            raise ValueError(f"Generator {generator_id} not found")
        if not generator.is_active():
            raise ValueError(f"Generator {generator_id} is not active")
        
        try:
            logger.info(f"Polishing content with {generator.get_name()}")
            result = await generator.polish(content, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Polishing failed with {generator.get_name()}: {str(e)}")
            raise


def get_generator_manager() -> GeneratorManager:
    """获取生成器管理表单例"""
    return GeneratorManager()


def reset_generator_manager() -> None:
    """重置生成器管理器"""
    GeneratorManager._instance = None
    GeneratorManager._generators = {}
