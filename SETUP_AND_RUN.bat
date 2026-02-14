@echo off
title GlowMiniAI Launcher

echo ====================================
echo   GlowMiniAI Portable Launcher
echo ====================================
echo.

cd /d %~dp0

echo Checking Python...
python --version
echo.

echo Installing dependencies...
python -m pip install -r requirements.txt
echo.

echo Starting GlowMiniAI...
python -m streamlit run app.py

pause