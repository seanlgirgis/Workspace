$venvPath = "C:\py_venv\proj_educate"
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

# 3. Check and Activate
if (Test-Path $activateScript) {
    # Set execution policy for this session only to allow the script to run
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
    
    & $activateScript
    Write-Host "--- Project Educate Environment ---" -ForegroundColor Yellow
    Write-Host "Status: Virtual environment activated" -ForegroundColor Green
    Write-Host "Venv Path: $venvPath" -ForegroundColor Gray
    Write-Host "Python: $(Get-Command python | Select-Object -ExpandProperty Source)" -ForegroundColor Cyan
}
else {
    Write-Host "Error: Activation script not found at $activateScript" -ForegroundColor Red
}