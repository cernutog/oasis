@echo off
REM OASIS Release Build Script - BUILDS WITHOUT INCREMENTING VERSION
REM Use this for official stable releases (e.g., 2.0, 2.1) where version is set manually.

echo.
echo ============================================
echo  OASIS STABLE RELEASE BUILD
echo ============================================
echo.

REM Step 1: Read current version for display
for /f %%i in ('python -c "from src.version import FULL_VERSION; print(FULL_VERSION)"') do set FULL_VER=%%i
echo   Target Version: %FULL_VER%
echo.

REM Step 2: Build the executable
echo Building executable...
set TCL_LIBRARY=C:\Users\giuse\AppData\Local\Programs\Python\Python313\tcl\tcl8.6
set TK_LIBRARY=C:\Users\giuse\AppData\Local\Programs\Python\Python313\tcl\tk8.6
.venv\Scripts\python -m PyInstaller OASIS.spec
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed!
    exit /b %errorlevel%
)

echo.
echo ============================================
echo  Release Build SUCCESSFUL!
echo  Version: %FULL_VER%
echo  Output: dist\OASIS.exe
echo ============================================
echo.
