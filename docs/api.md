# API Reference

Base URL: `/api/v1` (proxied through frontend) or `http://localhost:8000/api/v1`

---

## Health Check

### `GET /health`

Returns service health status.

**Response 200:**
```json
{
  "status": "ok",
  "version": "0.1.0",
  "timestamp": "2026-07-20T11:27:00Z"
}
```

---

## Financial Analysis

### `POST /api/v1/financial/analyze`

Submit a natural-language analysis query.

**Request:**
```json
{
  "query": "Analyze Apple Inc. revenue trends for Q4 2025",
  "context": {
    "company": "AAPL",
    "period": "Q4 2025"
  }
}
```

**Response 202:**
```json
{
  "request_id": "uuid-here",
  "status": "queued",
  "message": "Analysis queued successfully."
}
```

### `GET /api/v1/financial/analyze/{request_id}`

Retrieve the result of an analysis (not yet implemented).

---

## Market Data

### `POST /api/v1/financial/market-data`

Fetch market data for one or more symbols.

**Request:**
```json
{
  "symbols": ["AAPL", "MSFT", "GOOGL"],
  "start_date": "2026-01-01",
  "end_date": "2026-07-20",
  "interval": "1d"
}
```

**Response 200:**
```json
{
  "quotes": [
    {
      "symbol": "AAPL",
      "price": 198.42,
      "change": 2.15,
      "change_percent": 1.09,
      "volume": 52345678,
      "timestamp": "2026-07-20T11:27:00Z"
    }
  ],
  "total": 3
}
```

---

## Reports

### `POST /api/v1/financial/reports`

Generate a financial report via the AI copilot.

**Request:**
```json
{
  "company_id": "AAPL",
  "report_type": "income_statement",
  "period_start": "2025-10-01",
  "period_end": "2025-12-31",
  "additional_instructions": "Focus on revenue from Services segment"
}
```

**Response 202:**
```json
{
  "report_id": "uuid-here",
  "title": "Income Statement — AAPL",
  "report_type": "income_statement",
  "content": "# Income Statement Analysis...",
  "generated_at": "2026-07-20T11:27:00Z",
  "warnings": []
}
```

---

## Chat

### `POST /api/v1/chat`

Conversational AI copilot (non-streaming).

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "What is Apple's current P/E ratio?"}
  ],
  "stream": false,
  "temperature": 0.3
}
```

**Response 200:**
```json
{
  "reply": "Based on the latest financial data...",
  "sources": ["Yahoo Finance", "SEC Filing 10-K"],
  "token_usage": {
    "prompt_tokens": 350,
    "completion_tokens": 110,
    "total_tokens": 460
  }
}
```

### `POST /api/v1/chat/stream`

Streaming chat via Server-Sent Events (SSE).

Same request body as above. Response is a stream of SSE messages:

```
data: {"choices": [{"delta": {"content": "Based"}}]}

data: {"choices": [{"delta": {"content": " on"}}]}

data: {"choices": [{"delta": {"content": " the"}}]}

data: [DONE]
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Human-readable error description"
}
```

| Status | Meaning |
|--------|---------|
| 400 | Bad Request — invalid input |
| 401 | Unauthorized — authentication required |
| 404 | Not Found — resource doesn't exist |
| 422 | Unprocessable Entity — validation error |
| 500 | Internal Server Error |
| 501 | Not Implemented |
