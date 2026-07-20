"""Tests for the AI Pipeline service."""

from __future__ import annotations

import pytest

from app.services.ai_pipeline import AIPipeline
from app.services.prompt_pipeline import PromptPipeline


@pytest.mark.asyncio
async def test_ai_pipeline_analyze() -> None:
    """AIPipeline.analyze() returns a tuple (answer, metadata)."""
    pipeline = AIPipeline()
    answer, metadata = await pipeline.analyze("Test query")
    assert isinstance(answer, str)
    assert len(answer) > 0
    assert "processing_time_ms" in metadata


@pytest.mark.asyncio
async def test_ai_pipeline_with_context() -> None:
    """AIPipeline works with additional context."""
    pipeline = AIPipeline()
    context = {"company": "TEST", "year": "2025"}
    answer, metadata = await pipeline.analyze("Analyze revenue", context)
    assert isinstance(answer, str)
    assert "processing_time_ms" in metadata


def test_prompt_pipeline_build() -> None:
    """PromptPipeline builds a valid prompt pair."""
    pp = PromptPipeline()
    result = pp.build_analysis_prompt(
        "What is the EPS of MSFT?",
        {"company": "MSFT"},
    )
    assert "system" in result
    assert "user" in result
    assert "MSFT" in result["user"]


def test_prompt_pipeline_no_context() -> None:
    """PromptPipeline works without context."""
    pp = PromptPipeline()
    result = pp.build_analysis_prompt("Show me balance sheet data")
    assert "system" in result
    assert "user" in result
    assert "balance sheet" in result["user"].lower()
