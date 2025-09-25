# AI Agents Configuration for Goldilocks Development

This file defines custom instructions and configurations for AI agents working on the Goldilocks Flask application. These instructions ensure consistent, high-quality development practices across all AI-assisted development activities.

## Project Overview

Goldilocks is a modern Flask application that follows **MODERNIZE**, **DRY**, **SRP**, **STRUCTURED**, and **SOLID** principles. The codebase emphasizes:

- **Clean Architecture**: Separation of concerns with clear module boundaries
- **Type Safety**: Comprehensive type annotations throughout
- **Test Coverage**: 100% test coverage with pytest
- **Security First**: Input validation, authentication, and secure defaults
- **Performance**: Optimized for containers and cloud deployment
- **Documentation**: Clear, comprehensive documentation at all levels

## Agent Behavioral Guidelines

### Code Generation Standards

- Always include type hints for all function parameters and return values
- Write comprehensive docstrings using Google style format
- Implement proper error handling with specific exception types
- Follow PEP 8 style guidelines with Black formatting (88 character line limit)
- Use f-strings for string formatting and pathlib for file operations
- Prefer composition over inheritance and favor explicit over implicit

### Testing Requirements

- Generate tests for all new code using pytest framework
- Aim for 100% line and branch coverage
- Mock external dependencies and I/O operations
- Test both success and failure scenarios including edge cases
- Use descriptive test names that explain what is being tested
- Include integration tests for API endpoints

### Flask-Specific Practices

- Use Flask blueprints for organizing routes and maintaining separation of concerns
- Implement proper request validation using schemas or decorators
- Return consistent JSON response formats with appropriate HTTP status codes
- Use Flask-Login for authentication and implement CSRF protection
- Apply proper error handling with custom error handlers
- Include structured logging with correlation IDs for tracing

### Security Considerations

- Validate and sanitize all user inputs to prevent injection attacks
- Use parameterized queries for database operations
- Implement proper authentication and authorization checks
- Avoid hardcoding sensitive information; use environment variables
- Apply security headers and configure CORS appropriately
- Log security events for monitoring and audit trails

### Performance Optimization

- Use database connection pooling and query optimization
- Implement proper caching strategies for frequently accessed data
- Optimize Docker images with multi-stage builds and minimal layers
- Monitor resource usage and implement proper error boundaries
- Use async patterns where appropriate for I/O operations
- Profile code before making performance optimizations

## Development Workflow Integration

### Version Control

- Make atomic commits that focus on a single change or feature
- Write clear, descriptive commit messages using conventional format
- Keep commits small and focused to facilitate code review
- Always include tests with feature implementations
- Update documentation concurrently with code changes

### Code Quality Automation

- All code must pass pre-commit hooks (Black, isort, flake8, mypy)
- CI/CD pipeline must pass all tests and quality checks
- Use semantic versioning for releases and maintain changelog
- Apply security scanning and dependency updates via Dependabot
- Monitor code coverage and maintain quality metrics

### Documentation Practices

- Update README files when adding new features or changing setup
- Maintain API documentation with examples and proper status codes
- Document architectural decisions and design rationales
- Include troubleshooting guides for common issues
- Write clear installation and development setup instructions

## AI Agent Collaboration

### Multi-Agent Coordination

When working with multiple AI agents:

- **Planning Agent**: Focus on high-level architecture and feature design
- **Implementation Agent**: Handle detailed coding and testing
- **Review Agent**: Conduct code review and security analysis
- **Documentation Agent**: Maintain comprehensive documentation

### Context Sharing

- Reference existing code patterns and established conventions
- Maintain consistency with existing error handling and logging
- Use established database models and API patterns
- Follow the project's naming conventions and file organization
- Consider impact on existing functionality and backward compatibility

### Quality Assurance

- Validate all generated code against project standards
- Ensure compatibility with existing codebase architecture
- Test integrations with existing components and services
- Verify compliance with security and performance requirements
- Check documentation accuracy and completeness

## Tool and Extension Integration

### VS Code Copilot Features

- Leverage agent mode for complex, multi-file changes
- Use custom instructions for context-aware code generation
- Apply prompt files for standardized development tasks
- Utilize tool sets for grouped functionality operations
- Enable auto-fix for syntax errors and test failures

### Development Environment

- Use the configured dev container for consistent environment
- Leverage VS Code tasks for common development operations
- Use integrated debugging and profiling tools effectively
- Apply proper extension configurations for Python and Flask
- Maintain workspace settings for team consistency

## Continuous Improvement

### Learning and Adaptation

- Learn from code review feedback and apply lessons
- Adapt to evolving project requirements and standards
- Incorporate new Python and Flask features appropriately
- Update practices based on security advisories and best practices
- Share knowledge through improved documentation and examples

### Feedback Integration

- Apply feedback from manual code reviews
- Adjust based on testing results and quality metrics
- Incorporate user feedback for feature improvements
- Learn from production issues and implement preventive measures
- Contribute to project standards and guideline evolution

---

These instructions ensure all AI agents working on Goldilocks maintain consistency, quality, and alignment with project goals while enabling efficient, secure, and maintainable development practices.
