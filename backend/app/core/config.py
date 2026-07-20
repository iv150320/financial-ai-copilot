"""
Global configuration for the Financial AI Copilot.

Settings are loaded from environment variables with sensible defaults
for local development. All secrets must be provided via .env or the
runtime environment.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Project ──────────────────────────────────────────────────────────
    PROJECT_NAME: str = "Enterprise Financial AI Copilot"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # ── Server ───────────────────────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    # ── Database ─────────────────────────────────────────────────────────
    DATABASE_URL: str = (
        "postgresql+asyncpg://copilot:copilot@localhost:5432/copilot"
    )
    DATABASE_ECHO: bool = False

    # ── Redis / Celery ───────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # ── Auth / Security ──────────────────────────────────────────────────
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # ── NVIDIA NIM ───────────────────────────────────────────────────────
    NIM_API_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
    NIM_API_KEY: str = ""
    NIM_MODEL: str = "meta/llama3-70b-instruct"
    NIM_MAX_TOKENS: int = 4096
    NIM_TEMPERATURE: float = 0.1

    # ── External APIs ────────────────────────────────────────────────────
    MARKET_DATA_API_URL: str = "https://api.example.com/v1"
    MARKET_DATA_API_KEY: str = ""

    # ── Paths ────────────────────────────────────────────────────────────
    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent.parent


@lru_cache
def get_settings() -> Settings:
    """Return a cached singleton settings instance."""
    return Settings()
