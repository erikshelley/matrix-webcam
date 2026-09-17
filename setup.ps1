param(
    [ValidateSet("3.11", "3.12", "3.13")]
    [string]$PythonVersion = "3.13"
)

$ErrorActionPreference = "Stop"

$venvPath = Join-Path $PSScriptRoot ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    & py "-$PythonVersion" -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        throw "Could not create .venv with Python $PythonVersion. Install it, then run this script again."
    }
}

& $venvPython -c "import sys; raise SystemExit(0 if (3, 11) <= sys.version_info[:2] < (3, 14) else 1)"
if ($LASTEXITCODE -ne 0) {
    throw ".venv must use Python 3.11, 3.12, or 3.13. Remove .venv and run this script again."
}

& $venvPython -m pip install -e $PSScriptRoot
if ($LASTEXITCODE -ne 0) {
    throw "Could not install matrix-webcam."
}

Write-Host "Setup complete. Run .\run.ps1 to start matrix-webcam."