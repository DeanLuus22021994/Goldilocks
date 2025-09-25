# Goldilocks Docker Infrastructure

> **MODERNIZE • STRUCTURED • STANDARDIZATION** - Enterprise-grade containerized infrastructure following industry best practices and the Goldilocks development principles.

## 🏗️ Architecture Overview

This infrastructure implements a **modular, standardized Docker Compose architecture** that follows the **Single Responsibility Principle (SRP)** with centralized shared components and environment-specific overrides.

```
infrastructure/docker/
├── 🚀 docker-compose.yml           # Main composition with includes
├── � .env                         # Docker infrastructure configuration
├── �📂 compose/                     # Modular compose definitions
│   ├── shared/                     # 🔧 Shared infrastructure
│   │   ├── networks.yml            # Network definitions
│   │   ├── volumes.yml             # Volume management
│   │   ├── secrets.yml             # Docker secrets
│   │   └── environment.env         # Application runtime configuration
│   ├── services/                   # 🎯 Service definitions
│   │   ├── database.yml            # MariaDB service
│   │   ├── backend.yml             # Python Flask app
│   │   ├── frontend.yml            # Node.js tooling
│   │   └── adminer.yml             # Database admin
│   └── overrides/                  # 🌍 Environment configs
│       ├── development.yml         # Development mode
│       ├── production.yml          # Production mode
│       ├── ci-cd.yml               # CI/CD pipeline
│       └── edge.yml                # Edge computing
├── 📂 scripts/                     # 🛠️ Management utilities
│   ├── compose.sh                  # Main management script
│   ├── test-infrastructure.sh      # Comprehensive testing
│   └── entrypoints/                # Container entrypoints
├── 📂 dockerfiles/                 # 🐳 Multi-stage builds
│   ├── Dockerfile.development      # Development image
│   ├── Dockerfile.production       # Production image
│   └── Dockerfile.multi-stage      # Advanced build
└── 📂 database-init/               # 🗄️ Database initialization
    └── 01-init-database.sql        # Schema setup
```

## 🌟 Key Features

### **STRUCTURED** - Modular Architecture

- **Shared Infrastructure**: Centralized networks, volumes, and secrets
- **Service Isolation**: Individual service definitions following SRP
- **Environment Overrides**: Profile-based configuration management
- **Management Utilities**: Automated deployment and testing scripts

### **STANDARDIZATION** - Consistent Practices

- **Naming Conventions**: Consistent `goldilocks-*` prefixes across all resources
- **Labeling Strategy**: Comprehensive metadata for resource management
- **Documentation**: Self-documenting configurations with inline comments
- **Error Handling**: Robust health checks and failure recovery

### **MODERNIZE** - Latest Technologies

- **Docker Compose 3.9**: Latest specification with advanced features
- **Multi-stage Builds**: Optimized image layers and build caching
- **Health Monitoring**: Comprehensive service health validation
- **Security Hardening**: Non-root users, secrets management, capability dropping

### **HIGH COMPATIBILITY** - Multi-Environment Support

- **Development**: Hot reload, debugging tools, comprehensive caching
- **Production**: Security hardening, resource optimization, monitoring
- **CI/CD**: Pipeline-optimized builds and testing
- **Edge Computing**: Resource-constrained deployment optimization

## 🔧 Environment Configuration

### **Two-Tier Configuration Architecture**

Following **DRY** and **STRUCTURED** principles, the infrastructure uses separate configuration files for different concerns:

#### **Docker Infrastructure (`.env`)**

**Purpose**: Docker Compose build and infrastructure settings

```bash
# Docker build configuration
PYTHON_VERSION=3.12-slim
DOCKER_BUILDKIT=1
TARGETPLATFORM=linux/amd64

# Service ports and paths
BACKEND_PORT=9000
ADMINER_PORT=8080
DATA_PATH=./data

# Container configuration
MARIADB_ROOT_PASSWORD=secure-password
MEMORY_LIMIT=512m
```

#### **Application Runtime (`compose/shared/environment.env`)**

**Purpose**: Application runtime environment variables

```bash
# Flask application settings
FLASK_DEBUG=1
LOG_LEVEL=DEBUG
API_DOCS_ENABLED=true

# Database and caching
DATABASE_URL=mysql+pymysql://...
CACHE_TYPE=redis
SESSION_TYPE=redis

# Security and features
SECRET_KEY=dev-secret-key
FEATURE_PROFILER=true
```

### **Configuration Hierarchy**

```
Backend Service Environment:
├── 📄 .env                        # Docker & infrastructure
├── 📄 shared/environment.env      # Application runtime
└── 🔧 Service environment:        # Container-specific overrides
```

## 🚀 Quick Start

### Development Environment

```bash
# Clone and navigate
git clone <repository-url>
cd Goldilocks/infrastructure/docker

# Start development environment
./scripts/compose.sh dev up

# Or manually with profiles
docker compose --profile dev up -d

# View logs
./scripts/compose.sh dev logs -f
```

### Production Deployment

```bash
# Set production environment
export GOLDILOCKS_PROFILE=prod
export NODE_ENV=production
export FLASK_ENV=production

# Deploy with production overrides
./scripts/compose.sh prod deploy

# Scale services
./scripts/compose.sh prod scale backend=3
```

### Testing Infrastructure

```bash
# Run comprehensive test suite
./scripts/test-infrastructure.sh

# Quick validation
./scripts/compose.sh validate

# Health check all services
./scripts/compose.sh health
```

## 📋 Services

### 🗄️ Database (MariaDB 11.4)

- **Purpose**: Primary data persistence with edge computing optimizations
- **Features**: Performance tuning, health monitoring, automated backups
- **Ports**: `3306` (configurable via `DB_PORT`)
- **Profiles**: `dev`, `prod`, `database`

### 🐍 Backend (Python Flask)

- **Purpose**: Main application server with development tooling
- **Features**: Hot reload, comprehensive caching, performance profiling
- **Ports**: `9000` (configurable via `BACKEND_PORT`)
- **Profiles**: `dev`, `backend`

### 🎨 Frontend (Node.js Alpine)

- **Purpose**: Frontend tooling and asset management
- **Features**: Alpine Linux base, npm/yarn caching, development utilities
- **Profiles**: `dev`, `frontend`, `tools`

### � Adminer (Database Admin)

- **Purpose**: Web-based database administration interface
- **Features**: Security hardened, MariaDB optimized, custom theming
- **Ports**: `8080` (configurable via `ADMINER_PORT`)
- **Profiles**: `dev`, `admin`, `database`

## 🌐 Network Architecture

### Application Network (`goldilocks-app-network`)

- **Subnet**: `172.20.10.0/24` - Main application communication
- **Driver**: Bridge with custom configuration
- **Isolation**: Segmented from external networks for security

### Database Network (`goldilocks-db-network`)

- **Subnet**: `172.20.20.0/24` - Database-only communication
- **Access**: Backend and admin services only
- **Security**: Restricted access with firewall rules

### Monitoring Network (`goldilocks-monitoring-network`)

- **Subnet**: `172.20.30.0/24` - Observability stack
- **Services**: Prometheus, Grafana, logging aggregation
- **Isolation**: Separate monitoring infrastructure
  ./scripts/compose.sh up development

# Or directly with docker-compose

docker-compose -f docker-compose.yml -f compose/overrides/development.yml up -d

````

### Production Environment

```bash
# Using the management utility
./scripts/compose.sh up production

# Or directly with docker-compose
docker-compose -f docker-compose.yml -f compose/overrides/production.yml up -d
````

## 🎯 Key Features

### **MODERNIZE** - Latest Technologies

- **Docker Compose 3.9** with latest features
- **Python 3.12+** with uv package manager
- **MariaDB 11.4** with edge computing optimizations
- **BuildKit 1.9** advanced caching and multi-stage builds
- **Multi-architecture support** (amd64, arm64)

### **STRUCTURED** - Organized Architecture

- **SRP-based service decomposition**
- **Shared infrastructure components**
- **Environment-specific overrides**
- **Modular configuration management**
- **Centralized utility scripts**

### **STANDARDIZATION** - Consistent Practices

- **Naming conventions** across all components
- **Labeling standards** for Docker resources
- **Environment variable patterns**
- **Security best practices**
- **Documentation standards**

### **HIGH COMPATIBILITY** - Multiple Environments

- **Development**: Hot reload, debugging tools, exposed ports
- **Production**: Security-first, encrypted networks, secrets
- **Testing**: Fast startup, in-memory databases, minimal resources
- **CI/CD**: Pipeline optimization, comprehensive testing
- **Edge**: Ultra-lightweight, local storage, minimal footprint

## 🔧 Management Utility

The `scripts/compose.sh` utility provides a standardized interface for managing all environments:

### Available Commands

```bash
# Service Management
./scripts/compose.sh up <environment>      # Start services
./scripts/compose.sh down <environment>    # Stop services
./scripts/compose.sh restart <environment> # Restart services
./scripts/compose.sh status <environment>  # Show status

# Development and Debugging
./scripts/compose.sh logs <environment>    # Show logs
./scripts/compose.sh shell <environment>   # Open shell
./scripts/compose.sh health <environment>  # Check health

# Maintenance
./scripts/compose.sh build <environment>   # Build services
./scripts/compose.sh clean <environment>   # Clean up
```

### Usage Examples

```bash
# Start development environment
./scripts/compose.sh up development -d

# Check production health
./scripts/compose.sh health production

# View application logs
./scripts/compose.sh logs development goldilocks-app

# Open shell in backend container
./scripts/compose.sh shell production goldilocks-app

# Build with no cache
./scripts/compose.sh build production --no-cache
```

## 🌐 Network Architecture

### Network Segmentation

- **goldilocks-network**: Primary application network
- **goldilocks-db-network**: Database-only network (security)
- **goldilocks-cache-network**: Cache and session network
- **goldilocks-monitoring-network**: Observability network
- **goldilocks-external**: External reverse proxy network

### IP Address Allocation

| Network    | CIDR          | Purpose                |
| ---------- | ------------- | ---------------------- |
| Primary    | 172.20.0.0/16 | Application services   |
| Database   | 172.21.0.0/24 | Database isolation     |
| Cache      | 172.22.0.0/24 | Session/cache services |
| Monitoring | 172.23.0.0/24 | Metrics and logging    |

## 💾 Volume Management

### Volume Categories

- **Application Data**: Persistent user data and uploads
- **Database**: Critical database files and backups
- **Logs**: Application and service logs
- **Cache**: Performance optimization caches
- **Configuration**: Service configuration files
- **Temporary**: High-performance tmpfs volumes

### Storage Optimization

- **Bind mounts** for production data persistence
- **Named volumes** for development flexibility
- **tmpfs volumes** for temporary high-performance storage
- **Comprehensive labeling** for backup and retention policies

## 🔐 Security Features

### Production Security

- **Docker secrets** for sensitive data
- **Encrypted overlay networks**
- **Non-root container execution**
- **Security scanning integration**
- **Minimal attack surface**

### Development Security

- **Isolated networks** for local development
- **Debug-only service exposure**
- **Development credential separation**

## 📊 Monitoring and Observability

### Health Monitoring

- **Container health checks** for all services
- **Service dependency management**
- **Automated restart policies**
- **Performance metrics collection**

### Logging Strategy

- **Structured JSON logging** for production
- **Colored console logs** for development
- **Centralized log aggregation**
- **Log retention policies**

## 🔄 Environment Management

### Environment-Specific Configurations

#### Development

- **Resource allocation**: Generous limits for productivity
- **Port exposure**: Direct access to services
- **Hot reload**: Automatic code reloading
- **Debug tools**: Profiling and debugging enabled

#### Production

- **Security-first**: Encrypted networks and secrets
- **Resource optimization**: Efficient resource usage
- **Health monitoring**: Comprehensive health checks
- **Auto-scaling**: Resource-based scaling support

#### Testing

- **Speed optimization**: Fast startup and teardown
- **Isolation**: Clean test environments
- **Minimal resources**: CI/CD optimized
- **Comprehensive testing**: Full test suite integration

#### CI/CD

- **Pipeline optimization**: Automated testing workflows
- **Artifact collection**: Test reports and coverage
- **Security scanning**: Automated vulnerability detection
- **Multi-platform builds**: Cross-architecture support

#### Edge Computing

- **Ultra-lightweight**: Minimal resource usage
- **Local storage**: Optimized for edge devices
- **Resilient networking**: Edge-optimized configurations
- **IoT compatibility**: Raspberry Pi and embedded support

## 📈 Performance Optimizations

### Container Optimization

- **Multi-stage builds** for minimal image sizes
- **Layer caching** for faster builds
- **Python bytecode compilation**
- **Dependency optimization**

### Runtime Performance

- **Optimized Python settings**
- **Database connection pooling**
- **Intelligent cache strategies**
- **Resource limit enforcement**

## 🛠️ Development Workflow

### Local Development

1. **Start environment**: `./scripts/compose.sh up development`
2. **Access services**: Application (9000), Database Admin (8080)
3. **Hot reload**: Code changes automatically reflected
4. **Debug**: Full debugging and profiling tools available

### Testing

1. **Run tests**: `./scripts/compose.sh up testing`
2. **Isolated environment**: Clean database and cache
3. **Fast execution**: Optimized for CI/CD pipelines
4. **Comprehensive coverage**: Full test suite execution

### Production Deployment

1. **Security setup**: Configure secrets and certificates
2. **Resource planning**: Set appropriate resource limits
3. **Network configuration**: Set up external networking
4. **Deploy**: `./scripts/compose.sh up production`
5. **Monitor**: Use health checks and monitoring tools

## 📚 Documentation

- **[Override Documentation](compose/overrides/README.md)**: Environment-specific configurations
- **[Network Configuration](compose/shared/networks.yml)**: Network architecture details
- **[Volume Management](compose/shared/volumes.yml)**: Storage configuration
- **[Security Setup](compose/shared/secrets.yml)**: Secrets management
- **[Environment Variables](compose/shared/environment.env)**: Configuration reference

## 🔧 Maintenance and Operations

### Regular Tasks

- **Update base images** in Dockerfiles
- **Rotate secrets** using Docker Swarm secrets
- **Clean up unused volumes** and images
- **Review resource usage** and adjust limits
- **Update dependencies** in requirements files

### Backup and Recovery

- **Database backups**: Automated backup volumes
- **Configuration backups**: Version-controlled configs
- **Application data**: Persistent volume backups
- **Disaster recovery**: Multi-environment deployment

### Monitoring and Alerting

- **Health check failures**: Automated restart policies
- **Resource usage**: Memory and CPU monitoring
- **Performance metrics**: Application performance tracking
- **Log analysis**: Centralized log monitoring

---

This Docker infrastructure provides a **production-ready**, **scalable**, and **maintainable** foundation for the Goldilocks application, following industry best practices and modern containerization principles.
