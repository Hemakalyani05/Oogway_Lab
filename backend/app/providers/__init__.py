"""
Provider factory and registry for pluggable LLM inference.
"""
from typing import Dict, Any, List
from app.providers.base import BaseLLMProvider
from app.providers.ollama_provider import OllamaProvider
from app.providers.anthropic_provider import AnthropicProvider
from app.providers.openai_provider import OpenAIProvider
from app.providers.mock_provider import MockProvider
from app.core.config import settings
from app.core.logging import logger


def get_llm_provider(provider_name: str = None, model_name: str = None) -> BaseLLMProvider:
    """
    Returns an instantiated LLM provider with fallback handling.
    """
    target_provider = (provider_name or settings.DEFAULT_PROVIDER).lower()

    if target_provider == "ollama":
        return OllamaProvider(model_name=model_name or settings.OLLAMA_MODEL)
    elif target_provider == "anthropic":
        return AnthropicProvider(model_name=model_name or settings.ANTHROPIC_MODEL)
    elif target_provider == "openai":
        return OpenAIProvider(model_name=model_name or settings.OPENAI_MODEL)
    else:
        return MockProvider(model_name=model_name or "mock-demo-v1")


async def get_all_providers_status() -> List[Dict[str, Any]]:
    """Checks and returns the live health status of each supported provider."""
    ollama_prov = OllamaProvider()
    anthropic_prov = AnthropicProvider()
    openai_prov = OpenAIProvider()
    mock_prov = MockProvider()

    ollama_avail = await ollama_prov.is_available()
    anthropic_avail = await anthropic_prov.is_available()
    openai_avail = await openai_prov.is_available()

    return [
        {
            "provider_id": "ollama",
            "display_name": "Ollama (Local LLM)",
            "model_name": settings.OLLAMA_MODEL,
            "is_available": ollama_avail,
            "is_local": True,
            "description": "Runs fully offline on your local machine using Ollama.",
            "recommended": True,
        },
        {
            "provider_id": "anthropic",
            "display_name": "Anthropic Claude",
            "model_name": settings.ANTHROPIC_MODEL,
            "is_available": anthropic_avail,
            "is_local": False,
            "description": "High-intelligence reasoning with Claude 3.7 / 3.5 Sonnet.",
            "recommended": False,
        },
        {
            "provider_id": "openai",
            "display_name": "OpenAI GPT-4o",
            "model_name": settings.OPENAI_MODEL,
            "is_available": openai_avail,
            "is_local": False,
            "description": "OpenAI flagship GPT-4o multimodal model.",
            "recommended": False,
        },
        {
            "provider_id": "mock",
            "display_name": "Deterministic Demo Mode",
            "model_name": "lenny-grounded-mock-v1",
            "is_available": True,
            "is_local": True,
            "description": "Instant zero-dependency evaluator demo mode with grounded answers & artifacts.",
            "recommended": False,
        },
    ]
