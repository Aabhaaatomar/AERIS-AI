@echo off
title AERIS AI - Intelligent Air Quality Assistant
color 0A
echo ========================================================
echo   AERIS AI - Intelligent Air Quality Assistant
echo   Understand Your Air. Breathe Smarter.
echo ========================================================
echo.
echo Launching AERIS AI Dashboard in your browser...
cd /d "%~dp0"
python -m streamlit run app.py
pause
