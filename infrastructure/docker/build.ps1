# Optimized build script for Goldilocks using Docker Bake
# PowerShell version for Windows with SSD performance optimization

param(
  [string]$Target = "default",
  [switch]$NoCache = $false,
  [switch]$Verbose = $false
)

Write-Host "🏗️  Building Goldilocks with Docker Bake (optimized for SSD performance)..." -ForegroundColor Blue

# Enable Docker BuildKit with advanced features
$env:DOCKER_BUILDKIT = "1"
$env:BUILDKIT_PROGRESS = "plain"
$env:BUILDX_NO_DEFAULT_ATTESTATIONS = "1"

# Change to project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path "$scriptDir\..\.."
Set-Location $projectRoot

# Create cache directories for maximum performance
Write-Host "📁 Setting up cache directories..." -ForegroundColor Green
$cacheDirectories = @(
  "$env:TEMP\.buildx-cache-builder",
  "$env:TEMP\.buildx-cache-tools",
  "$env:TEMP\.buildx-cache-runtime",
  "$env:TEMP\.buildx-cache-production",
  "$env:TEMP\.buildx-cache-devcontainer",
  "$env:TEMP\goldilocks-venv",
  "$env:TEMP\goldilocks-node-modules",
  "$env:TEMP\goldilocks-bytecode",
  "$env:TEMP\goldilocks-build-cache",
  "$env:TEMP\pip-cache",
  "$env:TEMP\npm-cache",
  "$env:TEMP\pre-commit-cache",
  "$env:TEMP\mypy-cache",
  "$env:TEMP\pytest-cache",
  "$env:TEMP\ruff-cache",
  "$env:TEMP\buildx-cache"
)

foreach ($dir in $cacheDirectories) {
  if (!(Test-Path $dir)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
  }
}

# Initialize buildx builder with advanced features
Write-Host "🔧 Setting up buildx builder..." -ForegroundColor Green
try {
  docker buildx create --name goldilocks-builder --driver docker-container --use --bootstrap 2>$null
} catch {
  docker buildx use goldilocks-builder 2>$null
}

# Build arguments
$buildArgs = @()
if ($NoCache) {
  $buildArgs += "--no-cache"
}
if ($Verbose) {
  $buildArgs += "--progress=plain"
}

function Invoke-BuildTarget {
  param([string]$TargetName, [string]$Description)

  Write-Host "🚀 $Description..." -ForegroundColor Green

  $dockerCmd = @("docker", "buildx", "bake", "-f", "docker-bake.json", $TargetName, "--load") + $buildArgs

  & $dockerCmd[0] $dockerCmd[1..($dockerCmd.Length - 1)]
  if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to build $TargetName"
    exit 1
  }
}

# Target selection with optimized build order
switch ($Target.ToLower()) {
  "dev" {
    Invoke-BuildTarget "development" "Building development environment"
  }
  "development" {
    Invoke-BuildTarget "development" "Building development environment"
  }
  "prod" {
    Invoke-BuildTarget "production" "Building production environment"
  }
  "production" {
    Invoke-BuildTarget "production" "Building production environment"
  }
  "builder" {
    Invoke-BuildTarget "builder" "Building base builder stage"
  }
  "tools" {
    Invoke-BuildTarget "tools" "Building tools stage"
  }
  "runtime" {
    Invoke-BuildTarget "runtime" "Building runtime stage"
  }
  "devcontainer" {
    Invoke-BuildTarget "devcontainer" "Building devcontainer"
  }
  "all" {
    Invoke-BuildTarget "default" "Building all targets with maximum cache optimization"
  }
  "default" {
    Invoke-BuildTarget "default" "Building all targets with maximum cache optimization"
  }
  default {
    Write-Error "Invalid target: $Target. Valid options are: dev, prod, builder, tools, runtime, devcontainer, all, default"
    exit 1
  }
}

# Show cache usage statistics
Write-Host ""
Write-Host "📊 Build cache statistics:" -ForegroundColor Yellow
foreach ($dir in $cacheDirectories) {
  if (Test-Path $dir) {
    $size = (Get-ChildItem $dir -Recurse -File | Measure-Object -Property Length -Sum).Sum
    $sizeGB = [math]::Round($size / 1GB, 2)
    Write-Host "  $(Split-Path $dir -Leaf): $sizeGB GB" -ForegroundColor Gray
  }
}

Write-Host ""
Write-Host "📊 Docker images built:" -ForegroundColor Yellow
docker images | Select-String "goldilocks"

Write-Host ""
Write-Host "✅ Optimized multi-stage build complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Usage:" -ForegroundColor Cyan
Write-Host "  Development: docker-compose --profile dev up" -ForegroundColor Gray
Write-Host "  Production:  docker-compose --profile prod up" -ForegroundColor Gray
Write-Host "  Build only:  docker-compose --profile build up" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Subsequent builds will be near-instant thanks to cache optimization!" -ForegroundColor Magenta
