"""Tests for the AI Pipeline service with mocked NIM client."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.ai_pipeline import AIPipeline
from app.services.prompt_pipeline import PromptPipeline


@pytest.fixture
def mock_nim_response() -> dict:
    """A typical NIM chat completion response."""
    return {
        "id": "chat-123",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "meta/llama3-70b-instruct",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Apple's Q4 2025 revenue was $95.3B, up 6% YoY.",
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 120, "completion_tokens": 42, "total_tokens": 162},
    }


@pytest.fixture
def mock_nim_client(mock_nim_response: dict) -> AsyncMock:
    """Create a mocked NIMClient."""
    client = AsyncMock()
    client.chat_completion = AsyncMock(return_value=mock_nim_response)
    return client


@pytest.mark.asyncio
async def test_ai_pipeline_analyze(mock_nim_client: AsyncMock) -> None:
    """AIPipeline.analyze() returns a tuple (answer, metadata)."""
    pipeline = AIPipeline(nim_client=mock_nim_client)
    answer, metadata = await pipeline.analyze("Test query")
    assert isinstance(answer, str)
    assert len(answer) > 0
    assert "processing_time_ms" in metadata
    assert "model" in metadata
    assert metadata["model"] == "meta/llama3-70b-instruct"
    # Verify it called the NIM client with the right args
    mock_nim_client.chat_completion.assert_awaited_once()


@pytest.mark.asyncio
async def test_ai_pipeline_with_context(mock_nim_client: AsyncMock) -> None:
    """AIPipeline works with additional context."""
    pipeline = AIPipeline(nim_client=mock_nim_client)
    context = {"company": "TEST", "year": "2025"}
    answer, metadata = await pipeline.analyze("Analyze revenue", context)
    assert isinstance(answer, str)
    assert "processing_time_ms" in metadata


@pytest.mark.asyncio
async def test_ai_pipeline_handles_error(mock_nim_client: AsyncMock) -> None:
    """AIPipeline raises on NIM error."""
    mock_nim_client.chat_completion = AsyncMock(side_effect=Exception("NIM down"))
    pipeline = AIPipeline(nim_client=mock_nim_client)
    with pytest.raises(Exception, match="NIM down"):
        await pipeline.analyze("Test")


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
