---
description: "Refactor code to improve maintainability, performance, or architecture"
mode: "agent"
tools: ["codebase", "changes", "usages", "problems"]
---

# Code Refactoring

Refactor the specified code to improve its quality, maintainability, and performance.

## Refactoring Target

- **File(s)**: ${file}
- **Component**: ${input:component:Function, class, or module to refactor}
- **Goal**: ${input:refactoring_goal:What aspect to improve (performance, readability, architecture, etc.)}

## Refactoring Principles

1. **Code Quality Improvements**:

   - Apply DRY (Don't Repeat Yourself) principle
   - Follow Single Responsibility Principle (SRP)
   - Improve code readability and clarity
   - Enhance error handling and edge cases
   - Add or improve type hints and documentation

2. **Performance Optimization**:

   - Identify and eliminate bottlenecks
   - Optimize algorithms and data structures
   - Reduce memory usage and allocations
   - Improve I/O efficiency
   - Profile before and after changes

3. **Architecture Improvements**:

   - Separate concerns appropriately
   - Reduce coupling between components
   - Improve cohesion within modules
   - Enhance testability and modularity
   - Follow established design patterns

4. **Maintainability Enhancements**:
   - Simplify complex logic
   - Break down large functions or classes
   - Improve naming conventions
   - Add comprehensive documentation
   - Enhance error messages and logging

## Refactoring Process

1. **Analysis Phase**:

   - Understand the current implementation
   - Identify code smells and improvement opportunities
   - Analyze dependencies and usage patterns
   - Review existing tests for coverage

2. **Planning Phase**:

   - Define specific refactoring goals
   - Identify potential breaking changes
   - Plan incremental refactoring steps
   - Consider backward compatibility requirements

3. **Implementation Phase**:

   - Make changes incrementally
   - Maintain or improve test coverage
   - Update documentation and comments
   - Verify functionality remains unchanged

4. **Validation Phase**:
   - Run all existing tests
   - Add new tests if needed
   - Verify performance improvements
   - Check for regressions or side effects

## Safety Requirements

- Maintain backward compatibility unless explicitly requested
- Preserve all existing functionality
- Update or add tests to cover refactored code
- Ensure no performance regressions
- Update related documentation

## Flask-Specific Considerations

If refactoring Flask components:

- Maintain API compatibility
- Preserve request/response formats
- Update route documentation
- Consider impact on middleware and extensions
- Test with various request scenarios

## References

Follow the project's [Python instructions](../instructions/python.instructions.md) and [code style guidelines](../instructions/code-style.instructions.md).
