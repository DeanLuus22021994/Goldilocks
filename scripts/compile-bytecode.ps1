# Python bytecode precompilation script (PowerShell version)
# Compiles Python files to optimized bytecode for faster startup

param(
  [switch]$Force = $false,
  [int]$OptimizeLevel = 2,
  [string]$SrcDir = "src",
  [switch]$Help = $false
)

if ($Help) {
  Write-Host "Usage: compile-bytecode.ps1 [OPTIONS]" -ForegroundColor Cyan
  Write-Host "Options:" -ForegroundColor Yellow
  Write-Host "  -Force           Force recompilation of all files"
  Write-Host "  -OptimizeLevel   Optimization level (0, 1, or 2, default: 2)"
  Write-Host "  -SrcDir          Source directory (default: src)"
  Write-Host "  -Help            Show this help message"
  exit 0
}

Write-Host "🐍 Precompiling Python bytecode..." -ForegroundColor Blue

# Validate optimization level
if ($OptimizeLevel -notin @(0, 1, 2)) {
  Write-Error "Optimization level must be 0, 1, or 2"
  exit 1
}

# Check if source directory exists
if (-not (Test-Path $SrcDir)) {
  Write-Error "Source directory '$SrcDir' does not exist"
  exit 1
}

# Remove old bytecode if force recompile
if ($Force) {
  Write-Host "🧹 Cleaning old bytecode files..." -ForegroundColor Yellow
  Get-ChildItem -Path $SrcDir -Recurse -Name "*.pyc" | Remove-Item -Force
  Get-ChildItem -Path $SrcDir -Recurse -Directory -Name "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

# Set optimization environment variable
$env:PYTHONOPTIMIZE = $OptimizeLevel

Write-Host "📦 Compiling Python files in $SrcDir (optimization level: $OptimizeLevel)..." -ForegroundColor Green

# Compile Python files to bytecode
$compileArgs = @(
  "-m", "compileall",
  "-b",
  "-f",
  "--invalidation-mode", "unchecked-hash",
  $SrcDir
)

try {
  & python @compileArgs
  if ($LASTEXITCODE -ne 0) {
    throw "Python compilation failed"
  }
} catch {
  Write-Error "Failed to compile Python bytecode: $_"
  exit 1
}

# Count compiled files
$pyFileCount = (Get-ChildItem -Path $SrcDir -Recurse -Filter "*.py").Count
$pycFileCount = (Get-ChildItem -Path $SrcDir -Recurse -Filter "*.pyc").Count

Write-Host "✅ Bytecode compilation complete!" -ForegroundColor Green
Write-Host "📊 Statistics:" -ForegroundColor Cyan
Write-Host "  - Python files: $pyFileCount" -ForegroundColor Gray
Write-Host "  - Bytecode files: $pycFileCount" -ForegroundColor Gray
Write-Host "  - Optimization level: $OptimizeLevel" -ForegroundColor Gray

# Create __pycache__ directory if it doesn't exist
$cacheDir = "__pycache__"
if (-not (Test-Path $cacheDir)) {
  New-Item -ItemType Directory -Path $cacheDir -Force | Out-Null
}

# Create bytecode manifest for caching
$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss.fffZ" -AsUTC
$pythonVersion = (python --version 2>&1).Split(" ")[1]

$pycFiles = Get-ChildItem -Path $SrcDir -Recurse -Filter "*.pyc"
$filesObject = @{}
foreach ($file in $pycFiles) {
  $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
  $filesObject[$baseName] = $true
}

$manifest = @{
  generated          = $timestamp
  optimization_level = $OptimizeLevel
  source_directory   = $SrcDir
  python_version     = $pythonVersion
  files              = $filesObject
}

$manifest | ConvertTo-Json -Depth 3 | Set-Content "$cacheDir/manifest.json" -Encoding UTF8

Write-Host "📝 Created bytecode manifest" -ForegroundColor Green
Write-Host "🎉 Python bytecode precompilation complete!" -ForegroundColor Magenta
Write-Host "💡 To use bytecode-only mode, set PYTHONOPTIMIZE=$OptimizeLevel and remove .py files" -ForegroundColor Yellow
