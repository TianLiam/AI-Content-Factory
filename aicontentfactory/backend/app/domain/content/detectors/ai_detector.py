"""
AI 内容检测器 - 使用 LLM 检测内容是否由 AI 生成
"""

from typing import Dict, Any

from app.domain.ai.providers.base import LLMProvider
from app.domain.ai.providers import get_provider_manager

from .base import ContentDetector


class AIContentDetector(ContentDetector):
    """AI 内容检测器"""
    
    def __init__(self, llm_provider_id: str = None):
        self.llm_provider_id = llm_provider_id
    
    def get_id(self) -> str:
        return "ai"
    
    def get_name(self) -> str:
        return "AI 检测器"
    
    def is_active(self) -> bool:
        return True
    
    async def detect(self, content: str, **kwargs) -> Dict[str, Any]:
        """检测内容是否由 AI 生成"""
        provider = self._get_provider()
        if not provider:
            return {
                "score": 0,
                "ai_probability": 0.0,
                "repeat_sentence": [],
                "suggestions": []
            }
        
        prompt = f"""你是一个专业的 AI 内容检测助手。请分析以下文本，判断其是否由 AI 生成：

文本内容：
{content}

请返回 JSON 格式的检测结果，包含以下字段：
1. score: 检测置信度评分（0-100）
2. ai_probability: AI 生成概率（0.0-1.0）
3. repeat_sentence: 重复句子列表
4. suggestions: 修改建议列表

请直接输出 JSON，不要包含任何额外的解释或说明。"""
        
        result = await provider.generate(prompt, **kwargs)
        try:
            import json
            return json.loads(result)
        except Exception:
            return {
                "score": 50,
                "ai_probability": 0.5,
                "repeat_sentence": [],
                "suggestions": []
            }
    
    def _get_provider(self) -> LLMProvider:
        """获取 LLM Provider"""
        manager = get_provider_manager()
        if self.llm_provider_id:
            return manager.get_provider(self.llm_provider_id)
        return manager.get_active_provider()
