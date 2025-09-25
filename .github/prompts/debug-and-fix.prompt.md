---
description: "Debug and fix issues in code with comprehensive analysis and testing"
mode: "agent"
tools: ["codebase", "problems", "changes", "runTasks"]
---

# Debug and Fix Issues

Analyze, debug, and fix the identified issue with comprehensive testing.

## Issue Description

- **Problem**: ${input:issue_description:Describe the issue or bug}
- **Error Message**: ${input:error_message:Paste the exact error message including stack trace if available}
- **Expected Behavior**: ${input:expected_behavior:What should happen}
- **Actual Behavior**: ${input:actual_behavior:What actually happens}
- **Reproduction Steps**: ${input:repro_steps:Steps to reproduce the issue}

## Debugging Process

1. **Issue Analysis**:

   - Understand the problem scope and impact
   - Identify affected components and dependencies
   - Review related code and recent changes
   - Check logs and error messages for clues

2. **Root Cause Investigation**:

   - Use debugging tools and techniques
   - Add logging statements if needed
   - Test assumptions and hypotheses
   - Trace code execution flow
   - Check for race conditions or timing issues

3. **Environment Analysis**:

   - Verify configuration settings
   - Check dependency versions
   - Review environment variables
   - Test in different environments
   - Check for resource constraints

4. **Code Review**:
   - Look for logic errors and edge cases
   - Check error handling and validation
   - Review recent code changes
   - Analyze variable scoping and lifecycle
   - Check for memory leaks or resource issues

## Fix Implementation

1. **Solution Design**:

   - Design minimal, targeted fix
   - Consider multiple solution approaches
   - Evaluate impact on existing functionality
   - Plan for backward compatibility
   - Consider performance implications

2. **Code Changes**:

   - Implement the most appropriate solution
   - Add proper error handling
   - Include input validation
   - Add logging for future debugging
   - Follow project coding standards

3. **Testing Strategy**:
   - Create specific tests for the bug scenario
   - Test edge cases and boundary conditions
   - Verify fix doesn't break existing functionality
   - Add regression tests to prevent recurrence
   - Test in multiple environments if applicable

## Validation Process

1. **Functional Testing**:

   - Verify the original issue is resolved
   - Test normal operation scenarios
   - Check error handling paths
   - Validate user experience improvements
   - Test with real-world data

2. **Regression Testing**:

   - Run full test suite
   - Check related functionality
   - Verify no new issues introduced
   - Test performance impact
   - Validate in staging environment

3. **Documentation Updates**:
   - Update relevant documentation
   - Add troubleshooting information
   - Document any configuration changes
   - Update API documentation if applicable
   - Add comments explaining the fix

## Flask-Specific Debugging

If debugging Flask applications:

- Check request/response flow
- Verify route configurations
- Test middleware and extensions
- Check database connections
- Validate template rendering
- Review session handling

## References

Follow the project's [Python guidelines](../instructions/python.instructions.md) and [testing practices](../instructions/testing.instructions.md).
