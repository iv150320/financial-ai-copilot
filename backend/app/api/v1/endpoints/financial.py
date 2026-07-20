"""
Financial analysis endpoints — market data queries and report generation.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.pydantic_models import (
    AnalysisRequest,
    AnalysisResponse,
    AnalysisResult,
    MarketDataRequest,
    MarketDataResponse,
    MarketQuote,
    ReportRequest,
    ReportResponse,
)
from app.services.financial_service import FinancialAnalysisService

from app.core.dependencies import get_financial_service

router = APIRouter(prefix="/financial", tags=["financial"])


@router.post("/analyze", response_model=AnalysisResponse, status_code=status.HTTP_202_ACCEPTED)
async def analyze(
    request: AnalysisRequest,
    service: Annotated[FinancialAnalysisService, Depends(get_financial_service)],
) -> AnalysisResponse:
    """
    Submit a natural-language analysis query.

    The request is queued for async processing. Poll the returned
    ``request_id`` to retrieve the result.
    """
    # TODO: Persist to DB and dispatch to Celery worker
    result = await service.analyze(request.query, request.context)
    return AnalysisResponse(
        request_id="pending-implementation",
        status="queued",
        message="Analysis request received. Async processing is not yet wired.",
    )


@router.get("/analyze/{request_id}", response_model=AnalysisResult)
async def get_analysis_result(
    request_id: str,
    service: Annotated[FinancialAnalysisService, Depends(get_financial_service)],
) -> AnalysisResult:
    """Retrieve the result of a previously submitted analysis (stub)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Async result retrieval not yet implemented.",
    )


@router.post("/market-data", response_model=MarketDataResponse)
async def get_market_data(
    request: MarketDataRequest,
    service: Annotated[FinancialAnalysisService, Depends(get_financial_service)],
) -> MarketDataResponse:
    """
    Fetch live market data for the requested symbols.

    Returns quotes from the configured market data provider (or mock data
    when no provider API key is set).
    """
    snapshots = await service.get_market_data(
        symbols=request.symbols,
        start_date=str(request.start_date) if request.start_date else None,
        end_date=str(request.end_date) if request.end_date else None,
    )
    quotes = [
        MarketQuote(
            symbol=s.symbol,
            price=s.price,
            change=s.change,
            change_percent=s.change_percent,
            volume=s.volume,
            timestamp=s.timestamp,
        )
        for s in snapshots
    ]
    return MarketDataResponse(quotes=quotes, total=len(quotes))


@router.post("/reports", response_model=ReportResponse, status_code=status.HTTP_202_ACCEPTED)
async def generate_report(
    request: ReportRequest,
    service: Annotated[FinancialAnalysisService, Depends(get_financial_service)],
) -> ReportResponse:
    """
    Generate a financial report via the AI copilot.
    """
    result = await service.generate_report(
        company_id=request.company_id,
        report_type=request.report_type,
        instructions=request.additional_instructions,
    )
    return ReportResponse(
        report_id="pending-implementation",
        title=f"{request.report_type.replace('_', ' ').title()} — {request.company_id}",
        report_type=request.report_type,
        content=result.get("content", ""),
    )
