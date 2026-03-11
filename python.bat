@echo off
setlocal ENABLEDELAYEDEXPANSION

set "FIRST_ARG=%~1"
set "BLOCK=0"

if /i "!FIRST_ARG!"=="-c" set "BLOCK=1"
if /i "!FIRST_ARG!"=="/-c" set "BLOCK=1"

if "!BLOCK!"=="1" (
    echo.
    echo ==============================================================================
    echo ERRORE CRITICO: L'uso di "python -c" ^(inline execution^) e' PROIBITO.
    echo Protocollo di sicurezza OASIS violato. 
    echo Per favore, scrivi il codice in un file .py ed esegui quello.
    echo ==============================================================================
    echo.
    exit /b 1
)

:: Forward to venv python wrapper
if exist ".venv\Scripts\python.bat" (
    ".venv\Scripts\python.bat" %*
) else (
    python %*
)
