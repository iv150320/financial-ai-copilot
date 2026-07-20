"""
Pytest configuration — fixtures for unit and integration tests.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.main import app as _app


@pytest.fixture
def app() -> FastAPI:
    """Return the FastAPI application instance."""
    return _app


@pytest.fixture
async def async_client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create an async HTTP test client against the app without a server."""
    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def sample_analysis_query() -> dict[str, Any]:
    """A typical analysis request payload."""
    return {
        "query": "Analyze Apple Inc. revenue trends for Q4 2025",
        "context": {
            "company": "AAPL",
            "period": "Q4 2025",
        },
    }


@pytest.fixture
def sample_market_data_request() -> dict[str, Any]:
    """A typical market data request."""
    return {
        "symbols": ["AAPL", "MSFT", "GOOGL"],
    }
