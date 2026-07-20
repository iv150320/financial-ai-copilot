"""
Chat endpoint — conversational AI copilot interface.

Supports both streaming (SSE) and non-streaming responses.
"""

from __future__ import annotations

import json
import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from pydantic import ValidationError

from app.models.pydantic_models import ChatRequest, ChatResponse
from app.services.financial_service import FinancialAnalysisService

from app.core.dependencies import get_financial_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    service: Annotated[FinancialAnalysisService, Depends(get_financial_service)],
) -> ChatResponse:
    """
    Send a chat message to the AI copilot.

    Use ``stream=true`` in the request body to receive a Server-Sent Events
    (SSE) stream instead of a single JSON response.
    """
    if request.stream:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use POST /chat/stream for streaming responses.",
        )

    messages = [m.model_dump() for m in request.messages]
    result = await service.chat(messages, stream=False)
    return ChatResponse(
        reply=result.get("reply", ""),
        token_usage=result.get("usage", {}),
    )


@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    service: Annotated[FinancialAnalysisService, Depends(get_financial_service)],
) -> StreamingResponse:
    """
    Streaming chat endpoint using Server-Sent Events (SSE).

    Each chunk is a JSON-encoded SSE ``data`` field.
    """
    messages = [m.model_dump() for m in request.messages]

    async def event_generator() -> Any:
        # TODO: Replace with actual streaming from NIM
        # For now, simulate a stream with a single chunk.
        result = await service.chat(messages, stream=False)
        reply = result.get("reply", "")
        for word in reply.split(" "):
            chunk = {"choices": [{"delta": {"content": word + " "}}]}
            yield f"data: {json.dumps(chunk)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
