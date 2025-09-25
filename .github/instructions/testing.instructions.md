---
applyTo: "**/test_*.py,**/*_test.py,**/tests/**/*.py"
description: "Testing standards and practices for Python test files"
---

# Testing Instructions

## Test Structure and Organization

- Use descriptive test class names starting with `Test`
- Group related tests in classes
- Use descriptive test method names that explain what is being tested
- Follow the Arrange-Act-Assert pattern
- Keep tests isolated and independent

## Pytest Best Practices

- Use pytest fixtures for common setup and teardown
- Leverage pytest parameterization for testing multiple scenarios
- Use meaningful assertion messages
- Prefer `pytest.raises()` for exception testing
- Use `pytest.mark` for test categorization

## Mocking and Test Doubles

- Mock external dependencies and I/O operations
- Use `unittest.mock` or `pytest-mock` for mocking
- Mock at the boundary of your system
- Avoid mocking internal implementation details
- Use fixtures for consistent mock setups

## Test Coverage and Quality

- Aim for 100% line and branch coverage
- Test both happy path and edge cases
- Include negative test cases for error handling
- Test boundary conditions and edge cases
- Verify proper cleanup in teardown methods

## Flask Testing Patterns

- Use Flask's test client for integration tests
- Create test fixtures for database state
- Test API endpoints with various input scenarios
- Verify proper HTTP status codes and response formats
- Test authentication and authorization flows

## Test Data Management

- Use factories or builders for creating test data
- Keep test data minimal and focused
- Use fixtures for shared test data
- Clean up test data after each test
- Use in-memory databases for faster tests

## Performance Testing

- Write performance tests for critical paths
- Use `pytest-benchmark` for performance regression testing
- Profile slow tests and optimize when necessary
- Keep unit tests fast (under 10ms each)
- Separate slow integration tests from fast unit tests

## Test Documentation

- Document complex test scenarios
- Explain test setup when not obvious
- Include references to requirements being tested
- Document known test limitations
- Keep test code as clean as production code
