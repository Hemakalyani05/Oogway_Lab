"""
Central API v1 Router.
"""
from fastapi import APIRouter

from app.api.v1.chat import router as chat_router
from app.api.v1.sessions import router as sessions_router
from app.api.v1.artifacts import router as artifacts_router
from app.api.v1.models import router as models_router

api_v1_router = APIRouter()
api_v1_router.include_router(chat_router)
api_v1_router.include_router(sessions_router)
api_v1_router.include_router(artifacts_router)
api_v1_router.include_router(models_router)
