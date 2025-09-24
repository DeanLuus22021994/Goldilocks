# Devcontainer lock file generator and cache manager (PowerShell version)
# This script creates and updates devcontainer-lock.json for build reproducibility

$LockFile = ".devcontainer/devcontainer-lock.json"

Write-Host "🔒 Generating devcontainer lock file..." -ForegroundColor Blue

# Function to compute SHA256 hash of a file
function Get-FileHash256 {
  param([string]$Path)
  if (Test-Path $Path) {
    return (Get-FileHash -Path $Path -Algorithm SHA256).Hash.ToLower()
  }
  return ""
}

# Function to compute SHA256 hash of a string
function Get-StringHash256 {
  param([string]$String)
  $hasher = [System.Security.Cryptography.SHA256]::Create()
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($String)
  $hash = $hasher.ComputeHash($bytes)
  return [System.BitConverter]::ToString($hash).Replace("-", "").ToLower()
}

# Get current timestamp
$Timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss.fffZ" -AsUTC

# Read current devcontainer.json
$DevContainerHash = Get-FileHash256 ".devcontainer/devcontainer.json"

# Get requirements.txt hash
$RequirementsHash = Get-FileHash256 "requirements.txt"

# Get package.json hash
$PackageJsonHash = Get-FileHash256 "package.json"

# Get Python packages from requirements.txt
$PythonPackages = @{}
if (Test-Path "requirements.txt") {
  Get-Content "requirements.txt" | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith("#") -and -not $line.StartsWith("-")) {
      if ($line.Contains("==")) {
        $parts = $line.Split("==", 2)
        $PythonPackages[$parts[0].Trim()] = $parts[1].Trim()
      } elseif ($line) {
        $PythonPackages[$line] = "latest"
      }
    }
  }
}

# Get Node packages from package.json
$NodePackages = @{}
if (Test-Path "package.json") {
  try {
    $packageJson = Get-Content "package.json" | ConvertFrom-Json
    if ($packageJson.dependencies) {
      $packageJson.dependencies.PSObject.Properties | ForEach-Object {
        $NodePackages[$_.Name] = $_.Value
      }
    }
    if ($packageJson.devDependencies) {
      $packageJson.devDependencies.PSObject.Properties | ForEach-Object {
        $NodePackages[$_.Name] = $_.Value
      }
    }
  } catch {
    Write-Warning "Could not parse package.json"
  }
}

# Get Python version
$PythonVersion = "unknown"
try {
  $PythonVersion = (python --version 2>&1).Split(" ")[1]
} catch {
  try {
    $PythonVersion = (python3 --version 2>&1).Split(" ")[1]
  } catch {
    Write-Warning "Python not found"
  }
}

# Get pip version
$PipVersion = "unknown"
try {
  $PipVersion = (pip --version 2>&1).Split(" ")[1]
} catch {
  Write-Warning "Pip not found"
}

# Get Node version
$NodeVersion = "not-installed"
try {
  $NodeVersion = (node --version 2>&1).Substring(1)
} catch {
  Write-Warning "Node.js not found"
}

# Get npm version
$NpmVersion = "not-installed"
try {
  $NpmVersion = npm --version 2>&1
} catch {
  Write-Warning "npm not found"
}

# Get Docker version
$DockerVersion = "unknown"
try {
  $DockerVersion = (docker --version 2>&1) -replace "Docker version ([0-9.]+).*", '$1'
} catch {
  Write-Warning "Docker not found"
}

# Get OS type
$OSType = [System.Environment]::OSVersion.Platform

# Create the lock file content
$LockContent = @{
  '$schema'  = "https://json-schema.org/draft-07/schema"
  version    = "1.0.0"
  generated  = $Timestamp
  lockfile   = @{
    devcontainer = @{
      hash     = $DevContainerHash
      image    = "mcr.microsoft.com/devcontainers/python:1-3.14.0-trixie"
      features = @{
        node = @{
          version = "22"
          hash    = "sha256:placeholder"
        }
      }
    }
    python       = @{
      version           = $PythonVersion
      pip               = @{
        version = $PipVersion
        hash    = "sha256:placeholder"
      }
      packages          = $PythonPackages
      requirements_hash = $RequirementsHash
    }
    node         = @{
      version           = $NodeVersion
      npm               = @{
        version = $NpmVersion
        hash    = "sha256:placeholder"
      }
      packages          = $NodePackages
      package_json_hash = $PackageJsonHash
    }
    system       = @{
      base_image   = "mcr.microsoft.com/devcontainers/python:1-3.13-bookworm"
      base_hash    = "sha256:placeholder"
      apt_packages = @()
      cache_paths  = @(
        "/home/vscode/.cache/pip",
        "/home/vscode/.npm",
        "/home/vscode/.cache/uv",
        "/home/vscode/.vscode-server",
        "/home/vscode/.vscode-server/extensions"
      )
    }
  }
  cache      = @{
    volumes = @{
      "goldilocks-venv"         = @{
        created        = $Timestamp
        size           = "unknown"
        python_version = $PythonVersion
      }
      "goldilocks-node-modules" = @{
        created      = $Timestamp
        size         = "unknown"
        node_version = $NodeVersion
      }
      "goldilocks-bytecode"     = @{
        created         = $Timestamp
        size            = "unknown"
        python_optimize = 2
      }
      "pip-cache"               = @{
        created = $Timestamp
        size    = "unknown"
      }
      "npm-cache"               = @{
        created = $Timestamp
        size    = "unknown"
      }
    }
  }
  build_info = @{
    os             = $OSType.ToString()
    docker_version = $DockerVersion
    build_time     = $Timestamp
    cache_hit_rate = 0
  }
}

# Convert to JSON and save
$LockContent | ConvertTo-Json -Depth 10 | Set-Content -Path $LockFile -Encoding UTF8

Write-Host "✅ Lock file generated: $LockFile" -ForegroundColor Green
Write-Host "🔍 Summary:" -ForegroundColor Cyan
Write-Host "  - DevContainer hash: $DevContainerHash" -ForegroundColor Gray
Write-Host "  - Requirements hash: $RequirementsHash" -ForegroundColor Gray
Write-Host "  - Package.json hash: $PackageJsonHash" -ForegroundColor Gray
Write-Host "  - Python version: $PythonVersion" -ForegroundColor Gray
Write-Host "  - Node version: $NodeVersion" -ForegroundColor Gray
