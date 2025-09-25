---
applyTo: "**"
description: "Technology review and modernization guidelines for keeping code current"
---

# Technology Review and Modernization Instructions

## Review Scope and Objectives

- Analyze current technology stack versions and compatibility
- Research latest stable versions of frameworks and dependencies
- Identify deprecated features and recommend modern alternatives
- Ensure security patches and vulnerability fixes are current
- Evaluate performance improvements in newer versions
- Review syntax and language features for modernization opportunities

## Version Analysis Requirements

1. **Dependency Review**:

   - Check all package versions in requirements.txt, package.json, etc.
   - Compare current versions with latest stable releases
   - Identify major version upgrades and breaking changes
   - Review security advisories for current versions
   - Assess compatibility between dependencies

2. **Language Feature Analysis**:

   - Review Python syntax for latest language features
   - Check for deprecated functions and methods
   - Identify opportunities to use newer language constructs
   - Evaluate type system improvements and annotations
   - Review async/await patterns and modern concurrency

3. **Framework Updates**:
   - Analyze Flask version and extension compatibility
   - Review web framework best practices evolution
   - Check for new security features and configurations
   - Evaluate performance optimizations in newer versions
   - Review API design patterns and modern approaches

## Research Methodology

1. **Official Documentation Review**:

   - Check official project documentation for latest features
   - Review migration guides and upgrade paths
   - Identify breaking changes and compatibility issues
   - Study new configuration options and best practices
   - Evaluate security recommendations and updates

2. **Community and Ecosystem Analysis**:

   - Research community best practices and patterns
   - Review popular libraries and their update status
   - Analyze performance benchmarks and comparisons
   - Study security vulnerability databases
   - Evaluate maintenance status of dependencies

3. **Compatibility Assessment**:
   - Test compatibility between component versions
   - Identify potential conflicts or issues
   - Evaluate upgrade complexity and effort required
   - Assess rollback strategies and risk mitigation
   - Review testing requirements for updates

## Modernization Priorities

1. **Security Updates** (Highest Priority):

   - Critical security vulnerabilities
   - Authentication and authorization improvements
   - Encryption and data protection updates
   - Input validation and sanitization enhancements

2. **Performance Improvements** (High Priority):

   - Database query optimizations
   - Caching mechanism updates
   - Memory usage improvements
   - Response time optimizations

3. **Developer Experience** (Medium Priority):

   - IDE and tooling improvements
   - Debugging and logging enhancements
   - Testing framework updates
   - Documentation and error message clarity

4. **Future Compatibility** (Medium Priority):
   - Preparation for upcoming version changes
   - Adoption of stable new features
   - Removal of deprecated functionality
   - Modern syntax and pattern adoption

## Implementation Guidelines

1. **Gradual Updates**:

   - Prioritize security and critical updates first
   - Implement changes incrementally
   - Maintain backward compatibility when possible
   - Test thoroughly at each stage
   - Document all changes and rationale

2. **Risk Management**:

   - Create backup and rollback plans
   - Test in staging environments first
   - Monitor for regressions after updates
   - Maintain comprehensive test coverage
   - Document known issues and workarounds

3. **Documentation Requirements**:
   - Update version compatibility information
   - Document migration steps and procedures
   - Maintain changelog of all updates
   - Update deployment and configuration guides
   - Record lessons learned and best practices

## Validation and Testing

1. **Automated Testing**:

   - Run full test suite after each update
   - Include integration and end-to-end tests
   - Verify performance benchmarks
   - Test security configurations
   - Validate configuration and deployment scripts

2. **Manual Verification**:
   - Review functionality in development environment
   - Test user workflows and edge cases
   - Verify third-party integrations
   - Check monitoring and logging systems
   - Validate backup and recovery procedures

## Continuous Monitoring

1. **Update Tracking**:

   - Monitor security advisory feeds
   - Track dependency update notifications
   - Review framework and language roadmaps
   - Subscribe to relevant security bulletins
   - Maintain update schedule and calendar

2. **Health Metrics**:
   - Monitor application performance trends
   - Track security scan results
   - Review dependency vulnerability reports
   - Analyze error rates and patterns
   - Evaluate user experience metrics
