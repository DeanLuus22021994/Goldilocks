#!/bin/bash

# VS Code Server Extensions Verification Script
# This script checks if the GitHub Copilot extensions are properly provisioned

set -e

echo "=== Checking VS Code Server Extensions ==="
echo

# Check extensions directory
if [ -d "/root/.vscode-server-insiders/extensions" ]; then
  echo "✅ VS Code Server extensions directory exists"

  # List installed extensions
  echo "Installed extensions:"
  ls -la /root/.vscode-server-insiders/extensions/

  # Check for specific extensions
  if [ -d "/root/.vscode-server-insiders/extensions/github.copilot" ]; then
    echo "✅ GitHub Copilot extension is installed"
  else
    echo "❌ GitHub Copilot extension is missing"
  fi

  if [ -d "/root/.vscode-server-insiders/extensions/github.copilot-chat" ]; then
    echo "✅ GitHub Copilot Chat extension is installed"
  else
    echo "❌ GitHub Copilot Chat extension is missing"
  fi

  if [ -d "/root/.vscode-server-insiders/extensions/github.vscode-pull-request-github" ]; then
    echo "✅ GitHub Pull Request extension is installed"
  else
    echo "❌ GitHub Pull Request extension is missing"
  fi
else
  echo "❌ VS Code Server extensions directory not found"
fi

# Check extensions.json
if [ -f "/root/.vscode-server-insiders/extensions/extensions.json" ]; then
  echo "✅ extensions.json exists"
  echo "Content:"
  cat /root/.vscode-server-insiders/extensions/extensions.json

  # Validate JSON format
  if jq . /root/.vscode-server-insiders/extensions/extensions.json > /dev/null 2>&1; then
    echo "✅ extensions.json has valid JSON format"
  else
    echo "❌ extensions.json has invalid JSON format"
  fi
else
  echo "❌ extensions.json not found"
fi

# Check settings
if [ -f "/root/.vscode-server-insiders/data/Machine/settings.json" ]; then
  echo "✅ settings.json exists"
  echo "Content:"
  cat /root/.vscode-server-insiders/data/Machine/settings.json
else
  echo "❌ settings.json not found"
fi

echo
echo "=== VS Code Server Extensions check completed ==="
