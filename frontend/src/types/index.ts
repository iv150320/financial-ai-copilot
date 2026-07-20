/**
 * Shared TypeScript types for the Financial AI Copilot.
 */

/* ─── Domain Types ──────────────────────────────────────────────────── */

export interface MarketQuote {
  symbol: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  timestamp: string;
}

export interface FinancialReport {
  id: string;
  title: string;
  reportType: string;
  companyId: string;
  content: string;
  generatedAt: string;
  warnings?: string[];
}

export interface AnalysisResult {
  requestId: string;
  query: string;
  answer: string;
  sources: string[];
  confidence: number;
  processingTimeMs: number;
}

/* ─── Chat Types ────────────────────────────────────────────────────── */

export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: Date;
  metadata?: Record<string, unknown>;
}

export interface ChatRequestPayload {
  messages: Array<{ role: string; content: string }>;
  stream?: boolean;
  temperature?: number;
}

export interface ChatResponsePayload {
  reply: string;
  sources: string[];
  tokenUsage: Record<string, number>;
}

/* ─── UI State Types ────────────────────────────────────────────────── */

export type ThemeMode = "light" | "dark" | "system";

export interface CopilotState {
  isConnected: boolean;
  isProcessing: boolean;
  messages: ChatMessage[];
  error: string | null;
}
