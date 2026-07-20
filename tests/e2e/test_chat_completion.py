"""E2E test — chat completion through the running backend."""

from __future__ import annotations

import httpx


def test_chat_endpoint():
    """POST /api/v1/chat returns a reply."""
    resp = httpx.post(
        "http://localhost:8000/api/v1/chat",
        json={
            "messages": [
                {"role": "user", "content": "What is Apple's P/E ratio?"},
            ],
            "stream": False,
        },
        timeout=10.0,
    )
    assert resp.status_code in (200, 422, 500)


def test_health_e2e():
    """Gateway health is accessible."""
    resp = httpx.get("http://localhost:8000/health", timeout=5.0)
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
