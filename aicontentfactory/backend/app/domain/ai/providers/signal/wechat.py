from app.domain.ai.providers.base import SignalProvider


class WeChatProvider(SignalProvider):
    def get_id(self) -> str:
        return "wechat"

    def get_name(self) -> str:
        return "微信公众号"

    def is_active(self) -> bool:
        return True

    async def collect(self, **kwargs) -> list[dict]:
        return []
