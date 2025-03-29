@echo off
chcp 65001
echo Building Slamtec API Tool...

:: Check Python version
python --version
if errorlevel 1 (
    echo Python is not installed or not in PATH
    pause
    exit /b 1
)

:: Install dependencies with error checking
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

pip install pyinstaller
if errorlevel 1 (
    echo Failed to install PyInstaller
    pause
    exit /b 1
)

:: Clean previous builds
echo Cleaning previous builds...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
rmdir /s /q build_output 2>nul

:: Build main program using spec file
echo Building main program...
pyinstaller --noconfirm Slamtec_API_Tool.spec

if errorlevel 1 (
    echo Failed to build main program
    pause
    exit /b 1
)

:: Build mock server
echo Building mock server...
pyinstaller --noconfirm --clean --onefile ^
    --hidden-import=flask ^
    --hidden-import=werkzeug ^
    --hidden-import=requests ^
    --hidden-import=python-dotenv ^
    --hidden-import=loguru ^
    --distpath build_output ^
    --name MockServer ^
    --noupx ^
    server.py

if errorlevel 1 (
    echo Failed to build mock server
    pause
    exit /b 1
)

:: Copy files to build_output directory
echo Copying additional files...
xcopy /y /q dist\Slamtec_API_Tool.exe build_output\
copy server.py build_output\ 2>nul
copy requirements.txt build_output\ 2>nul
copy README.md build_output\ 2>nul

echo Build completed successfully!
echo.
echo Please check the following:
echo 1. The executable is in the build_output directory
echo 2. All required DLLs are present
echo 3. Try running the program with administrator privileges
echo.
pause 