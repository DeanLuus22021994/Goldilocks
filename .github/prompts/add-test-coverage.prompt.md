---
description: "Add comprehensive test coverage for a specific function or class"
mode: "agent"
tools: ["codebase", "changes", "problems"]
---

# Add Test Coverage

Add comprehensive test coverage for the specified code component.

## Target Component

- **File**: ${file}
- **Function/Class**: ${input:component_name:Function or class name to test}
- **Test Type**: ${input:test_type:unit,integration,end-to-end}

## Test Requirements

1. **Test Structure**:

   - Use pytest framework
   - Organize tests in logical test classes
   - Use descriptive test method names
   - Follow Arrange-Act-Assert pattern

2. **Coverage Goals**:

   - Test all public methods and functions
   - Cover both success and failure scenarios
   - Test edge cases and boundary conditions
   - Include negative test cases for error handling
   - Aim for 100% line and branch coverage

3. **Test Data and Mocking**:

   - Use pytest fixtures for test data setup
   - Mock external dependencies and I/O operations
   - Create realistic test data that reflects actual usage
   - Ensure test isolation and independence

4. **Assertions and Validation**:

   - Use specific and meaningful assertions
   - Verify both return values and side effects
   - Check proper exception handling
   - Validate state changes when applicable

5. **Performance and Resource Tests**:
   - Include performance benchmarks for critical paths
   - Test resource cleanup and memory management
   - Verify proper handling of timeouts and limits
   - Test concurrent access if applicable

## Flask-Specific Testing

If testing Flask components:

- Use Flask test client for endpoint testing
- Test with various HTTP methods and payloads
- Verify proper status codes and response formats
- Test authentication and authorization flows
- Mock database operations appropriately

## Documentation

- Add docstrings to test classes and complex test methods
- Include comments for complex test setup or assertions
- Document any test-specific configuration or requirements
- Reference requirements or user stories being tested

## References

Follow the project's [testing instructions](../instructions/testing.instructions.md) and [Python guidelines](../instructions/python.instructions.md).
