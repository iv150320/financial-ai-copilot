<div align="center">

# Enterprise Financial AI Copilot

**AI-powered financial analysis assistant for enterprise analysts**

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-000000?logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.5-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)](.github/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 📋 Overview

The **Enterprise Financial AI Copilot** is an intelligent assistant that helps
financial analysts perform complex analysis through natural conversation.
Powered by Nvidia NIM LLMs and built with Clean Architecture, it combines
AI reasoning with real-time market data to deliver actionable insights.

### Key Capabilities

- **Natural Language Analysis** — Ask questions about financial data in plain English
- **Market Intelligence** — Real-time quotes, trends, and market data
- **Report Generation** — Auto-generated balance sheets, income statements, cash flow
- **Ratio Analysis** — P/E, ROE, debt-to-equity, and custom financial ratios
- **Conversational Interface** — Context-aware chat with streaming responses
- **Enterprise Ready** — On-premise deployment option, audit logging, RBAC (coming)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                          │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Chat Interface │ Market Dashboard │ Report Viewer │ Settings │  │
│  └──────────────────────────┬────────────────────────────────────┘  │
│                              │ HTTP/SSE                              │
├──────────────────────────────┼──────────────────────────────────────┤
│                     Backend (FastAPI)                               │
│  ┌───────────────────────────┴────────────────────────────────────┐ │
│  │                    Application Services                        │ │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐   │ │
│  │  │ AI Pipeline  │ │   Prompt     │ │ Financial Service   │   │ │
│  │  │ (NIM)        │ │  Pipeline    │ │ (Domain Logic)      │   │ │
│  │  └──────┬───────┘ └──────────────┘ └──────────────────────┘   │ │
│  └─────────┼─────────────────────────────────────────────────────┘ │
│            │                                                        │
│  ┌─────────▼─────────────────────────────────────────────────────┐ │
│  │                    Infrastructure                             │ │
│  │  ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌─────────────┐ │ │
│  │  │PostgreSQL│  │  Redis   │  │ Nvidia    │  │ Market Data │ │ │
│  │  │ (Async)  │  │ (Cache)  │  │ NIM       │  │ APIs        │ │ │
│  │  └──────────┘  └──────────┘  └───────────┘  └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

**Read more:** [Architecture Documentation](docs/architecture.md) |
[ADRs](docs/adr/) | [API Reference](docs/api.md)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI Chat** | Conversational financial analysis via Nvidia NIM |
| 📊 **Market Data** | Real-time stock quotes and market trends |
| 📑 **Report Generation** | Auto-generated financial reports and statements |
| 🔍 **Ratio Analysis** | P/E, ROE, debt-to-equity, and custom ratios |
| 💬 **Streaming Responses** | Real-time token-by-token streaming |
| 🐳 **Dockerized** | One-command setup with Docker Compose |
| 🔒 **Enterprise Security** | JWT auth, RBAC (coming), audit logging (coming) |
| 📦 **Clean Architecture** | Maintainable, testable, framework-independent |

---

## 🚀 Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.12+](https://www.python.org/) (for local development)
- [Node.js 20+](https://nodejs.org/) (for local development)

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/financial-ai-copilot.git
cd financial-ai-copilot

# Start all services
make docker-up

# Check logs
make docker-logs
```

The services will be available at:

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

### Local Development

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (in another terminal)
cd frontend
npm ci
npm run dev
```

---

## 📖 API Examples

### Health Check

```bash
curl http://localhost:8000/health
```

### Market Data

```bash
curl -X POST http://localhost:8000/api/v1/financial/market-data \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["AAPL", "MSFT", "GOOGL"]}'
```

### Financial Analysis

```bash
curl -X POST http://localhost:8000/api/v1/financial/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Compare Apple and Microsoft revenue growth"}'
```

### Chat with AI Copilot

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "What is Apple'\''s P/E ratio?"}],
    "stream": false
  }'
```

**Full API reference:** [docs/api.md](docs/api.md)

---

## 📸 Screenshots

> *Screenshots coming soon!*

<!-- TODO: Add screenshots -->
<!-- ![Chat Interface](docs/screenshots/chat.png) -->
<!-- ![Market Dashboard](docs/screenshots/market-data.png) -->
<!-- ![Report Viewer](docs/screenshots/report.png) -->

---

## 🗺️ Roadmap

| Release | Focus |
|---------|-------|
| **FT1** ✅ | Foundation — Clean Architecture, Docker, CI/CD, NIM stub |
| **FT2** | Core Intelligence — Real NIM integration, streaming, RAG |
| **FT3** | Enterprise — Auth, RBAC, report storage, export |
| **FT4** | Advanced Analytics — Charts, ratios, trend detection |
| **FT5** | Production — K8s, monitoring, audit, security |
| **FT6** | Ecosystem — WebSocket, SDK, marketplace |

**Detailed roadmap:** [ROADMAP.md](ROADMAP.md)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 14, React 18, TypeScript, Tailwind CSS |
| **Backend** | Python 3.12, FastAPI, Pydantic v2 |
| **AI/ML** | Nvidia NIM (Llama 3, Nemotron) |
| **Database** | PostgreSQL 16, SQLAlchemy 2.0 (async) |
| **Cache** | Redis 7 |
| **Queue** | Celery |
| **Infrastructure** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |

---

## 🤝 Contributing

We welcome contributions! Please see our
[contributing guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
make install     # Install all dependencies
make dev         # Start dev servers
make test        # Run all tests
make lint        # Run linters
make format      # Format code
make clean       # Clean build artifacts
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ❤️ for financial analysts everywhere</sub>
</div>
