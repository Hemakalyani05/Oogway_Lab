"""
Ollama Provider for local LLM inference (llama3.2, mistral, deepseek-r1, etc.).
"""
import json
import httpx
from typing import AsyncGenerator, List, Dict, Any

from app.providers.base import BaseLLMProvider, LLMStreamChunk
from app.core.config import settings
from app.core.logging import logger


class OllamaProvider(BaseLLMProvider):
    def __init__(self, model_name: str = None, base_url: str = None):
        super().__init__(model_name or settings.OLLAMA_MODEL)
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")

    async def is_available(self) -> bool:
        """Checks if local Ollama daemon is running."""
        try:
            async with httpx.AsyncClient(timeout=1.5) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                return res.status_code == 200
        except Exception:
            return False

    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.2
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        payload_messages = [{"role": "system", "content": system_prompt}] + messages
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model_name,
            "messages": payload_messages,
            "stream": True,
            "options": {
                "temperature": temperature
            }
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream("POST", url, json=payload) as response:
                    if response.status_code != 200:
                        err_text = await response.aread()
                        logger.error(f"Ollama API error: {response.status_code} - {err_text.decode('utf-8')}")
                        yield LLMStreamChunk(token="", is_finished=True, model_used=self.model_name, error=f"Ollama error: {response.status_code}")
                        return

                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            chunk_text = data.get("message", {}).get("content", "")
                            is_done = data.get("done", False)
                            yield LLMStreamChunk(token=chunk_text, is_finished=is_done, model_used=self.model_name)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            yield LLMStreamChunk(token="", is_finished=True, model_used=self.model_name, error=f"Ollama unreachable: {str(e)}")

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
