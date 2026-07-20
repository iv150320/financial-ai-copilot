"""
Celery tasks — asynchronous background jobs for the AI copilot.
"""

from __future__ import annotations

import logging
from typing import Any

from worker.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    name="analyze_financial_query",
    max_retries=3,
    default_retry_delay=30,
)
def analyze_financial_query(
    self,
    query: str,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Background task: run a financial analysis via the AI pipeline.

    This task is dispatched by the API layer when a user submits
    an analysis request.  Results are stored in Celery's result backend
    and can be polled by request_id.
    """
    logger.info("Starting analysis task for query=%s", query[:80])
    # TODO: Instantiate AI pipeline inside task
    # from app.services.ai_pipeline import AIPipeline
    # pipeline = AIPipeline()
    # answer, meta = await pipeline.analyze(query, context)
    return {
        "status": "completed",
        "query": query[:80],
        "answer": "Analysis placeholder — AI pipeline not yet wired into Celery.",
    }


@celery_app.task(name="refresh_market_data")
def refresh_market_data(symbols: list[str] | None = None) -> dict:
    """
    Periodic task: refresh cached market data for watched symbols.
    """
    logger.info("Refreshing market data for %s", symbols or "all watched symbols")
    return {"status": "ok", "symbols_updated": 0}
