"""
Redis cache client — async wrapper around redis-py for the application.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import redis.asyncio as aioredis

from app.core.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

RedisClient = aioredis.Redis  # type alias for type hints

_client: RedisClient | None = None


async def get_redis_client() -> RedisClient:
    """Return a singleton async Redis client."""
    global _client
    if _client is None:
        _client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=3,
            socket_timeout=5,
        )
        logger.info("Redis client initialized: %s", settings.REDIS_URL)
    return _client


async def close_redis_client() -> None:
    """Gracefully close the Redis connection."""
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None
        logger.info("Redis client closed.")


async def cache_get(key: str) -> Any | None:
    """Get a JSON-deserialised value from cache."""
    client = await get_redis_client()
    raw = await client.get(key)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return raw


async def cache_set(
    key: str,
    value: Any,
    ttl_seconds: int = 300,
) -> None:
    """Store a value in cache as JSON with an optional TTL."""
    client = await get_redis_client()
    serialized = json.dumps(value, default=str)
    await client.setex(key, ttl_seconds, serialized)


async def cache_delete(pattern: str) -> int:
    """Delete keys matching *pattern*. Returns number of deleted keys."""
    client = await get_redis_client()
    cursor = 0
    deleted = 0
    while True:
        cursor, keys = await client.scan(cursor=cursor, match=pattern, count=100)
        if keys:
            deleted += await client.delete(*keys)
        if cursor == 0:
            break
    return deleted
