# ADR-002: Nvidia NIM as Primary LLM Inference Platform

**Status:** Accepted  
**Date:** 2026-07-20  
**Deciders:** Principal AI Engineer

---

## Context

The Financial AI Copilot requires access to a large language model for:
- Natural-language financial analysis
- Report generation
- Conversational Q&A
- Data extraction and summarization

Options evaluated:
1. **OpenAI API** (GPT-4, GPT-4o)
2. **Anthropic API** (Claude 3/3.5)
3. **Self-hosted LLM** (vLLM, Ollama)
4. **Nvidia NIM** — cloud-hosted or self-hosted Nvidia LLM microservice
5. **Groq** / **Together AI** — alternative managed providers

## Decision

We choose **Nvidia NIM** as the primary LLM inference platform.

### Rationale

1. **Enterprise compliance** — NIM supports on-premise deployment for regulated
   financial institutions that cannot send data to third-party APIs
2. **Performance** — Nvidia's optimized inference stack (TensorRT-LLM) offers
   industry-leading throughput and latency
3. **Model flexibility** — Access to Llama 3, Mixtral, Nemotron, and fine-tuned
   financial models through a unified API
4. **OpenAI-compatible API** — Simplifies integration; same SDK/format as OpenAI
5. **Sovereignty** — Can run within the customer's VPC (NIM microservice)

### Fallback Strategy

The `NIMClient` includes a **mock mode** (returns realistic simulated responses)
when `NIM_API_KEY` is not configured. This allows development and testing
without incurring API costs.

## Consequences

### Positive
- ✅ On-premise option for regulated environments
- ✅ High-performance inference
- ✅ Unified API across cloud and self-hosted
- ✅ Mock fallback for development

### Negative
- ❌ Vendor lock-in to Nvidia ecosystem
- ❌ Self-hosted NIM requires Nvidia GPU infrastructure
- ❌ Higher latency vs. purpose-built financial NLP models

## Implementation

```python
class NIMClient:
    """Async client for Nvidia NIM API (integrate.api.nvidia.com)."""

    async def chat_completion(self, messages, ...):
        if not self._api_key:
            return self._mock_response(messages)  # dev mode
        # Real NIM API call
        ...
```

## Alternatives Considered

| Option | Pro | Con |
|--------|-----|-----|
| OpenAI API | Best-in-class models | Data sent to third party; no on-prem |
| Anthropic | Strong safety features | No on-prem option announced |
| Self-hosted vLLM | Open-source, flexible | Requires GPU ops expertise |
| Groq | Very fast inference | Limited model selection |
