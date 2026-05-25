@echo off
set SCRIPT="../main.py"
set EXE=Nifleym
set ASSETS="../assets;assets"
set JSON="../client/ui/json;client/ui/json"

python -m PyInstaller --onefile --windowed --name %EXE% ^
    --add-data "%ASSETS%" ^
    --add-data "%JSON%" ^
    %SCRIPT%
pause