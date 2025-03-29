from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QGroupBox, QMessageBox, QTextEdit)
from PyQt5.QtCore import pyqtSignal
from loguru import logger

class DeviceInfoWidget(QGroupBox):
    def __init__(self, api_client=None):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        # 由于我们要移除这个widget的显示，这里可以保持最小化的实现
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.hide()  # 隐藏整个widget
    
    def set_api_client(self, api_client):
        """设置API客户端"""
        self.api_client = api_client 