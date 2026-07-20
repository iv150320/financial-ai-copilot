.PHONY: help install dev test lint clean build docker-up docker-down

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install backend and frontend dependencies
	cd backend && pip install -r requirements.txt
	cd frontend && npm ci

dev: ## Start development servers
	@echo "Starting backend and frontend in dev mode..."
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
	cd frontend && npm run dev &
	wait

test: ## Run all tests
	cd backend && pytest tests/ -v --cov=app
	cd frontend && npm run type-check

e2e: ## Run end-to-end integration tests
	docker compose -f docker/docker-compose.yml up -d
	@sleep 5
	python -m pytest tests/e2e/ -v || true
	docker compose -f docker/docker-compose.yml down

lint: ## Run linters
	cd backend && ruff check . && mypy app --ignore-missing-imports
	cd frontend && npm run lint

format: ## Format code
	cd backend && ruff format .
	cd frontend && npm run format

clean: ## Clean build artifacts
	rm -rf backend/.pytest_cache backend/__pycache__
	rm -rf backend/app/__pycache__ backend/app/**/__pycache__
	rm -rf frontend/.next frontend/node_modules frontend/out
	rm -rf .pytest_cache __pycache__

docker-up: ## Start all services with Docker Compose
	docker compose -f docker/docker-compose.yml up -d --build

docker-down: ## Stop all Docker services
	docker compose -f docker/docker-compose.yml down -v

docker-logs: ## Tail logs from all services
	docker compose -f docker/docker-compose.yml logs -f

migrate: ## Run database migrations
	cd backend && alembic upgrade head

migration: ## Create a new migration
	cd backend && alembic revision --autogenerate -m "$(name)"

worker: ## Start the Celery worker
	cd backend && celery -A worker.celery_app worker --loglevel=info
