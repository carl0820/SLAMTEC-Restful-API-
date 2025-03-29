@echo off
echo 正在安装打包依赖...
pip install pyinstaller

echo 正在清理旧的构建文件...
rmdir /s /q build
rmdir /s /q dist

echo 开始打包应用程序...
pyinstaller --clean build_exe.spec

echo 打包完成！
echo 可执行文件位于 dist 目录中
pause 