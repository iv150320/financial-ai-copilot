"""Tests for the health check endpoint."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient) -> None:
    """GET /health returns 200 with status 'ok'."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_health_check_has_version(async_client: AsyncClient) -> None:
    """Health response includes a non-empty version string."""
    response = await async_client.get("/health")
    data = response.json()
    assert len(data["version"]) > 0


@pytest.mark.asyncio
async def test_root_endpoint(async_client: AsyncClient) -> None:
    """GET / returns service info."""
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data
    assert "docs" in data
