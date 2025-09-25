# Docker Compose Environment Overrides

This directory contains environment-specific override files that extend the base Docker Compose configuration to support different deployment scenarios while following our **STRUCTURED**, **HIGH COMPATIBILITY**, and **MODERNIZE** principles.

## 📁 Override Files

### 🛠️ `development.yml`

**Purpose**: Local development environment with hot reload and debugging tools

- **Features**: Hot reload, exposed ports, development database, Adminer access
- **Resources**: Generous limits for development productivity
- **Usage**: Daily development work, debugging, testing new features

### 🚀 `production.yml`

**Purpose**: Production deployment with security and performance optimizations

- **Features**: Encrypted networks, secrets management, health checks, logging
- **Resources**: Optimized limits, auto-restart policies
- **Usage**: Production deployments, staging environments

### 🧪 `testing.yml`

**Purpose**: Automated testing environment with fast startup/teardown

- **Features**: In-memory databases, minimal resources, test-specific configurations
- **Resources**: Minimal for CI/CD efficiency
- **Usage**: Unit tests, integration tests, local test runs

### 🔄 `ci-cd.yml`

**Purpose**: CI/CD pipeline environment with comprehensive testing

- **Features**: PostgreSQL for speed, security scanning, type checking, coverage reports
- **Resources**: Optimized for CI runners
- **Usage**: GitHub Actions, Jenkins, automated pipelines

### 📱 `edge.yml`

**Purpose**: Edge computing and IoT deployments with minimal resource usage

- **Features**: SQLite support, local storage, ultra-lightweight configuration
- **Resources**: Extremely constrained for edge devices
- **Usage**: Raspberry Pi, IoT devices, edge computing scenarios

## 🚀 Usage Examples

### Development Environment

```bash
# Start development environment with hot reload
docker-compose -f docker-compose.yml -f compose/overrides/development.yml up -d

# View logs
docker-compose -f docker-compose.yml -f compose/overrides/development.yml logs -f

# Access Adminer at http://localhost:8080
```

### Production Environment

```bash
# Deploy to production with secrets
docker-compose -f docker-compose.yml -f compose/overrides/production.yml up -d

# Check health status
docker-compose -f docker-compose.yml -f compose/overrides/production.yml ps
```

### Testing Environment

```bash
# Run tests with isolated database
docker-compose -f docker-compose.yml -f compose/overrides/testing.yml run --rm goldilocks-app

# Clean up test environment
docker-compose -f docker-compose.yml -f compose/overrides/testing.yml down -v
```

### CI/CD Pipeline

```bash
# Run comprehensive CI/CD tests
export BUILD_TAG=ci-$(date +%s)
export BUILD_NUMBER=${GITHUB_RUN_NUMBER}
export COMMIT_SHA=${GITHUB_SHA}
export BRANCH_NAME=${GITHUB_REF_NAME}

docker-compose -f docker-compose.yml -f compose/overrides/ci-cd.yml run --rm goldilocks-app
```

### Edge Computing

```bash
# Deploy to edge device (minimal resources)
docker-compose -f docker-compose.yml -f compose/overrides/edge.yml up -d

# Use with external database when needed
docker-compose -f docker-compose.yml -f compose/overrides/edge.yml --profile with-database up -d
```

## 🔧 Configuration Profiles

Each override file supports different **profiles** for additional flexibility:

- **`debug`**: Additional debugging services (Adminer, monitoring tools)
- **`with-database`**: Include database services (useful for edge computing)
- **`monitoring`**: Additional monitoring and metrics collection

### Using Profiles

```bash
# Include debug tools in production
docker-compose -f docker-compose.yml -f compose/overrides/production.yml --profile debug up -d

# Edge computing with database
docker-compose -f docker-compose.yml -f compose/overrides/edge.yml --profile with-database up -d
```

## 📊 Resource Requirements

| Environment | Memory | CPU       | Storage | Network |
| ----------- | ------ | --------- | ------- | ------- |
| Development | ~1.5GB | 2+ cores  | ~5GB    | Bridge  |
| Production  | ~768MB | 1+ core   | ~10GB   | Overlay |
| Testing     | ~256MB | 0.5 core  | ~1GB    | Bridge  |
| CI/CD       | ~512MB | 1 core    | ~2GB    | Bridge  |
| Edge        | ~128MB | 0.25 core | ~500MB  | Bridge  |

## 🔐 Security Considerations

### Production Security Features

- **Secrets Management**: Database passwords via Docker secrets
- **Network Encryption**: Overlay networks with encryption
- **No External Access**: Database ports not exposed
- **Health Monitoring**: Comprehensive health checks
- **Resource Limits**: Prevents resource exhaustion attacks

### Development Security Notes

- **Exposed Ports**: Database accessible for development tools
- **Debug Mode**: Enabled for development productivity
- **Weak Passwords**: Use only for local development

## 🌐 Network Architecture

### Development

- **Subnet**: `172.20.0.0/16`
- **Type**: Bridge network
- **Access**: External ports exposed

### Production

- **Subnet**: `10.0.1.0/24`
- **Type**: Overlay network (encrypted)
- **Access**: Application port only

### Testing

- **Subnet**: `172.30.0.0/16`
- **Type**: Bridge network
- **Access**: Application port only

### CI/CD

- **Subnet**: `172.40.0.0/16`
- **Type**: Bridge network
- **Access**: Internal only

### Edge

- **Subnet**: `172.50.0.0/24`
- **Type**: Bridge network (MTU optimized)
- **Access**: Application port only

## 📈 Monitoring and Observability

Each environment includes appropriate monitoring configurations:

- **Development**: Debug logging, profiling enabled
- **Production**: JSON logging, health checks, metrics collection
- **Testing**: Minimal logging, fast health checks
- **CI/CD**: Structured logging, test reports, security scans
- **Edge**: Warning-level logging, basic health checks

## 🔄 Maintenance and Updates

### Regular Tasks

1. **Update base images** in each override file
2. **Review resource limits** based on actual usage
3. **Rotate secrets** in production environment
4. **Clean up test volumes** after CI/CD runs
5. **Monitor edge device resources** and adjust limits

### Best Practices

- **Version Control**: All override files should be version controlled
- **Environment Parity**: Keep configurations as similar as possible
- **Documentation**: Update this README when adding new overrides
- **Testing**: Test override files in staging before production deployment

---

This override system provides **HIGH COMPATIBILITY** across different deployment scenarios while maintaining **STRUCTURED** organization and **MODERNIZE** deployment practices. Each environment is optimized for its specific use case while sharing the common base configuration.
