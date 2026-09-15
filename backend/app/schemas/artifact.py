"""
Pydantic schemas for Artifacts and Model Configuration.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field


class ArtifactCreate(BaseModel):
    session_id: str
    title: str
    artifact_type: str = Field(..., description="'markdown', 'html', 'css', 'javascript'")
    language: str = Field("markdown", description="Language tag: markdown, html, javascript, etc.")
    content: str
    metadata_json: Optional[Dict[str, Any]] = None


class ArtifactResponse(BaseModel):
    id: str
    session_id: str
    title: str
    artifact_type: str
    language: str
    content: str
    metadata_json: Optional[Dict[str, Any]] = None
    created_at: datetime


class ModelStatus(BaseModel):
    provider_id: str
    display_name: str
    model_name: str
    is_available: bool
    is_local: bool
    status_message: str
    supports_artifacts: bool = True
    supports_streaming: bool = True
