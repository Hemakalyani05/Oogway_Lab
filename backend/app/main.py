"""
FastAPI application entrypoint for The Lenny Growth Assistant.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from app.core.config import settings
from app.core.logging import logger
from app.db.init_db import init_database
from app.rag.ingest import load_and_index_transcripts
from app.api.v1.router import api_v1_router
from app.api.v1.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup and shutdown routines."""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}...")
    
    # 1. Initialize DB Schema
    await init_database()
    
    # 2. Ingest Transcripts Knowledge Base
    chunk_count = load_and_index_transcripts()
    logger.info(f"Knowledge Base initialized with {chunk_count} transcript chunks.")

    yield

    logger.info(f"Shutting down {settings.PROJECT_NAME}...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-grade AI Growth & Product Assistant grounded in Lenny's Podcast transcripts.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing and structured logging middleware
@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(f"{request.method} {request.url.path} returned {response.status_code} in {process_time:.2f}ms")
        response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
        return response
    except Exception as exc:
        process_time = (time.time() - start_time) * 1000
        logger.error(f"{request.method} {request.url.path} failed after {process_time:.2f}ms: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error", "error": str(exc)}
        )


# Include API Routers
app.include_router(health_router)
app.include_router(api_v1_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
