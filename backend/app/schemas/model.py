"""
Pydantic schemas for Model Providers and health checks.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ModelInfo(BaseModel):
    provider_id: str
    display_name: str
    model_name: str
    is_available: bool
    is_local: bool
    description: str
    recommended: bool = False


class SetActiveModelRequest(BaseModel):
    provider: str
    model: Optional[str] = None
