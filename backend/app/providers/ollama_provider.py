"""
Ollama Provider for local LLM inference
(llama3.2, mistral, deepseek-r1, etc.).
"""

import json
import httpx
from typing import AsyncGenerator, List, Dict

from app.providers.base import BaseLLMProvider, LLMStreamChunk
from app.core.config import settings
from app.core.logging import logger


class OllamaProvider(BaseLLMProvider):

    def __init__(self, model_name: str = None, base_url: str = None):
        super().__init__(model_name or settings.OLLAMA_MODEL)
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")

    async def is_available(self) -> bool:
        """Check whether the local Ollama daemon is running."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"{self.base_url}/api/tags"
                )

                if response.status_code == 200:
                    logger.info(
                        f"Ollama is available at {self.base_url}"
                    )
                    return True

                logger.warning(
                    f"Ollama returned status {response.status_code}"
                )
                return False

        except Exception as e:
            logger.warning(
                f"Ollama availability check failed: {e}"
            )
            return False

    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.2
    ) -> AsyncGenerator[LLMStreamChunk, None]:

        # Add the system prompt before the conversation.
        payload_messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ] + messages

        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.model_name,
            "messages": payload_messages,
            "stream": True,
            "options": {
                "temperature": temperature
            }
        }

        logger.info(
            f"Sending request to Ollama: "
            f"model={self.model_name}"
        )

        try:
            # Ollama can take some time to load the model initially,
            # so use a longer timeout.
            timeout = httpx.Timeout(
                connect=10.0,
                read=300.0,
                write=30.0,
                pool=30.0
            )

            async with httpx.AsyncClient(
                timeout=timeout
            ) as client:

                async with client.stream(
                    "POST",
                    url,
                    json=payload
                ) as response:

                    if response.status_code != 200:

                        error_bytes = await response.aread()

                        error_text = error_bytes.decode(
                            "utf-8",
                            errors="replace"
                        )

                        logger.error(
                            f"Ollama API error: "
                            f"{response.status_code} - "
                            f"{error_text}"
                        )

                        yield LLMStreamChunk(
                            token="",
                            is_finished=True,
                            model_used=self.model_name,
                            error=(
                                f"Ollama error: "
                                f"{response.status_code}"
                            )
                        )

                        return

                    finished = False

                    async for line in response.aiter_lines():

                        if not line:
                            continue

                        try:
                            data = json.loads(line)

                        except json.JSONDecodeError:
                            logger.warning(
                                "Received invalid JSON from Ollama"
                            )
                            continue

                        message = data.get(
                            "message",
                            {}
                        )

                        chunk_text = message.get(
                            "content",
                            ""
                        )

                        is_done = data.get(
                            "done",
                            False
                        )

                        if chunk_text:
                            yield LLMStreamChunk(
                                token=chunk_text,
                                is_finished=False,
                                model_used=self.model_name
                            )

                        if is_done:
                            finished = True

                            yield LLMStreamChunk(
                                token="",
                                is_finished=True,
                                model_used=self.model_name
                            )

                            break

                    # Safety fallback in case Ollama closes the
                    # connection without sending done=true.
                    if not finished:
                        yield LLMStreamChunk(
                            token="",
                            is_finished=True,
                            model_used=self.model_name
                        )

        except httpx.TimeoutException as e:

            logger.error(
                f"Ollama request timed out: {e}"
            )

            yield LLMStreamChunk(
                token="",
                is_finished=True,
                model_used=self.model_name,
                error=(
                    "Ollama request timed out. "
                    "The local model may need more time."
                )
            )

        except Exception as e:

            logger.error(
                f"Failed to connect to Ollama: {e}"
            )

            yield LLMStreamChunk(
                token="",
                is_finished=True,
                model_used=self.model_name,
                error=(
                    f"Ollama unreachable: {str(e)}"
                )
            )

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.2
    ) -> str:

        tokens = []

        async for chunk in self.stream_chat(
            messages,
            system_prompt,
            temperature
        ):

            if chunk.token:
                tokens.append(chunk.token)

        return "".join(tokens)