# Goldilocks Copilot Development Workflow

This guide explains how to leverage the advanced GitHub Copilot features configured for the Goldilocks project to maximize development efficiency and code quality.

## Overview

The Goldilocks project is now equipped with comprehensive AI-powered development tools including:

- **Custom Instructions** - Context-aware code generation following project standards
- **Prompt Files** - Reusable templates for common development tasks
- **Agent Mode** - Autonomous multi-file editing and complex task handling
- **Tool Sets** - Organized collections of development tools
- **Multi-Agent Workflows** - Coordinated AI assistance across different development phases

## Getting Started

### Prerequisites

1. **VS Code Version**: Ensure you're using VS Code 1.99 or later
2. **GitHub Copilot**: Have an active Copilot subscription
3. **Extensions**: Install GitHub Copilot and GitHub Copilot Chat extensions
4. **Settings**: The project already includes optimized Copilot settings

### Initial Setup

1. Open the Goldilocks workspace in VS Code
2. The custom settings will automatically enable all Copilot features
3. Restart VS Code if prompted to ensure all settings take effect
4. Verify Copilot is active by checking the status bar

## Feature Guide

### 1. Custom Instructions

Custom instructions automatically guide Copilot to follow project standards without manual specification.

#### Available Instruction Files

- **General Code Style** (`.github/instructions/code-style.instructions.md`)

  - Applied to all files (`applyTo: "**"`)
  - Covers naming conventions, error handling, documentation standards

- **Python Specific** (`.github/instructions/python.instructions.md`)

  - Applied to Python files (`applyTo: "**/*.py"`)
  - Includes type annotations, Flask patterns, testing standards

- **Testing Guidelines** (`.github/instructions/testing.instructions.md`)

  - Applied to test files (`applyTo: "**/test_*.py,**/*_test.py,**/tests/**/*.py"`)
  - Covers pytest best practices, mocking, coverage requirements

- **Docker Instructions** (`.github/instructions/docker.instructions.md`)

  - Applied to Docker files (`applyTo: "**/Dockerfile*,**/docker-compose*.yml"`)
  - Security practices, optimization, best practices

- **Documentation Standards** (`.github/instructions/documentation.instructions.md`)
  - Applied to documentation files (`applyTo: "**/*.md,**/*.rst,**/docs/**"`)
  - Markdown standards, API documentation, user guides

#### Usage

Instructions are automatically applied based on file context. No manual action required!

```python
# When editing a Python file, Copilot automatically knows to:
# - Add type hints
# - Follow PEP 8
# - Write comprehensive docstrings
# - Include proper error handling

def process_user_data(user_id: str) -> dict[str, Any]:
    """Process user data with validation and error handling."""
    # Copilot will suggest code following project standards
```

### 2. Prompt Files

Reusable prompt templates for common development tasks.

#### Available Prompts

Access prompts by typing `/` followed by the prompt name in chat:

- **`/create-api-endpoint`** - Generate Flask API endpoints with validation and tests
- **`/add-test-coverage`** - Add comprehensive test coverage for functions/classes
- **`/refactor-code`** - Refactor code for better maintainability and performance
- **`/security-review`** - Perform security analysis and vulnerability assessment
- **`/debug-and-fix`** - Debug and resolve issues with comprehensive analysis
- **`/technology-review`** - Research and review technology stack for latest implementations and syntax

#### Usage Examples

```bash
# Create a new API endpoint
/create-api-endpoint: endpoint_path=/api/v1/users, http_method=POST, description=Create new user account

# Add test coverage for a specific function
/add-test-coverage: component_name=UserService.create_user, test_type=unit

# Review technology stack for updates
/technology-review: focus_area=Python dependencies, priority=Security updates

# Refactor existing code
/refactor-code: component=auth_service.py, refactoring_goal=improve performance and readability
```

### 3. Agent Mode

Agent mode enables autonomous multi-file editing for complex tasks.

#### Enabling Agent Mode

1. Open Chat view (`Ctrl+Alt+I`)
2. Select **Agent** from the chat mode selector
3. Or use direct links:
   - [Stable](vscode://GitHub.Copilot-Chat/chat?mode=agent)
   - [Insiders](vscode-insiders://GitHub.Copilot-Chat/chat?mode=agent)

#### Agent Mode Capabilities

- **Autonomous Context Detection** - Determines relevant files automatically
- **Multi-File Editing** - Makes changes across multiple files simultaneously
- **Tool Invocation** - Uses development tools as needed
- **Iterative Problem Solving** - Resolves issues through multiple iterations
- **Auto-Fix** - Automatically diagnoses and fixes syntax errors

#### Usage Examples

```bash
# High-level feature requests
"Add Redis caching to the user service"
"Refactor authentication to use OAuth 2.0"
"Add comprehensive logging throughout the application"
"Optimize database queries for better performance"
"Add input validation to all API endpoints"
```

### 4. Tool Sets

Organized collections of development tools for specific tasks.

#### Available Tool Sets

- **`development`** - General development tasks (codebase, changes, usages, problems)
- **`testing`** - Testing and QA focused tools (problems, codebase, changes, runTasks)
- **`debugging`** - Debugging and troubleshooting (problems, codebase, changes, runTasks)
- **`refactoring`** - Code refactoring tools (codebase, usages, changes, problems)
- **`documentation`** - Documentation tools (codebase, changes)
- **`security`** - Security analysis tools (codebase, problems, changes)
- **`research`** - Technology research and modernization analysis (codebase, fetch, changes, problems)

#### Usage

1. In Agent mode, click the **Tools** icon
2. Select appropriate tool set from the dropdown
3. Or reference directly: `#development`, `#security`, or `#research`

### 5. AGENTS.md Multi-Agent Workflows

The `AGENTS.md` file provides comprehensive instructions for coordinated AI development.

#### Agent Roles

- **Planning Agent** - Architecture and feature design
- **Implementation Agent** - Detailed coding and testing
- **Review Agent** - Code review and security analysis
- **Documentation Agent** - Comprehensive documentation

#### Workflow Integration

The AGENTS.md file ensures all AI agents:

- Follow consistent coding standards
- Maintain project architecture principles
- Apply security best practices
- Generate comprehensive tests
- Update documentation concurrently

## Technology Review and Modernization

### Keeping the Stack Current

The project includes comprehensive tools for maintaining an up-to-date technology stack:

#### Technology Review Workflow

1. **Regular Reviews**: Use `/technology-review` prompt to assess current state
2. **Targeted Analysis**: Focus on specific areas (dependencies, security, performance)
3. **Research Integration**: Leverages `fetch` tool to research latest versions and best practices
4. **Comprehensive Reports**: Provides detailed upgrade recommendations with priorities

#### Usage Examples

```bash
# Full stack review
/technology-review: focus_area=Full stack review, priority=Security updates

# Python-specific review
/technology-review: focus_area=Python dependencies, priority=General modernization

# Framework updates
/technology-review: focus_area=Flask framework, priority=Performance improvements
```

#### Review Areas Covered

- **Dependencies**: Package versions, security patches, compatibility
- **Language Features**: Modern Python syntax, deprecated functions, type annotations
- **Framework Updates**: Flask, extensions, configuration improvements
- **Security**: Vulnerability assessments, patch status, best practices
- **Performance**: Optimization opportunities, benchmarks, efficiency gains
- **Development Tools**: IDE support, linting, testing framework updates

## Advanced Features

### Auto-Approval Settings

The project includes smart auto-approval configurations:

#### File Edit Approvals

```json
{
  "**/*": true, // Auto-approve most files
  "**/.vscode/*.json": false, // Require approval for VS Code settings
  "**/.env*": false, // Require approval for environment files
  "**/secrets/**": false // Require approval for secrets
}
```

#### Terminal Command Approvals

```json
{
  "pytest": true, // Auto-approve test runs
  "black": true, // Auto-approve formatting
  "mypy": true, // Auto-approve type checking
  "/^git (status|log|show)$/": true, // Auto-approve safe git commands
  "rm": false, // Require approval for deletions
  "sudo": false // Require approval for sudo commands
}
```

### Checkpoints and Recovery

- **Checkpoints Enabled** - Automatically save workspace state before major changes
- **Revert Capability** - Easily rollback to previous stable states
- **Change Tracking** - Monitor all AI-generated modifications

### Todo List Integration

- **Experimental Feature** - Track progress of complex tasks
- **Agent Coordination** - Maintain focus on overall goals
- **Progress Visibility** - See task completion status

## Best Practices

### 1. Start Simple, Build Complexity

```bash
# Good: Start with high-level requirements
"Add user authentication to the Flask app"

# Better: Provide specific context
"Add OAuth 2.0 authentication using Flask-Login, with user registration, login/logout endpoints, and proper session management"
```

### 2. Use Appropriate Chat Modes

- **Ask Mode** - Questions about existing code
- **Edit Mode** - Specific file modifications with context
- **Agent Mode** - Complex multi-file tasks and autonomous development

### 3. Leverage Context

```bash
# Reference specific files
"Update the user service in src/goldilocks/services/auth.py to include password reset functionality"

# Reference instruction files
"Follow the security guidelines in .github/instructions/python.instructions.md when implementing this feature"
```

### 4. Iterative Development

1. Start with agent mode for initial implementation
2. Use edit mode for refinements
3. Apply prompt files for standardized tasks
4. Use tool sets for focused operations

### 5. Quality Assurance

- Always review AI-generated code before accepting
- Run tests after accepting changes (`/runTasks`)
- Use security review prompt for sensitive code
- Maintain manual oversight of architectural decisions

## Troubleshooting

### Common Issues

1. **Tool Limit Exceeded**: Reduce selected tools or enable virtual tools
2. **Approval Required**: Check auto-approval settings for specific commands
3. **Context Missing**: Use `#codebase` tool to provide broader context
4. **Instructions Not Applied**: Verify file patterns in instruction frontmatter

### Getting Help

1. Use the `/help` command in chat
2. Reference the [VS Code Copilot documentation](https://code.visualstudio.com/docs/copilot/)
3. Check the `.vscode/settings.json` for current configurations
4. Review the AGENTS.md file for comprehensive guidelines

## Continuous Improvement

The Copilot configuration will evolve with the project. Regularly:

1. Review and update instruction files
2. Refine prompt files based on usage patterns
3. Adjust tool sets for optimal workflows
4. Update AGENTS.md with new practices
5. Optimize auto-approval settings based on experience

---

This comprehensive setup transforms Goldilocks development into an AI-enhanced workflow that maintains high code quality while dramatically improving development velocity and consistency.
