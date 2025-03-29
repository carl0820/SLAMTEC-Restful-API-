@echo off
chcp 65001
echo Building Slamtec API Tool...

:: Clean previous builds
echo Cleaning previous builds...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
rmdir /s /q build_output 2>nul

:: Create build_output directory
mkdir build_output

:: Build main program with minimal options
echo Building main program...
pyinstaller --noconfirm --clean --onefile ^
    --hidden-import=PyQt5 ^
    --hidden-import=PyQt5.QtCore ^
    --hidden-import=PyQt5.QtGui ^
    --hidden-import=PyQt5.QtWidgets ^
    --hidden-import=requests ^
    --hidden-import=python-dotenv ^
    --hidden-import=loguru ^
    --hidden-import=werkzeug ^
    --hidden-import=flask ^
    --hidden-import=sip ^
    --hidden-import=PyQt5.sip ^
    --hidden-import=json ^
    --hidden-import=os ^
    --hidden-import=sys ^
    --hidden-import=logging ^
    --hidden-import=threading ^
    --hidden-import=uuid ^
    --add-data "src;src" ^
    --distpath build_output ^
    --name Slamtec_API_Tool ^
    --noupx ^
    --debug all ^
    src/main.py

:: Build mock server
echo Building mock server...
pyinstaller --noconfirm --clean --onefile ^
    --hidden-import=flask ^
    --hidden-import=werkzeug ^
    --hidden-import=requests ^
    --hidden-import=python-dotenv ^
    --hidden-import=loguru ^
    --hidden-import=json ^
    --hidden-import=os ^
    --hidden-import=sys ^
    --hidden-import=logging ^
    --hidden-import=threading ^
    --hidden-import=uuid ^
    --distpath build_output ^
    --name MockServer ^
    --noupx ^
    --debug all ^
    server.py

:: Copy additional files
echo Copying additional files...
copy server.py build_output\ 2>nul
copy requirements.txt build_output\ 2>nul
copy README.md build_output\ 2>nul
xcopy /E /I /Y src build_output\src\

echo Build completed!
pause 