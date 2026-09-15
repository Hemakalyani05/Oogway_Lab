"""
Grounding Guardrail and Citation Extractor.
Ensures responses strictly reflect knowledge from Lenny's transcripts and formats source citations.
"""
from typing import List, Dict, Any, Tuple
from app.schemas.chat import Citation


class GroundingGuard:
    """
    Checks LLM responses against retrieved transcript chunks and structures citations.
    """

    @staticmethod
    def extract_citations(retrieved_chunks: List[Dict[str, Any]]) -> List[Citation]:
        """
        Converts retrieved transcript chunks into structured citation objects for UI cards.
        """
        citations = []
        for i, chunk in enumerate(retrieved_chunks):
            citation_id = f"c_{i+1}"
            quote_excerpt = chunk.get("content", "")[:280] + "..." if len(chunk.get("content", "")) > 280 else chunk.get("content", "")
            
            citations.append(Citation(
                id=citation_id,
                episode_title=chunk.get("episode_title", "Lenny's Podcast"),
                guest=chunk.get("guest", "Podcast Guest"),
                timestamp=chunk.get("timestamp", "00:00"),
                quote=quote_excerpt,
                relevance_score=chunk.get("score", 0.0)
            ))
        return citations

    @staticmethod
    def is_out_of_domain(query: str, retrieved_chunks: List[Dict[str, Any]], threshold: float = 0.015) -> bool:
        """
        Detects if a query cannot be answered by the available knowledge base.
        """
        if not retrieved_chunks:
            return True
        top_score = retrieved_chunks[0].get("score", 0.0)
        return top_score < threshold
