"""
Main Growth Agent Orchestrator.
Coordinates retrieval, grounding guardrails, skills, and LLM streaming.
"""
from typing import AsyncGenerator, List, Dict, Any, Optional
import json

from app.rag.hybrid_retriever import hybrid_retriever
from app.skills.ship30 import SHIP30_SYSTEM_PROMPT, build_ship30_prompt
from app.skills.artifact_builder import ArtifactBuilder
from app.skills.grounding_guard import GroundingGuard
from app.agents.prompts import format_grounded_system_prompt
from app.providers import get_llm_provider
from app.schemas.chat import Citation
from app.core.logging import logger


class GrowthAgent:
    """
    The Lenny Growth Agent orchestrator.
    """
    def __init__(self, provider_name: str = None, model_name: str = None):
        self.provider = get_llm_provider(provider_name, model_name)

    async def run_stream(
        self,
        user_message: str,
        history: List[Dict[str, str]] = None,
        generate_ship30: bool = False,
        generate_artifact: bool = False,
        top_k: int = 5
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Executes the agentic loop and yields structured SSE dictionary events:
        - {"type": "status", "message": "..."}
        - {"type": "citations", "citations": [...]}
        - {"type": "token", "token": "..."}
        - {"type": "artifact", "artifact": {...}}
        - {"type": "done", "full_content": "..."}
        """
        history = history or []

        # 1. Status: Searching Knowledge Base
        yield {
            "type": "status",
            "message": "Searching Lenny's Podcast transcripts with Hybrid RAG..."
        }

        # 2. Hybrid Retrieval
        search_query = user_message
        retrieved_chunks = hybrid_retriever.search(search_query, top_k=top_k)
        
        # 3. Extract Citations
        citations = GroundingGuard.extract_citations(retrieved_chunks)
        yield {
            "type": "citations",
            "citations": [c.model_dump() for c in citations]
        }

        # 4. Formulate System Prompt & Target Messages
        if generate_ship30:
            yield {"type": "status", "message": "Drafting Ship 30 for 30 Atomic Essay..."}
            system_prompt = SHIP30_SYSTEM_PROMPT
            user_prompt = build_ship30_prompt(user_message, retrieved_chunks)
            messages = [{"role": "user", "content": user_prompt}]
        else:
            system_prompt = format_grounded_system_prompt(retrieved_chunks)
            messages = history + [{"role": "user", "content": user_message}]

        # 5. Stream LLM tokens
        full_tokens = []
        try:
            async for chunk in self.provider.stream_chat(messages, system_prompt):
                if chunk.error:
                    logger.warning(f"Provider error: {chunk.error}. Falling back to deterministic demo mock.")
                    # Yield warning event
                    yield {
                        "type": "status",
                        "message": f"Provider notice: {chunk.error}. Switching to local demo engine."
                    }
                if chunk.token:
                    full_tokens.append(chunk.token)
                    yield {
                        "type": "token",
                        "token": chunk.token
                    }
        except Exception as e:
            logger.error(f"Streaming error in GrowthAgent: {e}")
            fallback_msg = "\n\n*(Note: LLM stream experienced an interruption; returning retrieved transcript summary)*"
            yield {"type": "token", "token": fallback_msg}
            full_tokens.append(fallback_msg)

        full_content = "".join(full_tokens)

        # 6. Extract Artifact if generated
        artifact_data = ArtifactBuilder.extract_artifact(full_content)
        if artifact_data and artifact_data.get("is_valid"):
            yield {
                "type": "artifact",
                "artifact": artifact_data
            }

        # 7. Final completion event
        clean_content = ArtifactBuilder.strip_artifact_tags(full_content) if artifact_data else full_content
        yield {
            "type": "done",
            "full_content": clean_content,
            "raw_content": full_content,
            "citations": [c.model_dump() for c in citations],
            "artifact": artifact_data,
            "model_used": self.provider.model_name
        }
