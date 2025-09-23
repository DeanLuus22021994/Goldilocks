# Build script for Goldilocks multi-stage Docker architecture
# PowerShell version for Windows

param(
  [string]$Stage = "all",
  [switch]$NoCache = $false
)

Write-Host "🏗️  Building Goldilocks multi-stage Docker architecture..." -ForegroundColor Blue

# Enable Docker BuildKit for better caching
$env:DOCKER_BUILDKIT = "1"

# Build arguments for caching
$buildArgs = @("--build-arg", "BUILDKIT_INLINE_CACHE=1")
if ($NoCache) {
  $buildArgs += "--no-cache"
}

# Change to project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path "$scriptDir\..\.."
Set-Location $projectRoot

function Build-Stage {
  param(
    [string]$StageName,
    [string]$DockerFile,
    [string]$Target,
    [string[]]$CacheFrom
  )

  Write-Host "📦 Building stage: $StageName..." -ForegroundColor Green

  $dockerCmd = @("docker", "build") + $buildArgs
  $dockerCmd += "--target", $Target
  $dockerCmd += "--tag", "goldilocks:$Target"
  $dockerCmd += "--file", $DockerFile

  foreach ($cache in $CacheFrom) {
    $dockerCmd += "--cache-from", $cache
  }

  $dockerCmd += "."

  & $dockerCmd
  if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to build $StageName"
    exit 1
  }
}

# Build stages
switch ($Stage.ToLower()) {
  "builder" {
    Build-Stage "Builder" "infrastructure/docker/build.Dockerfile" "builder" @("goldilocks:builder")
  }
  "tools" {
    Build-Stage "Tools" "infrastructure/docker/tools.Dockerfile" "tools" @("goldilocks:builder", "goldilocks:tools")
  }
  "runtime" {
    Build-Stage "Runtime" "infrastructure/docker/runtime.Dockerfile" "runtime" @("goldilocks:builder", "goldilocks:runtime")
  }
  "all" {
    Build-Stage "Builder" "infrastructure/docker/build.Dockerfile" "builder" @("goldilocks:builder")
    Build-Stage "Tools" "infrastructure/docker/tools.Dockerfile" "tools" @("goldilocks:builder", "goldilocks:tools")
    Build-Stage "Runtime" "infrastructure/docker/runtime.Dockerfile" "runtime" @("goldilocks:builder", "goldilocks:runtime")
  }
  default {
    Write-Error "Invalid stage: $Stage. Valid options are: builder, tools, runtime, all"
    exit 1
  }
}

Write-Host "📊 Docker images built:" -ForegroundColor Yellow
docker images | Select-String "goldilocks"

Write-Host "✅ Multi-stage build complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Usage:" -ForegroundColor Cyan
Write-Host "  Development: docker-compose --profile dev up" -ForegroundColor Gray
Write-Host "  Production:  docker-compose --profile prod up" -ForegroundColor Gray
Write-Host "  Build only:  docker-compose --profile build up" -ForegroundColor Gray
