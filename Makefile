.PHONY: install format lint test test-watch cov mypy precommit run dev docker-build docker-run

# Goldilocks Development Makefile
# Optimized for SSD performance with Docker BuildKit caching

.PHONY: help build build-dev build-prod clean test lint format install setup docker-clean docker-prune

# Default target
.DEFAULT_GOAL := help

# Docker BuildKit environment
export DOCKER_BUILDKIT=1
export BUILDKIT_PROGRESS=plain
export BUILDX_BAKE_ENTITLEMENTS_FS=0

## Core Development Commands

help: ## Show this help message
	@echo "🏗️  Goldilocks Development Commands (Optimized for SSD)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "💡 All builds use optimized SSD caching for near-instant subsequent builds!"

## Setup and Installation Commands

setup: ## Set up optimized development environment with SSD caching
	@echo "🚀 Setting up optimized development environment..."
	./infrastructure/docker/setup-cache.sh

install: setup ## Alias for setup command

## Build Commands (Optimized)

build: build-dev ## Build development environment (default)

build-dev: ## Build optimized development environment with full caching
	@echo "🏗️  Building development environment with SSD optimization..."
	./infrastructure/docker/build.sh dev

build-prod: ## Build optimized production environment
	@echo "🏗️  Building production environment with SSD optimization..."
	./infrastructure/docker/build.sh prod

build-all: ## Build all targets with maximum cache optimization
	@echo "🌟 Building all targets with maximum SSD cache optimization..."
	./infrastructure/docker/build.sh all

build-devcontainer: ## Build devcontainer with optimized caching
	@echo "🏠 Building devcontainer with SSD optimization..."
	./infrastructure/docker/build.sh devcontainer

## Docker Compose Commands

up: ## Start development environment
	docker-compose --profile dev up

up-prod: ## Start production environment
	docker-compose --profile prod up

down: ## Stop all containers
	docker-compose down

logs: ## Show container logs
	docker-compose logs -f

## Development Commands

test: ## Run tests in optimized container
	docker-compose --profile dev run --rm goldilocks-dev pytest -q

test-cov: ## Run tests with coverage in optimized container
	docker-compose --profile dev run --rm goldilocks-dev pytest -q --cov=goldilocks --cov-report=term-missing

lint: ## Run linting in optimized container
	docker-compose --profile dev run --rm goldilocks-dev ruff check src/
	docker-compose --profile dev run --rm goldilocks-dev mypy src/

format: ## Format code in optimized container
	docker-compose --profile dev run --rm goldilocks-dev black src/
	docker-compose --profile dev run --rm goldilocks-dev isort src/

shell: ## Get shell in development container
	docker-compose --profile dev run --rm goldilocks-dev /bin/bash

## Maintenance Commands

clean: ## Clean up Docker resources (keep optimized caches)
	docker system prune -f --volumes
	@echo "✅ Cleaned Docker resources while preserving SSD caches"

docker-clean: ## Remove all goldilocks containers and images
	docker-compose down --remove-orphans
	docker images | grep goldilocks | awk '{print $$3}' | xargs -r docker rmi -f
	@echo "✅ Cleaned Goldilocks Docker resources"

docker-prune: ## DANGEROUS: Remove all caches and start fresh
	@echo "⚠️  This will remove ALL optimized caches!"
	@read -p "Are you sure? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		sudo rm -rf /tmp/.buildx-cache-* /tmp/goldilocks-*; \
		docker system prune -a -f --volumes; \
		echo "💥 All caches removed. Run 'make setup' to recreate."; \
	else \
		echo "❌ Cancelled."; \
	fi

cache-stats: ## Show cache statistics
	@echo "📊 SSD Cache Statistics:"
	@du -sh /tmp/.buildx-cache-* /tmp/goldilocks-* 2>/dev/null || echo "No caches found - run 'make setup' first"
	@echo ""
	@echo "📈 Docker Images:"
	@docker images | grep goldilocks || echo "No goldilocks images found"

## Quick Commands

dev: up ## Quick alias to start development environment

stop: down ## Quick alias to stop all containers

rebuild: docker-clean build ## Clean rebuild of development environment

fresh: docker-prune setup build ## Complete fresh start (removes all caches)

## Performance Testing

benchmark: ## Test build performance (requires existing cache)
	@echo "⏱️  Testing optimized build performance..."
	@time ./infrastructure/docker/build.sh devcontainer
	@echo ""
	@echo "💡 Subsequent builds should be significantly faster thanks to SSD caching!"

## Status and Info

status: ## Show environment status
	@echo "🔍 Goldilocks Development Environment Status"
	@echo "=========================================="
	@echo ""
	@echo "📦 Docker Images:"
	@docker images | grep goldilocks || echo "No goldilocks images found"
	@echo ""
	@echo "🏃 Running Containers:"
	@docker ps | grep goldilocks || echo "No goldilocks containers running"
	@echo ""
	@echo "💾 Cache Statistics:"
	@du -sh /tmp/.buildx-cache-* /tmp/goldilocks-* 2>/dev/null || echo "No caches found"
	@echo ""
	@echo "⚙️  BuildKit Status:"
	@docker buildx ls | grep goldilocks-builder || echo "Goldilocks builder not found"

## Documentation

docs: ## Generate and serve documentation
	@echo "📚 Documentation commands would go here"

.PHONY: help setup install build build-dev build-prod build-all build-devcontainer up up-prod down logs test test-cov lint format shell clean docker-clean docker-prune cache-stats dev stop rebuild fresh benchmark status docs
