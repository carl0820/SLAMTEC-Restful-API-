from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QLineEdit, QStatusBar)
from PyQt5.QtCore import Qt
from .connection_widget import ConnectionWidget
from .device_info_widget import DeviceInfoWidget
from .api_test_widget import ApiTestWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Slamtec API 新手上路")
        self.setMinimumSize(1200, 800)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建连接区域
        self.connection_widget = ConnectionWidget()
        main_layout.addWidget(self.connection_widget)
        
        # 创建设备信息区域
        self.device_info_widget = DeviceInfoWidget()
        main_layout.addWidget(self.device_info_widget)
        
        # 创建API测试区域
        self.api_test_widget = ApiTestWidget()
        main_layout.addWidget(self.api_test_widget)
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        
        # 连接信号
        self.connection_widget.connection_status_changed.connect(
            self.handle_connection_status_changed
        )
        self.connection_widget.api_client_changed.connect(
            self.handle_api_client_changed
        )
    
    def handle_connection_status_changed(self, connected: bool):
        """处理连接状态变化"""
        if connected:
            self.status_bar.showMessage("已连接到设备")
            self.device_info_widget.setEnabled(True)
            self.api_test_widget.setEnabled(True)
        else:
            self.status_bar.showMessage("未连接")
            self.device_info_widget.setEnabled(False)
            self.api_test_widget.setEnabled(False)
    
    def handle_api_client_changed(self, api_client):
        """处理API客户端变化"""
        self.device_info_widget.set_api_client(api_client)
        self.api_test_widget.set_api_client(api_client) 