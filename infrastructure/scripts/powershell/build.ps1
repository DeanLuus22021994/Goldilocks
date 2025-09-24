# Optimized build script for Goldilocks using Docker Buildx
# PowerShell version with maximum cache efficiency for instant subsequent builds

param(
  [string]$Target = "all",
  [switch]$NoCache = $false,
  [switch]$Verbose = $false
)

Write-Host "🏗️ Building Goldilocks with maximum cache optimization..." -ForegroundColor Blue

# Enable Docker BuildKit with advanced features
$env:DOCKER_BUILDKIT = "1"
$env:BUILDKIT_PROGRESS = if ($Verbose) { "plain" } else { "auto" }
$env:BUILDX_NO_DEFAULT_ATTESTATIONS = "1"

# Change to project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path "$scriptDir\..\..\..\"
Set-Location $projectRoot

# Setup cache directories for instant subsequent builds
Write-Host "📁 Setting up cache directories for maximum performance..." -ForegroundColor Green
$cacheDirectories = @(
  "$env:TEMP\goldilocks-cache\buildx",
  "$env:TEMP\goldilocks-cache\pip",
  "$env:TEMP\goldilocks-cache\npm",
  "$env:TEMP\goldilocks-cache\pre-commit",
  "$env:TEMP\goldilocks-cache\mypy",
  "$env:TEMP\goldilocks-cache\pytest",
  "$env:TEMP\goldilocks-cache\ruff"
)

foreach ($dir in $cacheDirectories) {
  if (!(Test-Path $dir)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
  }
}

# Create buildx builder with advanced features
Write-Host "🔧 Setting up buildx builder..." -ForegroundColor Green
try {
  docker buildx create --name goldilocks-builder --driver docker-container --use --bootstrap 2>$null
} catch {
  docker buildx use goldilocks-builder 2>$null
}

# Build function with aggressive caching
function Build-Image {
  param([string]$Target, [string]$Tag, [string]$Description)

  Write-Host "🚀 $Description..." -ForegroundColor Green

  $buildArgs = @(
    "docker", "buildx", "build",
    "--target", $Target,
    "--tag", "goldilocks:$Tag",
    "--file", "infrastructure\docker\dockerfiles\Dockerfile.multi-stage",
    "--cache-from", "type=local,src=$env:TEMP\goldilocks-cache\buildx",
    "--cache-to", "type=local,dest=$env:TEMP\goldilocks-cache\buildx,mode=max",
    "--load",
    "."
  )

  if ($NoCache) {
    $buildArgs += "--no-cache"
  }

  & $buildArgs[0] $buildArgs[1..($buildArgs.Length - 1)]
  if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to build $Tag"
    exit 1
  }
}

# Build target selection
switch ($Target.ToLower()) {
  { $_ -in @("builder", "build") } {
    Build-Image "builder" "builder" "Building base builder stage"
  }
  { $_ -in @("tools", "dev", "development") } {
    Build-Image "devcontainer" "devcontainer" "Building development environment"
  }
  { $_ -in @("runtime", "prod", "production") } {
    Build-Image "runtime" "runtime" "Building production runtime"
    Build-Image "production" "production" "Building production image"
  }
  "devcontainer" {
    Build-Image "devcontainer" "devcontainer" "Building devcontainer"
  }
  { $_ -in @("all", "default") } {
    Build-Image "builder" "builder" "Building base builder"
    Build-Image "devcontainer" "devcontainer" "Building development tools"
    Build-Image "runtime" "runtime" "Building production runtime"
  }
  default {
    Write-Error "Invalid target: $Target. Valid options are: builder, dev, prod, devcontainer, all"
    exit 1
  }
}

Write-Host ""
Write-Host "📊 Build complete! Images created:" -ForegroundColor Yellow
docker images | findstr goldilocks
Write-Host ""
Write-Host "💡 Subsequent builds will be near-instant thanks to aggressive caching!" -ForegroundColor Magenta
