"""
Model configuration and provider status API endpoints.
"""
from typing import List
from fastapi import APIRouter
from app.providers import get_all_providers_status
from app.schemas.model import ModelInfo

router = APIRouter(prefix="/models", tags=["Models"])


@router.get("", response_model=List[ModelInfo])
async def list_models():
    """Returns available LLM providers, model names, and real-time connectivity status."""
    statuses = await get_all_providers_status()
    return [ModelInfo(**s) for s in statuses]
