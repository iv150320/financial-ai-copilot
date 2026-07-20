"""Tests for the chat copilot endpoint."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_chat_non_streaming(async_client: AsyncClient) -> None:
    """POST /api/v1/chat returns a reply."""
    response = await async_client.post(
        "/api/v1/chat",
        json={
            "messages": [
                {"role": "user", "content": "What is Apple's current P/E ratio?"},
            ],
            "stream": False,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert len(data["reply"]) > 0


@pytest.mark.asyncio
async def test_chat_streaming_rejected(async_client: AsyncClient) -> None:
    """Streaming via POST /api/v1/chat should return 400."""
    response = await async_client.post(
        "/api/v1/chat",
        json={
            "messages": [{"role": "user", "content": "Hi"}],
            "stream": True,
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_chat_empty_messages(async_client: AsyncClient) -> None:
    """Empty messages should return 422."""
    response = await async_client.post(
        "/api/v1/chat",
        json={"messages": []},
    )
    assert response.status_code == 422
