import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from loguru import logger

def main():
    # 配置日志
    logger.add("logs/app.log", rotation="500 MB")
    
    # 创建应用
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec()) 