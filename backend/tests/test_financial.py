"""Tests for financial analysis endpoints with mocked NIM client."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient


@pytest.fixture(autouse=True)
def mock_nim_client():
    """Patch NIMClient to prevent real HTTP calls."""
    patcher = patch(
        "app.infrastructure.nvidia_nim.client.NIMClient.chat_completion",
        new_callable=AsyncMock,
    )
    mock = patcher.start()
    mock.return_value = {
        "id": "chat-test",
        "object": "chat.completion",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Analysis result: AAPL revenue $95.3B.",
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 50, "completion_tokens": 15, "total_tokens": 65},
    }
    yield mock
    patcher.stop()


@pytest.fixture(autouse=True)
def mock_market_client():
    """Mock MarketDataClient.fetch_quotes to return dicts."""
    patcher = patch(
        "app.infrastructure.external_api.market_data.MarketDataClient.fetch_quotes",
        new_callable=AsyncMock,
    )
    mock = patcher.start()
    mock.return_value = [
        {
            "symbol": "AAPL",
            "price": "175.50",
            "change": "2.30",
            "change_percent": "1.33",
            "volume": 45000000,
            "source": "api",
            "timestamp": "2025-01-15T10:30:00Z",
        }
    ]
    yield mock
    patcher.stop()


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
