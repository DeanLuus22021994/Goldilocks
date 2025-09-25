# Docker Infrastructure

> Containerized development and deployment infrastructure for Goldilocks.

## Quick Start

### Development Environment

```bash
# Start development environment
make dev
# or
cd infrastructure/docker && ./scripts/compose.sh development up

# Stop environment
make stop
# or
cd infrastructure/docker && ./scripts/compose.sh development down
```

### Production Deployment

```bash
# Build and deploy production
make build-prod
cd infrastructure/docker && ./scripts/compose.sh production up -d
```

## Architecture

### Service Stack

- **Backend**: Python Flask application with hot reload
- **Database**: MariaDB 11.4 with edge computing optimizations
- **Admin**: Adminer web interface for database management
- **Frontend**: Node.js Alpine for tooling and asset management

### Network Architecture

```
goldilocks-network (172.20.0.0/16)
├── Backend (Flask app on port 9000)
├── Database (MariaDB on port 3306)
├── Adminer (Web admin on port 8080)
└── Frontend (Node.js tooling)
```

### Volume Management

- **Persistent Data**: Database, logs, uploads
- **Development Cache**: Pip, npm, mypy, pytest caches
- **Build Cache**: Docker layer caching for fast rebuilds

## Configuration

### Environment Files

**`.env`** - Docker infrastructure settings:

```bash
PYTHON_VERSION=3.12-slim
BACKEND_PORT=9000
MARIADB_ROOT_PASSWORD=secure-password
```

**`shared/environment.env`** - Application runtime settings:

```bash
FLASK_DEBUG=1
DATABASE_URL=mysql+pymysql://...
LOG_LEVEL=DEBUG
```

### Deployment Profiles

```bash
# Available profiles
docker compose --profile dev up        # Development
docker compose --profile prod up       # Production
docker compose --profile database up   # Database only
docker compose --profile admin up      # Admin tools
```

## Management Commands

### Using Make

```bash
make dev         # Start development environment
make build-dev   # Build development images
make build-prod  # Build production images
make test        # Run tests in containers
make clean       # Clean up resources
```

### Using Management Script

```bash
cd infrastructure/docker

# Environment management
./scripts/compose.sh development up
./scripts/compose.sh production deploy
./scripts/compose.sh testing run

# Utility operations
./scripts/compose.sh health          # Check service health
./scripts/compose.sh logs -f         # View logs
./scripts/compose.sh clean          # Clean resources
```

## Development Workflow

### 1. Initial Setup

```bash
git clone <repository>
cd Goldilocks
make setup
```

### 2. Daily Development

```bash
make dev                    # Start development stack
# Code changes auto-reload
make test                   # Run tests
make shell                  # Get development shell
```

### 3. Testing Changes

```bash
./infrastructure/docker/scripts/test-infrastructure.sh
```

## Performance Features

### Build Optimization

- **Multi-stage builds** for minimal image sizes
- **BuildKit cache mounts** for persistent package caches
- **Layer caching** for near-instant rebuilds
- **Parallel builds** with docker-bake configuration

### Development Speed

- **Hot reload** for Flask applications
- **Volume caches** for pip, npm, and development tools
- **Persistent containers** to avoid restart overhead
- **Optimized health checks** for faster startup

### Resource Efficiency

- **Memory limits** appropriate for development/production
- **CPU constraints** to prevent resource exhaustion
- **Tmpfs volumes** for ephemeral data
- **Compressed logs** with rotation

## Troubleshooting

### Common Issues

**Services won't start:**

```bash
# Check logs
./scripts/compose.sh logs backend

# Validate configuration
docker compose config

# Reset environment
make clean && make dev
```

**Database connection issues:**

```bash
# Check database health
docker compose exec goldilocks-db healthcheck.sh --connect

# Reset database
docker compose down goldilocks-db -v
docker compose up goldilocks-db -d
```

**Port conflicts:**

```bash
# Check port usage
netstat -tulpn | grep :9000

# Use different ports
BACKEND_PORT=9001 make dev
```

### Debug Mode

```bash
# Enable verbose logging
export DEBUG=1
./scripts/compose.sh development up --verbose

# Check resource usage
docker stats

# Inspect networks
docker network ls | grep goldilocks
```

## Production Considerations

### Security

- Non-root container execution
- Read-only filesystems where possible
- Docker secrets for sensitive data
- Network segmentation between services

### Monitoring

- Health check endpoints for all services
- Structured JSON logging in production
- Resource usage monitoring
- Automated backup strategies

### Scaling

```bash
# Scale backend instances
./scripts/compose.sh production scale backend=3

# Load balancer configuration required
# Database replica setup for read scaling
```
