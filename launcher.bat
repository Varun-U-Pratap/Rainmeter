@echo off
cd /d "%~dp0"

REM ----------------------------------------------------------------
REM MODULAR LAUNCHER - SILENT MODE
REM ----------------------------------------------------------------

REM 1. Try 'py' launcher (Best for avoiding popups)
py -w stats.py >nul 2>&1
if %ERRORLEVEL% EQU 0 exit /b

REM 2. Try 'pythonw' (Standard silent python)
REM If this fails, we simply EXIT. We do NOT run 'python' (console mode)
REM because that causes the "App Installer" popup when offline.
pythonw stats.py >nul 2>&1

exit /b