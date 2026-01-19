@echo off
setlocal EnableDelayedExpansion

echo ===========================================
echo   OASIS Environment Setup and Repair Tool
echo ===========================================
echo.

set "VENV_DIR=.venv"
set "VPYTHON=.\.venv\Scripts\python.exe"
set "VPIP=.\.venv\Scripts\pip.exe"

REM ========================================================
REM 1. LOCATE PYTHON 3.13
REM ========================================================
set "PY_CMD="

if exist "C:\Users\giuse\AppData\Local\Programs\Python\Python313\python.exe" (
    set "PY_CMD=C:\Users\giuse\AppData\Local\Programs\Python\Python313\python.exe"
    echo [PYTHON] Found Python 3.13 at known location.
    goto :check_venv
)

python --version >nul 2>&1
if not errorlevel 1 (
    REM Check if global python is 3.13
    python --version 2>&1 | findstr "3.13" >nul
    if not errorlevel 1 (
         set "PY_CMD=python"
         echo [PYTHON] Found Python 3.13 in PATH.
         goto :check_venv
    )
)

if "%PY_CMD%"=="" (
    echo [ERROR] Python 3.13 not found! 
    echo Please install Python 3.13.
    pause
    exit /b 1
)

:check_venv
echo.
REM ========================================================
REM 2. CHECK VIRTUAL ENVIRONMENT INTEGRITY
REM ========================================================
if not exist "%VENV_DIR%" goto :create_venv

echo [VENV] Found existing virtual environment.

REM Check 1: Python Connectivity
"%VPYTHON%" --version >nul 2>&1
if errorlevel 1 (
    echo [WARN] venv python is broken.
    goto :broken_venv
)

REM Check 2: Pip Connectivity
"%VPIP%" --version >nul 2>&1
if errorlevel 1 (
    echo [WARN] venv pip is broken - PATH MISMATCH DETECTED.
    goto :broken_venv
)

echo [OK] venv is valid.
goto :install_deps

:broken_venv
echo [REPAIR] Deleting broken virtual environment...
rmdir /s /q "%VENV_DIR%"
timeout /t 1 >nul

:create_venv
echo [VENV] Creating new virtual environment...
"%PY_CMD%" -m venv "%VENV_DIR%"
if errorlevel 1 (
    echo [ERROR] Failed to create venv.
    pause
    exit /b 1
)
echo [OK] venv created.

:install_deps
echo.
REM ========================================================
REM 3. INSTALL DEPENDENCIES
REM ========================================================
echo [PIP] Installing requirements...
"%VPIP%" install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install requirements.
    pause
    exit /b 1
)

echo.
echo ===========================================
echo   SETUP COMPLETE!
echo ===========================================
echo You can now run build_exe.bat
pause
