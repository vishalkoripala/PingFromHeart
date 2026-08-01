@echo off
REM Build a single-file Windows executable using PyInstaller
REM Usage: run this in the project folder after installing requirements
pyinstaller --onefile --windowed --name AuraLove love.py

echo Build finished. Check the `dist` folder for AuraLove.exe
pause
