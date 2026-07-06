from app.domain.ai.providers.base import SignalProvider


class ToutiaoProvider(SignalProvider):
    def get_id(self) -> str:
        return "toutiao"

    def get_name(self) -> str:
        return "今日头条"

    def is_active(self) -> bool:
        return True

    async def collect(self, **kwargs) -> list[dict]:
        return []
