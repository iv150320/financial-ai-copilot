# Changelog

All notable changes to the **Enterprise Financial AI Copilot** will be
documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] — 2026-07-20

### Added
- **Backend API** — FastAPI scaffold with Clean Architecture layers
  - Health check endpoint (`GET /health`)
  - Financial analysis endpoint (`POST /api/v1/financial/analyze`)
  - Market data endpoint (`POST /api/v1/financial/market-data`)
  - Report generation endpoint (`POST /api/v1/financial/reports`)
  - Chat copilot endpoint (`POST /api/v1/chat`) with SSE streaming
- **AI Pipeline** — Nvidia NIM integration stub with mock fallback
- **Prompt Pipeline** — Template-driven prompt construction for financial analysis
- **Domain Layer** — Entities, value objects, domain events
- **Infrastructure** — Async PostgreSQL (SQLAlchemy 2.0), Redis cache, Celery worker
- **Frontend** — Next.js 14 with TypeScript, Tailwind CSS, shadcn/ui-inspired design
  - Chat interface with real-time messaging
  - API client library with full type safety
- **Docker** — Containerized deployment (backend + frontend + worker + Postgres + Redis)
- **CI** — GitHub Actions workflow (lint, test, build)
- **Documentation** — Architecture docs, ADRs, API docs, sequence diagrams
