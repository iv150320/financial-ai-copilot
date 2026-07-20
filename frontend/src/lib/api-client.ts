/**
 * API client for the Financial AI Copilot backend.
 *
 * Handles authentication, request/response serialization, and error handling.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api";

interface RequestOptions {
  method?: string;
  headers?: Record<string, string>;
  body?: unknown;
  signal?: AbortSignal;
}

class ApiError extends Error {
  status: number;
  details: unknown;

  constructor(status: number, message: string, details?: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.details = details;
  }
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = "GET", headers = {}, body, signal } = options;

  const config: RequestInit = {
    method,
    headers: {
      "Content-Type": "application/json",
      ...headers,
    },
    signal,
  };

  if (body !== undefined) {
    config.body = JSON.stringify(body);
  }

  const response = await fetch(`${API_BASE}${path}`, config);

  if (!response.ok) {
    let detail = `HTTP ${response.status}`;
    try {
      const errBody = await response.json();
      detail = errBody.detail || errBody.message || detail;
    } catch {
      // ignore parse errors
    }
    throw new ApiError(response.status, detail);
  }

  return response.json() as Promise<T>;
}

/* ─── Public API Methods ─────────────────────────────────────────────── */

export interface HealthResponse {
  status: string;
  version: string;
  timestamp: string;
}

export interface AnalysisRequest {
  query: string;
  context?: Record<string, unknown>;
}

export interface AnalysisResponse {
  request_id: string;
  status: string;
  message: string;
}

export interface MarketQuote {
  symbol: string;
  price: number;
  change: number;
  change_percent: number;
  volume: number;
  timestamp: string;
}

export interface MarketDataResponse {
  quotes: MarketQuote[];
  total: number;
}

export interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
}

export interface ChatResponse {
  reply: string;
  sources: string[];
  token_usage: Record<string, number>;
}

export const api = {
  health: () => request<HealthResponse>("/health"),

  analyze: (data: AnalysisRequest) =>
    request<AnalysisResponse>("/v1/financial/analyze", {
      method: "POST",
      body: data,
    }),

  marketData: (symbols: string[]) =>
    request<MarketDataResponse>("/v1/financial/market-data", {
      method: "POST",
      body: { symbols },
    }),

  chat: (messages: ChatMessage[], temperature = 0.3) =>
    request<ChatResponse>("/v1/chat", {
      method: "POST",
      body: { messages, stream: false, temperature },
    }),
};
