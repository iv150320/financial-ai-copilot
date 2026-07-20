"""
Nvidia NIM API Client — async HTTP client for LLM inference via
Nvidia's NIM microservice endpoints.

Integrates with ``integrate.api.nvidia.com`` or a self-hosted NIM.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


class NIMClient:
    """Async client for the Nvidia NIM API."""

    def __init__(self) -> None:
        self._base_url = settings.NIM_API_BASE_URL
        self._api_key = settings.NIM_API_KEY
        self._model = settings.NIM_MODEL
        self._default_max_tokens = settings.NIM_MAX_TOKENS
        self._default_temperature = settings.NIM_TEMPERATURE
        self._timeout = 60.0

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        stream: bool = False,
    ) -> dict[str, Any]:
        """
        Send a chat completion request to the NIM endpoint.

        Parameters
        ----------
        messages : list[dict]
            Chat messages in OpenAI format::
                [{"role": "system", "content": "..."},
                 {"role": "user", "content": "..."}]
        model : str, optional
            Override the default model.
        temperature : float, optional
            Sampling temperature (0.0-2.0).
        max_tokens : int, optional
            Maximum output tokens.
        stream : bool
            Enable streaming (not yet implemented).

        Returns
        -------
        dict
            The full NIM API response.
        """
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        payload: dict[str, Any] = {
            "model": model or self._model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self._default_temperature,
            "max_tokens": max_tokens or self._default_max_tokens,
            "stream": stream,
        }

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            logger.debug(
                "NIM request: model=%s, messages=%d tokens",
                payload["model"],
                sum(len(m.get("content", "")) for m in messages),
            )

            # ── Stub / Mock path ────────────────────────────────────────
            # Remove this when NIM_API_KEY is set and the endpoint is live.
            if not self._api_key:
                logger.warning("NIM_API_KEY not set — using mock response.")
                return self._mock_response(messages)

            try:
                response = await client.post(
                    f"{self._base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as exc:
                logger.error(
                    "NIM HTTP error: %s %s", exc.response.status_code, exc.response.text
                )
                raise
            except httpx.RequestError as exc:
                logger.error("NIM request failed: %s", exc)
                raise

    async def embeddings(
        self,
        texts: list[str],
        model: str = "nvidia/nv-embed-qa-4",
    ) -> list[list[float]]:
        """Generate embeddings via the NIM embeddings endpoint (stub)."""
        logger.warning("Embeddings endpoint not configured — using mock.")
        return [[0.0] * 768 for _ in texts]

    async def health_check(self) -> dict:
        """Simple health check — verify NIM connectivity."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f"{self._base_url}/models")
                if resp.is_success:
                    return {"status": "ok", "models": resp.json()}
                return {"status": "degraded", "detail": resp.text}
        except Exception as exc:
            return {"status": "unreachable", "detail": str(exc)}

    def _mock_response(self, messages: list[dict[str, str]]) -> dict[str, Any]:
        """Return a plausible mock response for development."""
        user_msg = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            "",
        )
        return {
            "id": "mock-response",
            "object": "chat.completion",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": (
                            "Based on the available financial data, I can provide "
                            "the following analysis:\n\n"
                            f"Your query: *{user_msg[:100]}*\n\n"
                            "This is a simulated response from the Financial AI Copilot.\n\n"
                            "**Key Findings:**\n"
                            "- Revenue growth trend is positive\n"
                            "- Operating margins are within industry benchmarks\n"
                            "- Liquidity ratios indicate strong short-term financial health\n\n"
                            "*Disclaimer: This is AI-generated analysis for informational "
                            "purposes only and does not constitute financial advice.*"
                        ),
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 350,
                "completion_tokens": 110,
                "total_tokens": 460,
            },
            "model": self._model,
        }
