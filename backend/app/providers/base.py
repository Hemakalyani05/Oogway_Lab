"""
Base LLM Provider Interface for pluggable model execution.
"""
from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Dict, Any, Optional
from pydantic import BaseModel


class LLMStreamChunk(BaseModel):
    token: str
    is_finished: bool = False
    model_used: str = ""
    error: Optional[str] = None


class BaseLLMProvider(ABC):
    """Abstract Base Class for LLM Providers."""

    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    async def is_available(self) -> bool:
        """Checks if the provider is reachable and configured."""
        pass

    @abstractmethod
    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.2
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        """Streams chat completion tokens asynchronously."""
        pass

    @abstractmethod
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.2
    ) -> str:
        """Generates a complete response synchronously/non-streaming."""
        pass
