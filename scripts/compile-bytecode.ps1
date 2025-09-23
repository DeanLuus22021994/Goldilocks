# Simple Python bytecode compilation script for Windows
Write-Host "Compiling Python bytecode..." -ForegroundColor Green
$env:PYTHONOPTIMIZE = "2"
python -m compileall -b src/
$pyFiles = (Get-ChildItem -Path src -Recurse -Filter "*.py").Count
$pycFiles = (Get-ChildItem -Path src -Recurse -Filter "*.pyc").Count
Write-Host "Complete! Python files: $pyFiles, Bytecode files: $pycFiles" -ForegroundColor Yellow
