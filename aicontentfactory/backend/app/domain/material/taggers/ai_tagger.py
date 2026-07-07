"""
AI 素材标签器 - 使用 LLM 提取和建议标签
"""

from typing import List

from app.domain.ai.providers.base import LLMProvider
from app.domain.ai.providers import get_provider_manager

from .base import MaterialTagger


class AIMaterialTagger(MaterialTagger):
    """AI 素材标签器"""
    
    def __init__(self, llm_provider_id: str = None):
        self.llm_provider_id = llm_provider_id
    
    def get_id(self) -> str:
        return "ai"
    
    def get_name(self) -> str:
        return "AI 标签器"
    
    def is_active(self) -> bool:
        return True
    
    async def extract_tags(self, content: str, **kwargs) -> List[str]:
        """从内容中提取标签"""
        provider = self._get_provider()
        if not provider:
            return []
        
        prompt = f"""请从以下内容中提取最相关的标签（关键词）：

内容：
{content}

要求：
1. 提取 5-10 个最核心的标签
2. 标签用逗号分隔
3. 不要包含无关的标签

请直接输出标签，不要包含任何额外的解释或说明。"""
        
        result = await provider.generate(prompt, **kwargs)
        return [tag.strip() for tag in result.split(",") if tag.strip()]
    
    async def suggest_tags(self, content: str, **kwargs) -> List[str]:
        """建议标签"""
        provider = self._get_provider()
        if not provider:
            return []
        
        prompt = f"""请为以下内容建议合适的标签（关键词）：

内容：
{content}

要求：
1. 建议 5-10 个相关标签
2. 标签用逗号分隔
3. 标签要具有分类和检索价值

请直接输出标签，不要包含任何额外的解释或说明。"""
        
        result = await provider.generate(prompt, **kwargs)
        return [tag.strip() for tag in result.split(",") if tag.strip()]
    
    def _get_provider(self) -> LLMProvider:
        """获取 LLM Provider"""
        manager = get_provider_manager()
        if self.llm_provider_id:
            return manager.get_provider(self.llm_provider_id)
        return manager.get_active_provider()
