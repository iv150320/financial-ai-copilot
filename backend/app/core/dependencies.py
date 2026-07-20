"""
FastAPI dependency injection — reusable ``Depends()`` providers.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings, Settings
from app.core.security import decode_access_token
from app.infrastructure.cache.redis_cache import get_redis_client, RedisClient
from app.infrastructure.db.session import async_session_factory
from app.infrastructure.external_api.market_data import MarketDataClient
from app.infrastructure.nvidia_nim.client import NIMClient

security_scheme = HTTPBearer(auto_error=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide an async database session per request."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_settings_dep() -> Settings:
    """Provide the cached settings instance."""
    return get_settings()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
) -> dict:
    """Decode JWT and return the current user payload (or a stub for now)."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    try:
        payload = decode_access_token(credentials.credentials)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return payload


async def get_redis() -> RedisClient:
    """Provide the Redis client singleton."""
    return await get_redis_client()


async def get_market_data_client() -> MarketDataClient:
    """Provide a MarketDataClient instance."""
    return MarketDataClient()


async def get_nim_client() -> NIMClient:
    """Provide an Nvidia NIM client instance."""
    return NIMClient()


async def get_financial_service() -> "FinancialAnalysisService":
    """Provide a FinancialAnalysisService instance."""
    from app.services.financial_service import FinancialAnalysisService
    return FinancialAnalysisService()
