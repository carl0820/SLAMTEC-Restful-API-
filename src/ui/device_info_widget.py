from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QGroupBox, QMessageBox, QTextEdit,
                             QLabel, QGridLayout)
from PyQt5.QtCore import pyqtSignal
from loguru import logger

class DeviceInfoWidget(QGroupBox):
    def __init__(self, api_client=None):
        super().__init__("设备信息")
        self.api_client = api_client
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 创建信息显示区域
        info_layout = QGridLayout()
        
        # 电源信息
        self.battery_label = QLabel("电池电量: --")
        self.docking_label = QLabel("充电状态: --")
        self.charging_label = QLabel("是否充电: --")
        self.power_stage_label = QLabel("电源状态: --")
        self.sleep_mode_label = QLabel("睡眠模式: --")
        
        # 定位信息
        self.localization_label = QLabel("定位质量: --")
        
        # 添加到网格布局
        info_layout.addWidget(self.battery_label, 0, 0)
        info_layout.addWidget(self.docking_label, 0, 1)
        info_layout.addWidget(self.charging_label, 1, 0)
        info_layout.addWidget(self.power_stage_label, 1, 1)
        info_layout.addWidget(self.sleep_mode_label, 2, 0)
        info_layout.addWidget(self.localization_label, 2, 1)
        
        layout.addLayout(info_layout)
    
    def set_api_client(self, api_client):
        """设置API客户端"""
        self.api_client = api_client
    
    def update_info(self, power_info, localization_quality):
        """更新设备信息显示"""
        try:
            # 更新电源信息
            self.battery_label.setText(f"电池电量: {power_info.get('batteryPercentage', '--')}%")
            self.docking_label.setText(f"充电状态: {power_info.get('dockingStatus', '--')}")
            self.charging_label.setText(f"是否充电: {'是' if power_info.get('isCharging') else '否'}")
            self.power_stage_label.setText(f"电源状态: {power_info.get('powerStage', '--')}")
            self.sleep_mode_label.setText(f"睡眠模式: {power_info.get('sleepMode', '--')}")
            
            # 更新定位信息
            self.localization_label.setText(f"定位质量: {localization_quality}")
            
        except Exception as e:
            error_msg = f"更新设备信息失败: {str(e)}"
            logger.error(error_msg)
            QMessageBox.critical(self, "错误", error_msg)
    
    def clear_info(self):
        """清空设备信息"""
        self.battery_label.setText("电池电量: --")
        self.docking_label.setText("充电状态: --")
        self.charging_label.setText("是否充电: --")
        self.power_stage_label.setText("电源状态: --")
        self.sleep_mode_label.setText("睡眠模式: --")
        self.localization_label.setText("定位质量: --") 