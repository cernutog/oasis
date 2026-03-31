@echo off
setlocal

echo ==============================================================================
echo  Launching OASIS - OAS Integration Suite
echo ==============================================================================
echo.

if exist ".venv\Scripts\python.exe" goto launch
echo [ERROR] Virtual environment (.venv) not found!
echo Please run 'setup_oasis.bat' first to install dependencies.
echo.
pause
exit /b 1

:launch
echo [INFO] Using virtual environment: .venv
echo.
".venv\Scripts\python.exe" run_gui.py

if ERRORLEVEL 1 goto crash
goto end

:crash
echo.
echo [CRITICAL] Application crashed with exit code %ERRORLEVEL%
echo Check the error messages above for more details.
echo.
pause

:end
endlocal
