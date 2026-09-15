"""
Anthropic Claude Provider (Claude 3.7 / 3.5 Sonnet).
"""
import json
import httpx
from typing import AsyncGenerator, List, Dict, Any

from app.providers.base import BaseLLMProvider, LLMStreamChunk
from app.core.config import settings
from app.core.logging import logger


class AnthropicProvider(BaseLLMProvider):
    def __init__(self, model_name: str = None, api_key: str = None):
        super().__init__(model_name or settings.ANTHROPIC_MODEL)
        self.api_key = api_key or settings.ANTHROPIC_API_KEY

    async def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 10)

    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.2
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        if not self.api_key:
            yield LLMStreamChunk(token="", is_finished=True, model_used=self.model_name, error="Anthropic API Key not configured")
            return

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        # Filter and format messages for Anthropic API
        formatted_messages = []
        for m in messages:
            if m["role"] in ["user", "assistant"]:
                formatted_messages.append({"role": m["role"], "content": m["content"]})

        payload = {
            "model": self.model_name,
            "max_tokens": 4096,
            "system": system_prompt,
            "messages": formatted_messages,
            "stream": True,
            "temperature": temperature
        }

        url = "https://api.anthropic.com/v1/messages"

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream("POST", url, headers=headers, json=payload) as response:
                    if response.status_code != 200:
                        err_bytes = await response.aread()
                        logger.error(f"Anthropic API error: {response.status_code} - {err_bytes.decode('utf-8')}")
                        yield LLMStreamChunk(token="", is_finished=True, model_used=self.model_name, error=f"Anthropic API error: {response.status_code}")
                        return

                    async for line in response.aiter_lines():
                        if not line or not line.startswith("data: "):
                            continue
                        data_str = line[6:].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            evt = json.loads(data_str)
                            if evt.get("type") == "content_block_delta":
                                delta_text = evt.get("delta", {}).get("text", "")
                                yield LLMStreamChunk(token=delta_text, is_finished=False, model_used=self.model_name)
                            elif evt.get("type") == "message_stop":
                                yield LLMStreamChunk(token="", is_finished=True, model_used=self.model_name)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            logger.error(f"Anthropic request failed: {e}")
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
