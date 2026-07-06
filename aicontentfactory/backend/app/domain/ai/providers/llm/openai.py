from typing import Optional
import httpx

from app.domain.ai.providers.base import LLMProvider
from app.core.config import settings


class OpenAIProvider(LLMProvider):
    def get_id(self) -> str:
        return "openai"

    def get_name(self) -> str:
        return "OpenAI"

    def is_active(self) -> bool:
        return settings.OPENAI_API_KEY is not None

    async def generate(self, prompt: str, **kwargs) -> str:
        model = kwargs.get("model", "gpt-4o-mini")
        temperature = kwargs.get("temperature", 0.7)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                },
                timeout=60,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    async def chat(self, messages: list[dict], **kwargs) -> str:
        model = kwargs.get("model", "gpt-4o-mini")
        temperature = kwargs.get("temperature", 0.7)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                },
                timeout=60,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
