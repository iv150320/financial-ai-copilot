"""E2E health checks — validate all docker-compose services are up."""

from __future__ import annotations

import httpx


def test_backend_health():
    """Backend /health returns 200 when running in docker-compose."""
    resp = httpx.get("http://localhost:8000/health", timeout=5.0)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"


def test_frontend_accessible():
    """Frontend is accessible on port 3000."""
    resp = httpx.get("http://localhost:3000", timeout=5.0)
    assert resp.status_code in (200, 301, 302)
