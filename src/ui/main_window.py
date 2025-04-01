from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QLineEdit, QStatusBar)
from PyQt5.QtCore import Qt, QTimer
from .connection_widget import ConnectionWidget
from .device_info_widget import DeviceInfoWidget
from .api_test_widget import ApiTestWidget
from loguru import logger

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
        
        # 创建定时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.query_device_info)
        self.update_timer.setInterval(1000)  # 设置1000ms(1秒)的更新间隔
        
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
            # 连接成功后立即查询设备信息
            self.query_device_info()
            # 启动定时器
            self.update_timer.start()
        else:
            self.status_bar.showMessage("未连接")
            self.device_info_widget.setEnabled(False)
            self.api_test_widget.setEnabled(False)
            # 断开连接时清空设备信息
            self.device_info_widget.clear_info()
            # 停止定时器
            self.update_timer.stop()
    
    def handle_api_client_changed(self, api_client):
        """处理API客户端变化"""
        self.device_info_widget.set_api_client(api_client)
        self.api_test_widget.set_api_client(api_client)
        # API客户端变化时查询设备信息
        if api_client:
            self.query_device_info()
            # 启动定时器
            self.update_timer.start()
        else:
            # 停止定时器
            self.update_timer.stop()
    
    def query_device_info(self):
        """查询设备信息"""
        try:
            if not self.device_info_widget.api_client:
                return
                
            # 查询电源信息
            power_info = self.device_info_widget.api_client.get("/api/core/system/v1/power/status")
            
            # 查询定位质量
            localization_quality = self.device_info_widget.api_client.get("/api/core/slam/v1/localization/quality")
            
            # 查询当前任务状态（包含最新的stage和state信息）
            current_action = self.device_info_widget.api_client.get_current_action()
            
            # 如果没有任务，显示无任务状态
            if current_action is None:
                current_action = {
                    "action_id": 0,
                    "action_name": "无任务",
                    "stage": "--",
                    "state": {
                        "status": 0,
                        "result": 0,
                        "reason": ""
                    }
                }
            
            # 更新设备信息显示
            self.device_info_widget.update_info(power_info, localization_quality, current_action)
            
        except Exception as e:
            error_msg = f"查询设备信息失败: {str(e)}"
            logger.error(error_msg)
            self.status_bar.showMessage(error_msg) 