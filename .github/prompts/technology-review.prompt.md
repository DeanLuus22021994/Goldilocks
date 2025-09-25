---
description: "Research and review technology stack for latest implementations, syntax, and ensure everything is current"
mode: "agent"
tools: ["codebase", "fetch", "changes", "problems"]
---

# Technology Stack Review and Modernization

Conduct a comprehensive review of the current technology stack to ensure all components are using the latest stable versions, modern syntax, and current best practices.

## Review Scope

- **Focus Area**: ${input:focus_area:Full stack review, Python dependencies, Flask framework, Docker configuration, etc.}
- **Priority Level**: ${input:priority:Security updates, Performance improvements, General modernization}
- **Target Files**: ${file}

## Comprehensive Analysis Tasks

### 1. Dependency Version Analysis

**Python Dependencies Review**:

- Analyze `requirements.txt` for outdated packages
- Check `pyproject.toml` for modern packaging standards
- Research latest stable versions of all Python packages
- Identify security vulnerabilities in current versions
- Evaluate compatibility between dependency versions

**System Dependencies**:

- Review Docker base image versions and security patches
- Check Node.js and npm versions in development tools
- Analyze system package versions in container configurations

### 2. Language and Framework Modernization

**Python Language Features**:

- Review for modern Python 3.12+ syntax opportunities
- Check for deprecated functions and recommend alternatives
- Evaluate type annotation improvements and new typing features
- Identify opportunities for pattern matching (`match` statements)
- Review async/await usage and modern concurrency patterns

**Flask Framework Updates**:

- Research Flask latest version features and improvements
- Review Flask extension versions and compatibility
- Check for new security features and configuration options
- Evaluate modern Flask patterns and best practices
- Analyze performance optimizations in newer versions

### 3. Security and Vulnerability Assessment

**Security Updates**:

- Research known vulnerabilities in current package versions
- Check CVE databases for security advisories
- Evaluate security patches and critical updates
- Review authentication and authorization best practices
- Assess encryption and data protection standards

**Configuration Security**:

- Review security headers and configurations
- Check for secure defaults in framework settings
- Evaluate session management and CSRF protection
- Assess input validation and sanitization practices

### 4. Performance and Optimization Review

**Performance Improvements**:

- Research performance optimizations in newer versions
- Identify bottlenecks that newer versions address
- Evaluate caching strategies and improvements
- Review database connection and query optimization
- Assess container image size and startup time optimization

**Modern Patterns**:

- Review for modern architectural patterns
- Evaluate API design best practices evolution
- Check logging and monitoring improvements
- Assess testing framework updates and features

### 5. Development Tools and Workflow

**Development Environment**:

- Review IDE and editor support improvements
- Check linting and formatting tool updates
- Evaluate testing framework features and performance
- Review CI/CD pipeline optimization opportunities
- Assess debugging and profiling tool updates

**Docker and Containerization**:

- Research Docker base image updates and security patches
- Review multi-stage build optimization opportunities
- Check for new Docker Compose features and syntax
- Evaluate container security scanning and best practices

## Research and Verification Process

### 1. Official Documentation Research

For each component, research:

- Official project documentation and changelogs
- Migration guides and upgrade instructions
- Breaking changes and compatibility notes
- New features and improvement highlights
- Security recommendations and updates

### 2. Community and Ecosystem Analysis

- Review GitHub repositories for latest releases and issues
- Check community discussions and recommendations
- Analyze Stack Overflow trends and common patterns
- Review security advisory databases and vulnerability reports
- Evaluate maintenance status and project health

### 3. Compatibility Testing Recommendations

- Identify potential conflicts between updated versions
- Recommend testing strategies for version upgrades
- Suggest staging environment validation procedures
- Propose rollback plans and risk mitigation strategies

## Output Requirements

### 1. Current State Assessment

Provide a comprehensive report including:

- Current versions of all major dependencies and tools
- Security status and vulnerability assessment
- Performance baseline and optimization opportunities
- Compatibility matrix and potential conflicts

### 2. Modernization Recommendations

For each component, provide:

- **Current Version**: What's currently in use
- **Latest Stable Version**: Most recent stable release
- **Security Status**: Any known vulnerabilities or patches
- **Upgrade Priority**: Critical, High, Medium, or Low
- **Breaking Changes**: Any compatibility issues to consider
- **Benefits**: Performance, security, or feature improvements
- **Migration Effort**: Complexity and time estimation

### 3. Implementation Roadmap

- **Phase 1**: Critical security updates and patches
- **Phase 2**: High-priority performance and compatibility updates
- **Phase 3**: General modernization and feature adoption
- **Phase 4**: Future-proofing and preparation for upcoming changes

### 4. Specific Code Updates

For each modernization opportunity:

- Show current implementation
- Provide updated/modern alternative
- Explain benefits and rationale
- Include any necessary configuration changes
- Suggest testing validation steps

## Example Analysis Format

```markdown
## Flask Framework Analysis

**Current Version**: Flask 2.3.0
**Latest Stable**: Flask 3.1.0
**Security Status**: ✅ No known vulnerabilities
**Upgrade Priority**: Medium
**Breaking Changes**:

- Deprecated `flask.json` module (use `json` stdlib)
- Updated Jinja2 template security defaults
  **Benefits**:
- 15% performance improvement in request handling
- Enhanced async support
- Better type annotations
- Improved error messages
  **Migration Effort**: Low (2-4 hours)
  **Code Changes Required**:
- Update import statements
- Review template configurations
- Test async route compatibility
```

## Validation Steps

After providing recommendations:

1. **Verify Information**: Cross-reference multiple official sources
2. **Check Compatibility**: Ensure recommended versions work together
3. **Security Validation**: Confirm security patches and vulnerability status
4. **Testing Recommendations**: Suggest specific test cases for validation
5. **Documentation Updates**: Identify docs that need updating post-upgrade

## References

Use the project's [technology review guidelines](../instructions/technology-review.instructions.md) and maintain consistency with existing [Python standards](../instructions/python.instructions.md) and [Docker practices](../instructions/docker.instructions.md).
