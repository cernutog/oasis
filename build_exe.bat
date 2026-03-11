@echo off
REM OASIS Build Script - Auto-increments BUILD_NUMBER before building

echo.
echo ============================================
echo  OASIS EXE Build Process
echo ============================================
echo.

REM Step 0: Kill running instances
echo Step 0: Killing running instances...
taskkill /F /IM OASIS.exe /T 2>nul
taskkill /F /IM OAS_Generation.exe /T 2>nul

REM Step 1: Increment BUILD_NUMBER in version.py
echo Step 1: Incrementing build number...
call .venv\Scripts\python bin\manage_version.py increment
if %errorlevel% neq 0 (
    echo ERROR: Failed to increment build number!
    exit /b 1
)

REM Step 2: Read new version for display
call .venv\Scripts\python bin\manage_version.py get > temp_ver.txt
set /p FULL_VER=<temp_ver.txt
del temp_ver.txt
echo   Full version: %FULL_VER%
echo.

REM Step 3: Build the executable
echo Step 2: Building executable...
set TCL_LIBRARY=C:\Users\giuse\AppData\Local\Programs\Python\Python313\tcl\tcl8.6
set TK_LIBRARY=C:\Users\giuse\AppData\Local\Programs\Python\Python313\tcl\tk8.6
call .venv\Scripts\python -m PyInstaller OASIS.spec
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed!
    exit /b %errorlevel%
)

echo.
echo ============================================
echo  Build SUCCESSFUL!
echo  Version: %FULL_VER%
echo  Output: dist\OASIS.exe
echo ============================================
echo.
echo  MANDATORY: COMMIT YOUR CHANGES NOW!
echo  -----------------------------------
echo  git add .
echo  git commit -m "Build v%FULL_VER%: <Description>"
echo.
echo ============================================
echo.
