"""
Financial Service — domain-specific financial business logic that
coordinates market data, report generation, and the AI pipeline.
"""

from __future__ import annotations

import logging
from decimal import Decimal
from typing import Any

from app.domain.entities import AnalysisRequest, MarketSnapshot
from app.domain.value_objects import (
    AnalysisStatus,
    Currency,
    DateRange,
    FinancialRatio,
    Money,
    ReportType,
)
from app.infrastructure.external_api.market_data import MarketDataClient
from app.infrastructure.nvidia_nim.client import NIMClient
from app.services.ai_pipeline import AIPipeline

logger = logging.getLogger(__name__)


class FinancialAnalysisService:
    """Core business service for financial analysis operations."""

    def __init__(
        self,
        ai_pipeline: AIPipeline | None = None,
        market_client: MarketDataClient | None = None,
    ) -> None:
        self._ai = ai_pipeline or AIPipeline()
        self._market = market_client or MarketDataClient()

    async def analyze(self, query: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Run a full AI-powered financial analysis."""
        answer, metadata = await self._ai.analyze(query, context)
        return {"answer": answer, **metadata}

    async def get_market_data(
        self,
        symbols: list[str],
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[MarketSnapshot]:
        """Fetch current market data for one or more symbols."""
        raw = await self._market.fetch_quotes(symbols)
        snapshots: list[MarketSnapshot] = []
        for item in raw:
            snapshots.append(
                MarketSnapshot(
                    symbol=item.get("symbol", ""),
                    price=Decimal(str(item.get("price", 0))),
                    change=Decimal(str(item.get("change", 0))),
                    change_percent=Decimal(str(item.get("change_percent", 0))),
                    volume=item.get("volume", 0),
                    source=item.get("source", "api"),
                )
            )
        return snapshots

    async def generate_report(
        self,
        company_id: str,
        report_type: str,
        period: DateRange | None = None,
        instructions: str = "",
    ) -> dict[str, Any]:
        """Generate a structured financial report via AI."""
        query = (
            f"Generate a {report_type} report for company {company_id}"
            f"{f' from {period.start} to {period.end}' if period else ''}."
            f" {instructions}".strip()
        )
        context = {
            "company_id": company_id,
            "report_type": report_type,
            "_description": f"Report generation for {company_id}",
        }
        answer, metadata = await self._ai.analyze(query, context)
        return {"content": answer, "report_type": report_type, **metadata}

    async def chat(
        self,
        messages: list[dict[str, str]],
        context: dict[str, Any] | None = None,
        stream: bool = False,
    ) -> dict[str, Any]:
        """Send a chat message to the AI copilot."""
        # For streaming, this would be an async generator;
        # here we provide the non-streaming fallback.
        reply, metadata = await self._ai.chat(messages, context)
        return {
            "reply": reply,
            "usage": metadata.get("tokens_used", {}),
        }}
