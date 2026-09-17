param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$MatrixWebcamArguments
)

$ErrorActionPreference = "Stop"

$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    throw "Could not find .venv. Run .\setup.ps1 first."
}

Push-Location $PSScriptRoot
try {
    & $venvPython -m matrix_webcam @MatrixWebcamArguments
    exit $LASTEXITCODE
} finally {
    Pop-Location
}