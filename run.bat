@echo off
title Journey of Mankind (Audio Survival Game)
cd /d "%~dp0"
python main.py
if errorlevel 1 (
    echo.
    echo Game run karne mein masla hua.
    pause
)
