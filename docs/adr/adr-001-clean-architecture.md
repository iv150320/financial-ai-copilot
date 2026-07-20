# ADR-001: Clean Architecture with Domain-Driven Design

**Status:** Accepted  
**Date:** 2026-07-20  
**Deciders:** Principal AI Engineer

---

## Context

The Financial AI Copilot must be maintainable, testable, and adaptable to changing
business requirements. It integrates multiple concerns (AI/LLM, market data,
financial analysis, user management) that should be loosely coupled.

Several architectural patterns were considered:
- Traditional MVC (flat, framework-coupled)
- Hexagonal Architecture
- Clean Architecture (Robert C. Martin)

## Decision

We adopt **Clean Architecture** with **Domain-Driven Design** principles:

```
┌─────────────┐
│  API Layer  │  ← FastAPI routers, serialization
├─────────────┤
│  Services   │  ← Business logic orchestration
├─────────────┤
│  Domain     │  ← Entities, value objects, invariants
├─────────────┤
│ Infra       │  ← DB, cache, external APIs
└─────────────┘
```

### Key Rules
1. **Dependency inversion** — Domain layer has zero imports from frameworks
   (FastAPI, SQLAlchemy, etc.)
2. **Outer layers depend on inner layers** — Services depend on domain;
   infrastructure depends on abstractions in the domain layer
3. **No framework in domain** — Entities are plain dataclasses, not ORM models
4. **Boundaries are explicit** — Each layer has its own `__init__.py` and
   clearly defined public API

## Consequences

### Positive
- ✅ Testability — Domain logic tested without framework overhead
- ✅ Maintainability — Changes in one layer don't cascade
- ✅ Replaceability — Swap PostgreSQL for another DB by changing infra only
- ✅ Clarity — New developers understand the system structure quickly

### Negative
- ❌ More boilerplate — Additional layers mean more files and indirection
- ❌ Learning curve — Team must understand Clean Architecture patterns

## Alternatives Considered

| Pattern | Reason for Rejection |
|---------|---------------------|
| Classic MVC | Business logic leaks into controllers and models |
| Flat structure | Becomes unmaintainable at scale |
| Micro-frontends | Premature for initial release |
