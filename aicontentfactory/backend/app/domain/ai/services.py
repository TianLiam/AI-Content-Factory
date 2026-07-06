from sqlalchemy.orm import Session

from app.domain.ai.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    GenerateRequest,
    GenerateResponse,
    PolishRequest,
    PolishResponse,
    DetectAIRequest,
    DetectAIResponse,
    ProviderInfo,
)
from app.domain.ai.providers import (
    LLMProvider,
    SignalProvider,
    OpenAIProvider,
    DeepSeekProvider,
    WeChatProvider,
    ToutiaoProvider,
    ZhihuProvider,
)


_llm_providers: list[LLMProvider] = [
    OpenAIProvider(),
    DeepSeekProvider(),
]

_signal_providers: list[SignalProvider] = [
    WeChatProvider(),
    ToutiaoProvider(),
    ZhihuProvider(),
]


def _get_active_llm_provider() -> LLMProvider | None:
    for provider in _llm_providers:
        if provider.is_active():
            return provider
    return None


async def analyze_signal(db: Session, payload: AnalysisRequest) -> AnalysisResponse:
    return AnalysisResponse()


async def generate_article(payload: GenerateRequest) -> GenerateResponse:
    provider = _get_active_llm_provider()
    if not provider:
        return GenerateResponse(content="No LLM provider available")

    prompt = f"""
    根据以下大纲和素材，生成一篇适合{payload.target_platform}平台的文章，语气为{payload.tone}。
    
    大纲：
    {payload.outline}
    
    素材：
    {payload.materials}
    
    请输出完整的文章内容。
    """

    content = await provider.generate(prompt)
    return GenerateResponse(content=content, outline=payload.outline)


async def polish_article(payload: PolishRequest) -> PolishResponse:
    provider = _get_active_llm_provider()
    if not provider:
        return PolishResponse(content=payload.content)

    prompt = f"""
    请润色以下文章，使其更适合{payload.target_platform}平台发布。
    要求：
    1. 保持原意不变
    2. 提升文章质量
    3. 去除AI味
    4. 语言流畅自然
    
    文章内容：
    {payload.content}
    """

    content = await provider.generate(prompt)
    return PolishResponse(content=content)


async def detect_ai(payload: DetectAIRequest) -> DetectAIResponse:
    return DetectAIResponse(
        score=0,
        ai_probability=0.0,
        repeat_sentence=[],
        suggestions=[],
    )


def list_providers() -> list[ProviderInfo]:
    providers = []
    for provider in _llm_providers + _signal_providers:
        providers.append(
            ProviderInfo(
                id=provider.get_id(),
                name=provider.get_name(),
                status="active" if provider.is_active() else "inactive",
            )
        )
    return providers


async def test_provider(provider_id: str) -> dict:
    for provider in _llm_providers:
        if provider.get_id() == provider_id:
            if not provider.is_active():
                return {"success": False, "message": "Provider is not active"}
            try:
                result = await provider.generate("Hello, world!")
                return {"success": True, "message": "Test passed", "result": result[:50]}
            except Exception as e:
                return {"success": False, "message": str(e)}

    for provider in _signal_providers:
        if provider.get_id() == provider_id:
            try:
                result = await provider.collect()
                return {"success": True, "message": "Test passed", "result": len(result)}
            except Exception as e:
                return {"success": False, "message": str(e)}

    return {"success": False, "message": "Provider not found"}
