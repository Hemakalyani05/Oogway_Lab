"""
OpenAI Provider (GPT-4o / GPT-4o-mini).
"""
import json
import httpx
from typing import AsyncGenerator, List, Dict, Any

from app.providers.base import BaseLLMProvider, LLMStreamChunk
from app.core.config import settings
from app.core.logging import logger


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, model_name: str = None, api_key: str = None):
        super().__init__(model_name or settings.OPENAI_MODEL)
        self.api_key = api_key or settings.OPENAI_API_KEY

    async def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 10)

    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.2
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        if not self.api_key:
            yield LLMStreamChunk(token="", is_finished=True, model_used=self.model_name, error="OpenAI API Key not configured")
            return

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload_messages = [{"role": "system", "content": system_prompt}] + messages
        payload = {
            "model": self.model_name,
            "messages": payload_messages,
            "stream": True,
            "temperature": temperature
        }

        url = "https://api.openai.com/v1/chat/completions"

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream("POST", url, headers=headers, json=payload) as response:
                    if response.status_code != 200:
                        err_bytes = await response.aread()
                        logger.error(f"OpenAI API error: {response.status_code} - {err_bytes.decode('utf-8')}")
                        yield LLMStreamChunk(token="", is_finished=True, model_used=self.model_name, error=f"OpenAI error: {response.status_code}")
                        return

                    async for line in response.aiter_lines():
                        if not line or not line.startswith("data: "):
                            continue
                        data_str = line[6:].strip()
                        if data_str == "[DONE]":
                            yield LLMStreamChunk(token="", is_finished=True, model_used=self.model_name)
                            break
                        try:
                            evt = json.loads(data_str)
                            delta_content = evt.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if delta_content:
                                yield LLMStreamChunk(token=delta_content, is_finished=False, model_used=self.model_name)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            logger.error(f"OpenAI request failed: {e}")
            yield LLMStreamChunk(token="", is_finished=True, model_used=self.model_name, error=str(e))

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.2
    ) -> str:
        tokens = []
        async for chunk in self.stream_chat(messages, system_prompt, temperature):
            if chunk.token:
                tokens.append(chunk.token)
        return "".join(tokens)
