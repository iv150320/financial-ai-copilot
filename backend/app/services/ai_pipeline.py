"""
AI Pipeline — orchestrates LLM calls through Nvidia NIM with
prompt engineering, context assembly, and response parsing.

Clean Architecture: this is a *service* that depends on the
infrastructure layer (NIMClient) and domain models.
"""

from __future__ import annotations

import logging
import time
from datetime import date
from typing import Any

from app.core.config import get_settings
from app.domain.value_objects import AnalysisStatus
from app.infrastructure.nvidia_nim.client import NIMClient
from app.services.prompt_pipeline import PromptPipeline

logger = logging.getLogger(__name__)


class AIPipelineError(RuntimeError):
    """Base exception for AIPipeline errors."""


class AIPipeline:
    """Orchestrates the end-to-end AI analysis workflow."""

    def __init__(
        self,
        nim_client: NIMClient | None = None,
        prompt_pipeline: PromptPipeline | None = None,
    ) -> None:
        settings = get_settings()
        self._nim = nim_client or NIMClient()
        self._prompter = prompt_pipeline or PromptPipeline()
        # Default generation parameters from settings
        self._default_temperature = settings.NIM_TEMPERATURE
        self._default_max_tokens = settings.NIM_MAX_TOKENS

    async def analyze(
        self,
        query: str,
        context: dict[str, Any] | None = None,
    ) -> tuple[str, dict[str, Any]]:
        """
        Execute a full analysis cycle.

        Returns
        -------
        tuple[str, dict]
            (answer_text, metadata)
        """
        # Basic input validation to prevent overly large prompts
        if not query or not query.strip():
            raise ValueError("Query must not be empty")
        if len(query) > 10_000:  # Arbitrary safe limit
            raise ValueError("Query is too long (max 10,000 characters)")
        if context:
            # Limit the size of the context dict (by converting to string and checking length)
            context_str = str(context)
            if len(context_str) > 50_000:  # Arbitrary safe limit
                raise ValueError("Context is too large (max 50,000 characters when stringified)")

        start = time.monotonic()

        # 1. Build the prompt with context
        prompt = self._prompter.build_analysis_prompt(
            query,
            context,
            current_date=date.today().isoformat(),
        )

        # 2. Call the NIM endpoint
        try:
            raw_response = await self._nim.chat_completion(
                messages=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]},
                ],
                temperature=self._default_temperature,
                max_tokens=self._default_max_tokens,
            )
        except Exception as exc:
            logger.exception("NIM call failed for query=%s", query[:80])
            raise AIPipelineError(f"Failed to get response from NIM: {exc}") from exc

        # 3. Parse and validate response
        answer = self._post_process(raw_response)

        elapsed_ms = int((time.monotonic() - start) * 1000)
        metadata = {
            "processing_time_ms": elapsed_ms,
            "model": raw_response.get("model", "unknown"),
            "tokens_used": raw_response.get("usage", {}),
            "status": AnalysisStatus.COMPLETED.value,
        }

        logger.info(
            "Analysis completed in %d ms. tokens=%s",
            elapsed_ms,
            metadata["tokens_used"],
        )
        return answer, metadata

    async def chat(
        self,
        messages: list[dict[str, str]],
        context: dict[str, Any] | None = None,
    ) -> tuple[str, dict[str, Any]]:
        """
        Handle a chat conversation.

        Returns
        -------
        tuple[str, dict]
            (reply_text, metadata)
        """
        if not messages:
            raise ValueError("Messages list must not be empty")
        # Basic validation: ensure each message has role and content
        for i, msg in enumerate(messages):
            if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
                raise ValueError(f"Message at index {i} is invalid: must be a dict with 'role' and 'content'")

        start = time.monotonic()

        # Build the prompt using the chat pipeline
        prompt_messages = self._prompter.build_chat_prompt(
            messages,
            context,
            current_date=date.today().isoformat(),
        )

        try:
            raw_response = await self._nim.chat_completion(
                messages=prompt_messages,
                temperature=self._default_temperature,
                max_tokens=self._default_max_tokens,
            )
        except Exception as exc:
            logger.exception("NIM chat call failed for messages=%s", messages)
            raise AIPipelineError(f"Failed to get response from NIM: {exc}") from exc

        answer = self._post_process(raw_response)

        elapsed_ms = int((time.monotonic() - start) * 1000)
        metadata = {
            "processing_time_ms": elapsed_ms,
            "model": raw_response.get("model", "unknown"),
            "tokens_used": raw_response.get("usage", {}),
            "status": AnalysisStatus.COMPLETED.value,
        }

        logger.info(
            "Chat completed in %d ms. tokens=%s",
            elapsed_ms,
            metadata["tokens_used"],
        )
        return answer, metadata

    def _post_process(self, raw: dict) -> str:
        """Extract and clean the assistant's reply from the NIM response."""
        try:
            content = raw["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            logger.warning("Unexpected NIM response shape: %s", raw)
            return "I encountered an error while processing your request."
        return content.strip()

    async def health_check(self) -> dict:
        """Verify the AI pipeline is operational."""
        # First, check the NIM client
        nim_health = await self._nim.health_check()
        if nim_health.get("status") != "ok":
            return {
                "status": "degraded",
                "component": "nim_client",
                "detail": nim_health.get("detail", "NIM client unhealthy"),
            }

        # Then, try to build a simple prompt to verify the prompt pipeline
        try:
            self._prompter.build_analysis_prompt("test", {}, current_date="2024-01-01")
        except Exception as exc:
            return {
                "status": "degraded",
                "component": "prompt_pipeline",
                "detail": f"Failed to build prompt: {exc}",
            }

        return {"status": "ok"}