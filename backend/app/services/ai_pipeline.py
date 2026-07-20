"""
AI Pipeline — orchestrates LLM calls through Nvidia NIM with
prompt engineering, context assembly, and response parsing.

Clean Architecture: this is a *service* that depends on the
infrastructure layer (NIMClient) and domain models.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from app.domain.value_objects import AnalysisStatus
from app.infrastructure.nvidia_nim.client import NIMClient
from app.services.prompt_pipeline import PromptPipeline

logger = logging.getLogger(__name__)


class AIPipeline:
    """Orchestrates the end-to-end AI analysis workflow."""

    def __init__(
        self,
        nim_client: NIMClient | None = None,
        prompt_pipeline: PromptPipeline | None = None,
    ) -> None:
        self._nim = nim_client or NIMClient()
        self._prompter = prompt_pipeline or PromptPipeline()

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
        start = time.monotonic()

        # 1. Build the prompt with context
        prompt = self._prompter.build_analysis_prompt(query, context)

        # 2. Call the NIM endpoint
        try:
            raw_response = await self._nim.chat_completion(
                messages=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]},
                ],
                temperature=0.1,
                max_tokens=4096,
            )
        except Exception as exc:
            logger.exception("NIM call failed for query=%s", query[:80])
            raise

        # 3. Parse and validate response
        answer = self._post_process(raw_response)

        elapsed_ms = int((time.monotonic() - start) * 1000)
        metadata = {
            "processing_time_ms": elapsed_ms,
            "model": raw_response.get("model", "unknown"),
            "tokens_used": raw_response.get("usage", {}),
        }

        logger.info(
            "Analysis completed in %d ms. tokens=%s",
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
        return await self._nim.health_check()
