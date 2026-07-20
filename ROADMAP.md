# Roadmap

> **Current release:** `v0.1.0 (ft1)` — Initial scaffold

## ✨ FT1 (Current) — Foundation
- [x] FastAPI backend with Clean Architecture
- [x] Next.js frontend with TypeScript
- [x] Docker Compose (backend + frontend + Postgres + Redis)
- [x] Nvidia NIM integration stub
- [x] Health check and API endpoints
- [x] Pydantic v2 request/response models
- [x] SQLAlchemy async ORM models
- [x] Celery worker configuration
- [x] CI pipeline (GitHub Actions)
- [x] Architecture documentation and ADRs

## 🚀 FT2 — Core Intelligence
- [ ] Nvidia NIM production integration (real API calls)
- [ ] Streaming LLM responses (SSE from NIM to frontend)
- [ ] Financial analysis prompt engineering
- [ ] Market data real API (Yahoo Finance / Polygon.io)
- [ ] RAG pipeline for financial documents (SEC filings, earnings calls)
- [ ] Vector embeddings store (pgvector)

## 💼 FT3 — Enterprise Features
- [ ] User authentication (JWT)
- [ ] Role-based access control (admin, analyst, viewer)
- [ ] Report storage and history
- [ ] Saved analyses and watchlists
- [ ] Export to PDF / Excel
- [ ] Multi-company portfolio analysis

## 🔬 FT4 — Advanced Analytics
- [ ] Financial ratio calculator
- [ ] Chart generation (D3.js / Recharts)
- [ ] Peer comparison analysis
- [ ] Trend detection with time-series analysis
- [ ] Risk scoring engine
- [ ] Anomaly detection in financial data

## 🏢 FT5 — Production Hardening
- [ ] Kubernetes deployment manifests
- [ ] Helm charts
- [ ] Monitoring (Prometheus + Grafana)
- [ ] Structured logging (OpenTelemetry)
- [ ] Rate limiting
- [ ] Audit logging
- [ ] Load testing and performance tuning
- [ ] Security audit
- [ ] Documentation for self-hosted deployment

## 🌐 FT6 — Ecosystem
- [ ] WebSocket-based real-time updates
- [ ] Browser notifications for price alerts
- [ ] Mobile-responsive views
- [ ] API versioning strategy
- [ ] SDK / API client packages (Python, JS)
- [ ] Marketplace integration (data sources)
