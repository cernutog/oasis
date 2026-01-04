@echo off
echo Building OASIS Executable...
set TCL_LIBRARY=C:\Users\giuse\AppData\Local\Programs\Python\Python313\tcl\tcl8.6
set TK_LIBRARY=C:\Users\giuse\AppData\Local\Programs\Python\Python313\tcl\tk8.6
.venv\Scripts\python -m PyInstaller OASIS.spec
if %errorlevel% neq 0 (
    echo Build failed!
    exit /b %errorlevel%
)
echo Build successful! Executable is in dist/
