"""
Enterprise Financial AI Copilot — FastAPI application entry point.

``uvicorn app.main:app --reload``
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.endpoints import chat, financial, health
from app.core.config import get_settings
from app.infrastructure.cache.redis_cache import close_redis_client

logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan — startup / shutdown hooks."""
    logger.info(
        "Starting %s v%s", settings.PROJECT_NAME, settings.VERSION,
    )
    yield
    logger.info("Shutting down — closing connections...")
    await close_redis_client()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered financial analysis copilot for enterprise analysts.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ── CORS ──────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routers ───────────────────────────────────────────────────────────────
app.include_router(health.router, tags=["health"])
app.include_router(financial.router, prefix=settings.API_V1_PREFIX)
app.include_router(chat.router, prefix=settings.API_V1_PREFIX)


# ── Root ──────────────────────────────────────────────────────────────────


@app.get("/")
async def root() -> dict:
    """Minimal root endpoint — redirects to API docs."""
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
    }


# ── Global exception handler ──────────────────────────────────────────────


@app.exception_handler(Exception)
async def global_exception_handler(_request, exc: Exception) -> JSONResponse:
    """Catch unhandled exceptions and return a structured error."""
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred.",
        },
    )
