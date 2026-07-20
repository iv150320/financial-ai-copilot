"""Tests for financial analysis endpoints."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_market_data_endpoint(
    async_client: AsyncClient,
    sample_market_data_request: dict,
) -> None:
    """POST /api/v1/financial/market-data returns quotes."""
    response = await async_client.post(
        "/api/v1/financial/market-data",
        json=sample_market_data_request,
    )
    assert response.status_code == 200
    data = response.json()
    assert "quotes" in data
    assert data["total"] > 0


@pytest.mark.asyncio
async def test_market_data_invalid_symbols(async_client: AsyncClient) -> None:
    """Empty symbols list should return 422."""
    response = await async_client.post(
        "/api/v1/financial/market-data",
        json={"symbols": []},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_analysis_endpoint(
    async_client: AsyncClient,
    sample_analysis_query: dict,
) -> None:
    """POST /api/v1/financial/analyze returns 202."""
    response = await async_client.post(
        "/api/v1/financial/analyze",
        json=sample_analysis_query,
    )
    assert response.status_code == 202
    data = response.json()
    assert "request_id" in data
    assert "status" in data


@pytest.mark.asyncio
async def test_analysis_empty_query(async_client: AsyncClient) -> None:
    """Empty query should return 422."""
    response = await async_client.post(
        "/api/v1/financial/analyze",
        json={"query": ""},
    )
    assert response.status_code == 422
