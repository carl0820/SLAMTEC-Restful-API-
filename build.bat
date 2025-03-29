@echo off
chcp 65001
echo 开始打包程序...

:: 清理之前的构建
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
rmdir /s /q build_output 2>nul
del /f /q *.spec 2>nul

:: 创建输出目录
mkdir build_output

:: 打包主程序
python -m PyInstaller --noconfirm --clean ^
    --onefile ^
    --noconsole ^
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
    --add-data "requirements.txt;." ^
    --add-data "README.md;." ^
    --distpath build_output ^
    --name Slamtec_API_Tool ^
    --noupx ^
    --debug all ^
    run.py

:: 复制必要的文件
copy server.py build_output\
copy requirements.txt build_output\
copy README.md build_output\

echo 打包完成！
echo 输出目录：build_output
pause 