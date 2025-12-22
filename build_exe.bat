@echo off
echo Building OAS Generator Executable...
python -m PyInstaller --noconfirm --onefile --windowed --name "OAS_Generation" --clean --collect-all customtkinter --icon "icon.ico" --add-data "icon.ico;." --add-data "src;src" --hidden-import src.generator --hidden-import src.excel_parser run_gui.py
if %errorlevel% neq 0 (
    echo Build failed!
    exit /b %errorlevel%
)
echo Build successful! Executable is in dist/
