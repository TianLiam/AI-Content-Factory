"""
AI 内容生成器 - 使用 LLM Provider 生成内容
"""

from typing import List, Dict, Any

from app.domain.ai.providers.base import LLMProvider
from app.domain.ai.providers import get_provider_manager

from .base import ContentGenerator


class AIContentGenerator(ContentGenerator):
    """AI 内容生成器"""
    
    def __init__(self, llm_provider_id: str = None):
        self.llm_provider_id = llm_provider_id
    
    def get_id(self) -> str:
        return "ai"
    
    def get_name(self) -> str:
        return "AI 生成器"
    
    def is_active(self) -> bool:
        return True
    
    async def generate(self, topic: str, **kwargs) -> str:
        """使用 LLM 生成内容"""
        provider = self._get_provider()
        if not provider:
            return "No LLM provider available"
        
        prompt = f"""你是一个专业的内容创作助手。请根据以下主题生成一篇高质量的文章：

主题：{topic}

要求：
1. 结构清晰，有标题、引言、正文、结论
2. 内容丰富，有深度
3. 语言流畅，符合中文表达习惯
4. 字数约 1000-2000 字

请直接输出文章内容，不要包含任何额外的解释或说明。"""
        
        result = await provider.generate(prompt, **kwargs)
        return result
    
    async def polish(self, content: str, **kwargs) -> str:
        """使用 LLM 润色内容"""
        provider = self._get_provider()
        if not provider:
            return content
        
        prompt = f"""你是一个专业的内容润色助手。请对以下文章进行润色：

原文：
{content}

要求：
1. 保持原意不变
2. 优化语言表达，使其更加流畅自然
3. 修正语法和用词错误
4. 提升文章的可读性和专业性

请直接输出润色后的文章，不要包含任何额外的解释或说明。"""
        
        result = await provider.generate(prompt, **kwargs)
        return result
    
    def _get_provider(self) -> LLMProvider:
        """获取 LLM Provider"""
        manager = get_provider_manager()
        if self.llm_provider_id:
            return manager.get_provider(self.llm_provider_id)
        return manager.get_active_provider()
