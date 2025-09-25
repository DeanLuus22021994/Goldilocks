---
applyTo: "**"
description: "General coding standards and conventions for all languages"
---

# Project General Coding Standards

## Naming Conventions

- Use PascalCase for class names, interfaces, and type aliases
- Use camelCase for variables, functions, and methods (JavaScript/TypeScript)
- Use snake_case for variables, functions, and methods (Python)
- Prefix private class members with underscore (\_) in Python
- Use ALL_CAPS for constants across all languages
- Use descriptive names that clearly indicate purpose

## Error Handling

- Use try/catch blocks for async operations
- Implement proper error boundaries in React components
- Always log errors with contextual information
- Use specific exception types instead of generic ones
- Provide meaningful error messages to users
- Implement proper fallback mechanisms

## Code Organization

- Follow single responsibility principle
- Keep functions focused and concise
- Group related functionality together
- Use consistent file and folder naming conventions
- Maintain clear module boundaries
- Avoid deep nesting (max 3-4 levels)

## Documentation Standards

- Write clear, concise comments explaining the "why", not the "what"
- Maintain up-to-date README files
- Document API endpoints and their parameters
- Include usage examples in documentation
- Use JSDoc for JavaScript/TypeScript
- Use docstrings for Python functions and classes

## Version Control

- Use semantic commit messages
- Make atomic commits that focus on a single change
- Write descriptive commit messages
- Use conventional commit format when possible
- Keep commits small and focused
- Always review changes before committing

## Performance & Security

- Validate all user inputs
- Use parameterized queries to prevent SQL injection
- Implement proper authentication and authorization
- Avoid hardcoding sensitive information
- Optimize for readability first, then performance
- Profile before optimizing
- Use secure defaults for all configurations
