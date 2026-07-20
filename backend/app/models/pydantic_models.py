"""
Pydantic v2 models — request / response schemas for the API layer.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field


# ── Health ────────────────────────────────────────────────────────────────


class HealthResponse(BaseModel):
    """GET /health response."""

    status: str = "ok"
    version: str = "0.1.0"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ── Analysis ──────────────────────────────────────────────────────────────


class AnalysisRequest(BaseModel):
    """Request body for the AI analysis endpoint."""

    query: str = Field(
        ...,
        min_length=1,
        max_length=10_000,
        description="Natural-language query for financial analysis.",
    )
    context: dict[str, Any] | None = Field(
        None,
        description="Optional context (company, period, filters, etc.).",
    )


class AnalysisResponse(BaseModel):
    """Response returned after submitting an analysis request."""

    request_id: str
    status: str
    message: str = "Analysis queued successfully."


class AnalysisResult(BaseModel):
    """Full result once the analysis is complete."""

    request_id: str
    query: str
    answer: str
    sources: list[str] = []
    confidence: float = Field(ge=0.0, le=1.0)
    processing_time_ms: int = 0
    completed_at: datetime = Field(default_factory=datetime.utcnow)


# ── Financial Data ────────────────────────────────────────────────────────


class MarketDataRequest(BaseModel):
    """Request parameters for market data retrieval."""

    symbols: list[str] = Field(..., min_length=1, max_length=50)
    start_date: date | None = None
    end_date: date | None = None
    interval: str = "1d"  # 1m, 5m, 15m, 1h, 1d, 1wk, 1mo


class MarketQuote(BaseModel):
    """A single price quote for a symbol."""

    symbol: str
    price: Decimal
    change: Decimal = Decimal("0")
    change_percent: Decimal = Decimal("0")
    volume: int = 0
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MarketDataResponse(BaseModel):
    """List of market quotes."""

    quotes: list[MarketQuote]
    total: int = 0


# ── Financial Reports ─────────────────────────────────────────────────────


class ReportRequest(BaseModel):
    """Request to generate a financial report."""

    company_id: str = Field(..., min_length=1, max_length=20)
    report_type: str = "custom_analysis"
    period_start: date | None = None
    period_end: date | None = None
    additional_instructions: str = ""


class ReportResponse(BaseModel):
    """Response containing the generated report."""

    report_id: str
    title: str
    report_type: str
    content: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    warnings: list[str] = []


# ── Chat ──────────────────────────────────────────────────────────────────


class ChatMessage(BaseModel):
    """A single message in the copilot chat."""

    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1)
    metadata: dict[str, Any] = {}


class ChatRequest(BaseModel):
    """Request body for the streaming chat endpoint."""

    messages: list[ChatMessage] = Field(..., min_length=1, max_length=100)
    stream: bool = True
    temperature: float | None = Field(None, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    """Non-streaming response from the copilot chat."""

    reply: str
    sources: list[str] = []
    token_usage: dict[str, int] = {}
