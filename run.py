import os
import sys
from src.main import main

if __name__ == "__main__":
    # 确保日志目录存在
    os.makedirs("logs", exist_ok=True)
    
    # 运行主程序
    main() 

# 根据同事的建议，重新安装 PyQt6
import subprocess

subprocess.run(["pip", "uninstall", "PyQt6", "PyQt6-Qt6", "PyQt6-sip", "-y"])
subprocess.run(["pip", "install", "-r", "requirements.txt"])

# 使用 pyinstaller 打包
subprocess.run(["pyinstaller", "--onefile", "--distpath", "dist", "run.py"])