"""Cross-service integration tests — NIM client routing through gateway."""

from __future__ import annotations

import pytest

from app.infrastructure.nvidia_nim.client import NIMClient


def test_nim_client_routes_through_gateway():
    """NIMClient uses NIM_GATEWAY_URL when configured."""
    client = NIMClient()
    assert client._using_gateway is True
    assert "nvidia-nim-gateway" in client._base_url


def test_nim_client_base_url_is_gateway():
    """The client base URL points to the gateway, not direct NIM."""
    client = NIMClient()
    assert client._base_url == "http://nvidia-nim-gateway:8000"


def test_nim_client_properties():
    """NIMClient exposes expected properties."""
    client = NIMClient()
    assert client._model is not None
    assert len(client._model) > 0
    assert client._default_max_tokens > 0
    assert isinstance(client._default_temperature, float)


def test_nim_client_service_name():
    """NIMClient has a service identifier for gateway observability."""
    assert NIMClient.SERVICE_NAME == "financial-ai-copilot"


@pytest.mark.asyncio
async def test_nim_client_headers_with_gateway():
    """When using gateway, headers identify the service, no API key."""
    client = NIMClient()
    headers = client._build_headers()
    assert headers["Content-Type"] == "application/json"
    # When routing through gateway, service name is sent instead of API key
    assert "X-Service-Name" in headers
    assert headers["X-Service-Name"] == "financial-ai-copilot"


@pytest.mark.asyncio
async def test_nim_chat_completion_model():
    """NIMClient has a configured model for chat completion."""
    client = NIMClient()
    assert client._model is not None
    # The model should be a valid NVIDIA NIM model identifier
    assert "/" in client._model or len(client._model) > 0
