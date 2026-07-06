from abc import ABC, abstractmethod
from typing import Optional


class LLMProvider(ABC):
    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def is_active(self) -> bool:
        pass

    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    async def chat(self, messages: list[dict], **kwargs) -> str:
        pass


class SignalProvider(ABC):
    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def is_active(self) -> bool:
        pass

    @abstractmethod
    async def collect(self, **kwargs) -> list[dict]:
        pass


class AiDetector(ABC):
    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def is_active(self) -> bool:
        pass

    @abstractmethod
    async def detect(self, content: str) -> dict:
        pass
