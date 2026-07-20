"""
Market Data Client — abstraction over external financial data APIs.

Currently a stub that returns simulated data. In production, replace
with a real provider (Yahoo Finance, Alpha Vantage, Polygon.io, etc.).
"""

from __future__ import annotations

import logging
import random
from decimal import Decimal
from typing import Any

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


class MarketDataClient:
    """Async client for external market data APIs."""

    def __init__(self) -> None:
        self._base_url = settings.MARKET_DATA_API_URL
        self._api_key = settings.MARKET_DATA_API_KEY
        self._http_timeout = 10.0

    async def fetch_quotes(self, symbols: list[str]) -> list[dict[str, Any]]:
        """
        Fetch real-time quotes for the given symbols.

        Currently returns simulated data. When connected to a real
        provider, this method will call the external HTTP API.
        """
        # ── TODO: Replace with real API call ──────────────────────────────
        logger.info(
            "MarketDataClient.fetch_quotes(symbols=%s) — using mock data",
            symbols,
        )
        results: list[dict[str, Any]] = []
        for symbol in symbols:
            base = random.uniform(50, 500)
            change_pct = random.uniform(-5.0, 5.0)
            change = base * change_pct / 100
            results.append({
                "symbol": symbol.upper(),
                "price": round(base + change, 2),
                "change": round(change, 2),
                "change_percent": round(change_pct, 2),
                "volume": random.randint(100_000, 10_000_000),
                "source": "mock",
            })
        return results

    async def fetch_historical(
        self,
        symbol: str,
        interval: str = "1d",
        range_days: int = 30,
    ) -> list[dict[str, Any]]:
        """Fetch historical price data (stub)."""
        logger.info("fetch_historical(%s, interval=%s) — stub", symbol, interval)
        return []

    async def health_check(self) -> dict:
        """Check if the external market data API is reachable."""
        # In production, make a lightweight HEAD /ping or similar call.
        return {"status": "ok", "provider": "mock"}
