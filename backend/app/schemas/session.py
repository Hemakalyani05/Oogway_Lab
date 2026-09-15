"""
Pydantic schemas for Sessions and Message History.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.chat import ChatMessage, Citation


class SessionCreate(BaseModel):
    title: Optional[str] = Field("New Conversation", description="Initial session title")
    user_id: Optional[str] = Field("default_user", description="User identifier")
    active_model: Optional[str] = Field("mock", description="Default model for this session")


class SessionSummary(BaseModel):
    id: str
    title: str
    user_id: str
    active_model: str
    message_count: int = 0
    created_at: datetime
    updated_at: datetime


class SessionDetail(BaseModel):
    id: str
    title: str
    user_id: str
    active_model: str
    messages: List[ChatMessage] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
