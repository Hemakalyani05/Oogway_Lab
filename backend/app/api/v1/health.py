"""
Health check and observability readiness endpoints.
"""
from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy import text

from app.api.deps import get_db
from app.db.session import db_execute
from app.rag.hybrid_retriever import hybrid_retriever
from app.providers import get_all_providers_status

router = APIRouter(tags=["Health"])


@router.get("/healthz", status_code=status.HTTP_200_OK)
async def health_check():
    """Liveness probe."""
    return {
        "status": "healthy",
        "service": "lenny-growth-assistant",
        "version": "1.0.0"
    }


@router.get("/readyz", status_code=status.HTTP_200_OK)
async def readiness_check(db: Any = Depends(get_db)):
    """Readiness probe checking database and knowledge base indexing."""
    db_ok = False
    try:
        await db_execute(db, text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    kb_chunks_indexed = len(hybrid_retriever.documents)
    providers = await get_all_providers_status()

    return {
        "status": "ready" if (db_ok and kb_chunks_indexed > 0) else "degraded",
        "checks": {
            "database": "connected" if db_ok else "unreachable",
            "knowledge_base_chunks": kb_chunks_indexed,
            "providers_available": [p["provider_id"] for p in providers if p["is_available"]]
        }
    }
