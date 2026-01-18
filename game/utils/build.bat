@echo off
set SCRIPT="../main.py"
set EXE=Nifleym
set ASSETS="../assets;assets"

python -m PyInstaller --onefile --windowed --name %EXE% --add-data "%ASSETS%" %SCRIPT%
pause