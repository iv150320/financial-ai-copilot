"""
Prompt Pipeline — prompt construction, templating, and context injection
for financial analysis use-cases.
"""

from __future__ import annotations

from typing import Any

SYSTEM_PROMPT_TEMPLATE = """You are an expert financial analyst AI assistant.
You help users analyze financial data, generate reports, and answer
questions about markets, companies, and economic indicators.

**Guidelines:**
- Always cite your sources when providing specific data points.
- Clearly distinguish between factual data and analytical opinions.
- Use precise financial terminology and explain jargon when asked.
- Structure complex analyses with clear sections.
- Flag uncertainty clearly: "I estimate", "Based on available data",
  "This is approximate".
- Never provide investment advice. Always include a disclaimer.
- If you lack data to answer a question, say so explicitly.

**Current context:**
- Date: {current_date}
- User context: {user_context}

**Your knowledge cutoff:** {knowledge_cutoff}
"""

USER_PROMPT_TEMPLATE = """Please analyze the following:

{query}

{filters}
"""


class PromptPipeline:
    """Constructs and manages prompts for the AI copilot."""

    def __init__(self, knowledge_cutoff: str = "2025-01-01") -> None:
        self._knowledge_cutoff = knowledge_cutoff

    def build_analysis_prompt(
        self,
        query: str,
        context: dict[str, Any] | None = None,
    ) -> dict[str, str]:
        """
        Build a complete prompt pair (system + user) for an analysis query.

        Parameters
        ----------
        query : str
            The user's natural-language analysis request.
        context : dict or None
            Optional context (company, filters, period, etc.).

        Returns
        -------
        dict[str, str]
            {"system": ..., "user": ...}
        """
        ctx = context or {}

        filters_str = ""
        if ctx:
            filter_items = [f"- **{k}**: {v}" for k, v in ctx.items()]
            filters_str = "**Context / Filters:**\n" + "\n".join(filter_items)

        system = SYSTEM_PROMPT_TEMPLATE.format(
            current_date="2026-07-20",
            user_context=ctx.get("_description", "General financial analysis"),
            knowledge_cutoff=self._knowledge_cutoff,
        )

        user = USER_PROMPT_TEMPLATE.format(query=query, filters=filters_str)

        return {"system": system, "user": user}

    def build_chat_prompt(
        self,
        messages: list[dict[str, str]],
        context: dict[str, Any] | None = None,
    ) -> list[dict[str, str]]:
        """
        Build a full message list for conversational chat.
        Prepends the system prompt and injects context.
        """
        ctx = context or {}
        system = SYSTEM_PROMPT_TEMPLATE.format(
            current_date="2026-07-20",
            user_context=ctx.get("_description", "Conversational financial analysis"),
            knowledge_cutoff=self._knowledge_cutoff,
        )

        result: list[dict[str, str]] = [{"role": "system", "content": system}]
        result.extend(messages)
        return result
