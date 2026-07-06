from app.domain.ai.providers.base import SignalProvider


class ZhihuProvider(SignalProvider):
    def get_id(self) -> str:
        return "zhihu"

    def get_name(self) -> str:
        return "知乎"

    def is_active(self) -> bool:
        return True

    async def collect(self, **kwargs) -> list[dict]:
        return []
