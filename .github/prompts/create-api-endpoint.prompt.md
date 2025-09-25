---
description: "Create a new Flask API endpoint with proper validation, error handling, and tests"
mode: "agent"
tools: ["codebase", "changes", "usages"]
---

# Create Flask API Endpoint

Create a new Flask API endpoint with the following requirements:

## Endpoint Specifications

- **Path**: ${input:endpoint_path:/api/v1/example}
- **Method**: ${input:http_method:GET}
- **Description**: ${input:description:API endpoint description}

## Implementation Requirements

1. **Route Definition**:

   - Use appropriate Flask blueprint
   - Include proper HTTP method decoration
   - Add route documentation

2. **Input Validation**:

   - Validate request data using schemas
   - Return proper error responses for invalid input
   - Include parameter type checking

3. **Error Handling**:

   - Implement proper exception handling
   - Return consistent error response format
   - Log errors with appropriate context

4. **Response Format**:

   - Return JSON responses with consistent structure
   - Include appropriate HTTP status codes
   - Add response headers if needed

5. **Authentication & Authorization**:

   - Add authentication decorators if required
   - Implement proper authorization checks
   - Handle unauthorized access gracefully

6. **Testing**:

   - Create unit tests for the endpoint
   - Test both success and error scenarios
   - Include integration tests if appropriate
   - Mock external dependencies

7. **Documentation**:
   - Add comprehensive docstrings
   - Include API documentation comments
   - Provide usage examples

## Code Structure

Follow the existing project patterns:

- Use the established error handling patterns
- Follow the logging conventions
- Maintain consistency with existing endpoints
- Include proper type hints

## References

Reference the existing Flask patterns in [src/goldilocks/api/](../../src/goldilocks/api/) and follow the project's [Python instructions](../instructions/python.instructions.md).
