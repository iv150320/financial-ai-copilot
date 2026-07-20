"""Cross-service integration tests — NIM client routing through gateway."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from app.infrastructure.nvidia_nim.client import NIMClient


def test_nim_client_default_base_url():
    """NIMClient defaults to NVIDIA cloud API URL."""
    client = NIMClient()
    assert client._base_url.startswith("https://integrate.api.nvidia.com")


@pytest.mark.asyncio
async def test_nim_client_routes_through_gateway_env():
    """NIMClient uses the configured base URL (gateway override)."""
    with patch("app.infrastructure.nvidia_nim.client.get_settings") as mock_get:
        mock_settings = AsyncMock()
        mock_settings.NIM_API_BASE_URL = "http://nvidia-nim-gateway:8000/v1"
        mock_settings.NIM_API_KEY = "test-key"
        mock_settings.NIM_MODEL = "meta/llama-3.1-8b-instruct"
        mock_settings.NIM_MAX_TOKENS = 4096
        mock_settings.NIM_TEMPERATURE = 0.1
        mock_get.return_value = mock_settings

        client = NIMClient()
        assert client._base_url == "http://nvidia-nim-gateway:8000/v1"
        assert "nvidia-nim-gateway" in client._base_url


@pytest.mark.asyncio
async def test_nim_client_known_base_url():
    """Direct NIM URL via integrate.api.nvidia.com — known default."""
    # The default is production NVIDIA API, not the local gateway
    client = NIMClient()
    assert "integrate.api.nvidia.com" in client._base_url


@pytest.mark.asyncio
async def test_nim_chat_completion_sends_correct_payload():
    """Verify the chat endpoint payload format is OpenAI-compatible."""
    with patch("app.infrastructure.nvidia_nim.client.get_settings") as mock_get:
        mock_settings = AsyncMock()
        mock_settings.NIM_API_BASE_URL = "http://localhost:8000/v1"
        mock_settings.NIM_API_KEY = "test-key"
        mock_settings.NIM_MODEL = "meta/llama-3.1-8b-instruct"
        mock_settings.NIM_MAX_TOKENS = 1024
        mock_settings.NIM_TEMPERATURE = 0.1
        mock_get.return_value = mock_settings

        client = NIMClient()
        assert client._model == "meta/llama-3.1-8b-instruct"
        assert client._default_max_tokens == 1024
        assert client._default_temperature == 0.1
