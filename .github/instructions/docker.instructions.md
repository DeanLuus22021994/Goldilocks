---
applyTo: "**/Dockerfile*,**/docker-compose*.yml,**/docker-compose*.yaml"
description: "Docker and containerization best practices"
---

# Docker and Containerization Instructions

## Dockerfile Best Practices

- Use specific base image versions, never `latest`
- Use multi-stage builds for production optimization
- Minimize the number of layers by combining RUN commands
- Use `.dockerignore` to exclude unnecessary files
- Run containers as non-root users for security
- Set appropriate WORKDIR and use absolute paths

## Layer Optimization

- Copy `requirements.txt` before copying source code for better caching
- Install dependencies in a separate layer before copying application code
- Use `--no-cache-dir` flag when installing packages with pip
- Clean up package manager caches in the same layer
- Order instructions from least to most frequently changing

## Security Practices

- Use minimal base images (alpine, slim variants)
- Run as non-root user with USER instruction
- Don't include secrets or credentials in images
- Use build-time secrets for sensitive data
- Scan images for vulnerabilities regularly
- Keep base images updated

## Container Configuration

- Use EXPOSE to document which ports the container listens on
- Set appropriate resource limits and requests
- Use health checks to monitor container status
- Configure proper signal handling for graceful shutdown
- Set timezone explicitly if needed

## Docker Compose Guidelines

- Do not use version of docker-compose.yml format as it is obsolete
- Define services with descriptive names
- Use environment variables for configuration
- Implement proper volume mounts for persistence
- Configure restart policies appropriately
- Use networks to isolate services

## Development vs Production

- Use different Dockerfiles for development and production
- Enable debug modes only in development
- Use volume mounts for development hot-reload
- Optimize image size for production builds
- Use secrets management for production credentials
- Implement proper logging configuration

## Performance Optimization

- Use build caches effectively
- Minimize image size by removing unnecessary files
- Use appropriate image compression
- Configure proper resource limits
- Use health checks for better orchestration
- Implement graceful shutdown handling

## Monitoring and Logging

- Use structured logging with JSON format
- Configure log rotation and retention
- Expose metrics endpoints for monitoring
- Use standard output for container logs
- Implement health check endpoints
- Monitor resource usage and performance
