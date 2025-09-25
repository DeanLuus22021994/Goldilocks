# VS Code Extensions & MCP Servers

## Overview

Goldilocks no longer provisions Visual Studio Code extensions or Model Context Protocol (MCP) servers inside Docker containers. Every developer now manages editor tooling directly through the standard VS Code marketplace. This keeps the project lightweight, easy to maintain, and aligned with the **SEPARATION OF CONCERNS** principle from the Copilot instructions.

## Getting Started

- Install GitHub Copilot, Copilot Chat, and any other extensions from within VS Code.
- When working inside the Dev Container, declare preferred extensions in `devcontainer.json` under `customizations.vscode.extensions`. VS Code handles the installation automatically on attach.
- Use VS Code Settings Sync (GitHub or Microsoft account) if you want a consistent setup across machines.

### Recommended Dev Container Snippet

```jsonc
"customizations": {
  "vscode": {
    "extensions": [
      "github.copilot",
      "github.copilot-chat"
    ]
  }
}
```

Add or remove extension identifiers to match your workflow. The Dev Container never ships with preinstalled marketplace content, so this list is the single source of truth.

## MCP Servers

MCP servers were previously provisioned alongside Copilot extensions. They are no longer bundled with the container image. If your workflow still needs an MCP server, install and configure it locally through the VS Code marketplace or follow the vendor’s installation guide.

## Retirement of Custom Provisioning

The former `goldilocks-extensions` Docker service, provisioning scripts, and Dockerfile layers have been removed. The pipeline now focuses solely on running the Flask application. Benefits:

- **Simplicity:** No bespoke scripts to maintain or debug.
- **Flexibility:** Each contributor can decide which tools to install.
- **Security:** Marketplace downloads remain signed and up to date.
- **Compatibility:** Works with both local VS Code installs and the Dev Container.

## Legacy Cleanup (Optional)

If you previously ran the deprecated provisioning workflow, you might have residual Docker volumes. Remove them to free disk space:

```bash
docker volume rm goldilocks_vscode_server_extensions || true
docker volume rm goldilocks_vscode_server_data || true
```

No further action is required—VS Code will handle extensions the next time you attach to the container.

## Troubleshooting

- **Extensions not installing in the Dev Container?** Re-open the folder in container and confirm the extensions are listed under `customizations.vscode.extensions`.
- **Need to share a standard set of tools?** Document the recommended marketplace IDs in the project README or team handbook rather than baking them into container images.
- **Unsure which extensions to use?** Start with the snippet above and add extras as needed—VS Code installations remain isolated per-user.

For more details on Dev Container customization, read the official [VS Code documentation](https://code.visualstudio.com/docs/devcontainers/containers#_creating-a-devcontainerjson-file).
Refer to `docs/SETUP.md` for Dev Container usage instructions or reach out to the team if you encounter marketplace installation issues.

## Docker Host Communication
