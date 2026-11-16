# AERIS AI - PowerShell Launcher
Write-Host "========================================================" -ForegroundColor DarkGreen
Write-Host "  AERIS AI - Intelligent Air Quality Assistant" -ForegroundColor Green
Write-Host "  Understand Your Air. Breathe Smarter." -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor DarkGreen
Set-Location -Path $PSScriptRoot
Write-Host "`nLaunching AERIS AI application..." -ForegroundColor Yellow
python -m streamlit run app.py
