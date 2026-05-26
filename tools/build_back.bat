@echo off

python --version >nul 2>&1
if errorlevel 1 (
    echo Python n'est pas installe !
    pause
    exit
)

set SCRIPT="../game/main.py"
set EXE=Nifhleim
set ASSETS="../game/assets;assets"
set JSON="../game/client/ui/json;client/ui/json"

pip install -r requirement.txt

python -m PyInstaller --onefile --windowed --name %EXE% ^
    --add-data "%ASSETS%" ^
    --add-data "%JSON%" ^
    %SCRIPT%

move dist\Nifhleim.exe ..\

pause