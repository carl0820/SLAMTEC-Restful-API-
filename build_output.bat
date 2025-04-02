@echo off
chcp 65001
echo Building Slamtec API Tool...

:: Install dependencies
pip install -r requirements.txt
pip install pyinstaller

:: Build main program
pyinstaller --noconfirm --onefile --windowed --hidden-import=PyQt5 --hidden-import=requests --hidden-import=python-dotenv --hidden-import=loguru --distpath build_output --name Slamtec_API_Tool src/main.py

:: Build mock server
pyinstaller --noconfirm --onefile --hidden-import=flask --hidden-import=werkzeug --distpath build_output --name MockServer server.py

:: Copy files to build_output directory
copy server.py build_output\
copy requirements.txt build_output\
copy README.md build_output\

echo Build completed!
pause 