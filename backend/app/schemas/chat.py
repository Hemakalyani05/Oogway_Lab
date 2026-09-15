"""
Pydantic schemas for chat requests, responses, citations, and stream events.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Citation(BaseModel):
    id: str
    episode_title: str
    guest: str
    timestamp: Optional[str] = None
    quote: str
    relevance_score: Optional[float] = None


class ChatMessage(BaseModel):
    role: str = Field(..., description="'user', 'assistant', or 'system'")
    content: str
    citations: Optional[List[Citation]] = None
    created_at: Optional[str] = None


class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(None, description="Active session ID or null for new session")
    message: str = Field(..., min_length=1, description="User prompt or question")
    provider: Optional[str] = Field(None, description="Override LLM provider: 'ollama', 'anthropic', 'openai', 'mock'")
    model: Optional[str] = Field(None, description="Specific model name")
    generate_ship30: Optional[bool] = Field(False, description="Explicitly request Ship 30 for 30 essay")
    generate_artifact: Optional[bool] = Field(False, description="Explicitly request interactive artifact")


class ChatResponse(BaseModel):
    session_id: str
    message_id: str
    content: str
    role: str = "assistant"
    citations: List[Citation] = Field(default_factory=list)
    artifact_id: Optional[str] = None
    model_used: str
    token_usage: Optional[Dict[str, int]] = None
