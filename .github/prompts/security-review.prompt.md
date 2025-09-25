---
description: "Perform a comprehensive security review of code, focusing on vulnerabilities and best practices"
mode: "agent"
tools: ["codebase", "problems", "changes"]
---

# Security Review

Conduct a thorough security review of the specified code components.

## Review Scope

- **Files**: ${file}
- **Focus Area**: ${input:focus_area:Authentication, authorization, input validation, data handling, etc.}
- **Security Level**: ${input:security_level:Basic, Standard, High-security}

## Security Analysis Areas

1. **Input Validation and Sanitization**:

   - Check for SQL injection vulnerabilities
   - Verify XSS prevention measures
   - Validate input parsing and type checking
   - Review file upload security
   - Check for command injection risks

2. **Authentication and Authorization**:

   - Review authentication mechanisms
   - Check session management security
   - Verify authorization controls
   - Analyze password handling practices
   - Check for privilege escalation risks

3. **Data Protection**:

   - Review data encryption at rest and in transit
   - Check for sensitive data exposure
   - Verify secure configuration handling
   - Review logging practices for sensitive data
   - Check database security practices

4. **API Security**:

   - Review rate limiting and throttling
   - Check CORS configuration
   - Verify proper HTTP headers
   - Review error message information disclosure
   - Check API versioning security

5. **Dependency Security**:
   - Check for known vulnerable dependencies
   - Review third-party library usage
   - Verify dependency update practices
   - Check for supply chain security risks

## Security Best Practices Verification

1. **OWASP Top 10 Compliance**:

   - Injection vulnerabilities
   - Broken authentication
   - Sensitive data exposure
   - XML External Entities (XXE)
   - Broken access control
   - Security misconfiguration
   - Cross-site scripting (XSS)
   - Insecure deserialization
   - Using components with known vulnerabilities
   - Insufficient logging and monitoring

2. **Flask-Specific Security**:
   - CSRF protection implementation
   - Secure cookie configuration
   - Content Security Policy headers
   - Session security configuration
   - Template security practices

## Security Findings Format

For each finding, provide:

- **Severity**: Critical, High, Medium, Low
- **Description**: Clear explanation of the security issue
- **Impact**: Potential consequences if exploited
- **Recommendation**: Specific remediation steps
- **Code Example**: Secure implementation example

## Compliance Considerations

Check compliance with relevant standards:

- PCI DSS for payment data
- GDPR for personal data protection
- SOC 2 for security controls
- Industry-specific requirements

## References

Follow security guidelines in [code style instructions](../instructions/code-style.instructions.md) and [Python security practices](../instructions/python.instructions.md).
