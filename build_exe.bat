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
python -c "import re; f=open('src/version.py','r'); c=f.read(); f.close(); m=re.search(r'BUILD_NUMBER\s*=\s*(\d+)',c); old=int(m.group(1)); new=old+1; c=re.sub(r'BUILD_NUMBER\s*=\s*\d+',f'BUILD_NUMBER = {new}',c); f=open('src/version.py','w'); f.write(c); f.close(); print(f'  Build number: {old} -> {new}')"
if %errorlevel% neq 0 (
    echo ERROR: Failed to increment build number!
    exit /b 1
)

REM Step 2: Read new version for display
for /f %%i in ('python -c "from src.version import FULL_VERSION; print(FULL_VERSION)"') do set FULL_VER=%%i
echo   Full version: %FULL_VER%
echo.

REM Step 3: Build the executable
echo Step 2: Building executable...
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
