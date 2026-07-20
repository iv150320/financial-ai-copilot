# Architecture

## Overview

The **Enterprise Financial AI Copilot** follows **Clean Architecture** principles
with a clear separation of concerns across layers:

```
┌─────────────────────────────────────────────────────────┐
│                     Presentation Layer                    │
│  ┌─────────────────┐  ┌──────────────────────────────┐  │
│  │   Next.js SPA   │  │      FastAPI (REST/SSE)      │  │
│  │  (React/TS)     │◄─┤  ┌────────────────────────┐  │  │
│  │                 │  │  │  API Endpoints          │  │  │
│  └─────────────────┘  │  │  /health, /api/v1/*     │  │  │
│         │             │  └────────────────────────┘  │  │
│         │ HTTP/JSON   └──────────────────────────────┘  │
│         ▼                                                │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Application / Service Layer         │   │
│  │  ┌─────────────┐ ┌──────────────┐ ┌──────────┐  │   │
│  │  │ AI Pipeline │ │PromptPipeline│ │Financial │  │   │
│  │  │ (NIM)       │ │(Templates)   │ │Service   │  │   │
│  │  └──────┬──────┘ └──────────────┘ └──────────┘  │   │
│  └─────────┼────────────────────────────────────────┘   │
│            │                                            │
│  ┌─────────▼────────────────────────────────────────┐   │
│  │              Domain Layer                        │   │
│  │  ┌────────────┐ ┌──────────────┐ ┌────────────┐  │   │
│  │  │  Entities  │ │Value Objects │ │   Events   │  │   │
│  │  └────────────┘ └──────────────┘ └────────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
│            │                                            │
│  ┌─────────▼────────────────────────────────────────┐   │
│  │           Infrastructure Layer                    │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐  │   │
│  │  │PostgreSQL│ │  Redis   │ │ Nvidia NIM /     │  │   │
│  │  │(asyncpg) │ │ (cache)  │ │ External APIs    │  │   │
│  │  └──────────┘ └──────────┘ └──────────────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### Presentation Layer
- **Next.js SPA** — Server-rendered React app with client-side interactivity
- **FastAPI** — RESTful API with OpenAPI docs, SSE for streaming chat

### Application / Service Layer
- **AI Pipeline** — Orchestrates LLM calls, manages context, post-processes results
- **Prompt Pipeline** — Template-driven prompt construction for financial analysis
- **Financial Service** — Domain-specific business logic coordinating AI + market data

### Domain Layer
- **Entities** — `FinancialReport`, `AnalysisRequest`, `MarketSnapshot`
- **Value Objects** — `Currency`, `Money`, `DateRange`, `FinancialRatio`
- **Events** — `AnalysisRequested`, `AnalysisCompleted`, `MarketDataRefreshed`

### Infrastructure Layer
- **PostgreSQL** — Primary datastore (SQLAlchemy 2.0 async)
- **Redis** — Cache layer + Celery message broker
- **Nvidia NIM** — LLM inference via Nvidia API (self-hosted or cloud)
- **External APIs** — Market data providers (stub for development)

## Data Flow

```
User ──► Next.js ──HTTP──► FastAPI ──► FinancialService
                                          ├──► AIPipeline ──► NIMClient ──► Nvidia NIM
                                          └──► MarketDataClient ──► External API
                                               │
                                               ▼
                                           Redis (cache)
                                               │
                                               ▼
                                         PostgreSQL (persistence)
```

## Key Design Decisions

1. **Clean Architecture** — Domain has zero dependencies on frameworks
2. **Async from day one** — async/await throughout Python and TypeScript
3. **Mock-by-default** — External APIs return mock data when keys aren't set
4. **Containerized** — Everything runs in Docker for reproducible development
5. **Event-driven** — Domain events for loose coupling between services
