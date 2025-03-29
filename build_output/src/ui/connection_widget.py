from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QGroupBox, QMessageBox,
                             QTextEdit, QToolButton)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from loguru import logger
from src.api.robot_api import RobotAPI
import requests
import socket
import threading
import json
import os
import webbrowser

class ConnectionWidget(QGroupBox):
    connection_status_changed = pyqtSignal(bool)
    api_client_changed = pyqtSignal(object)
    
    def __init__(self):
        super().__init__("设备连接")
        self.config_file = "connection_config.json"
        self.init_ui()
        self.connected = False
        self.api_client = None
        self.device_info = None
        
        # 加载上次的连接配置
        self.load_connection_config()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 创建连接表单
        form_layout = QHBoxLayout()
        
        # IP地址输入
        ip_layout = QHBoxLayout()
        ip_label = QLabel("IP地址:")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("例如: 10.160.129.66")
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.ip_input)
        form_layout.addLayout(ip_layout)
        
        # 端口号输入
        port_layout = QHBoxLayout()
        port_label = QLabel("端口号:")
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("例如: 1448")
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_input)
        form_layout.addLayout(port_layout)
        
        # 连接按钮
        self.connect_button = QPushButton("连接")
        self.connect_button.clicked.connect(self.handle_connection)
        form_layout.addWidget(self.connect_button)
        
        # 添加在线API调试按钮
        self.api_doc_button = QPushButton("在线API调试")
        self.api_doc_button.clicked.connect(self.open_api_doc)
        form_layout.addWidget(self.api_doc_button)
        
        layout.addLayout(form_layout)
        
        # 创建设备信息显示区域
        info_layout = QVBoxLayout()
        
        # 创建设备信息标题栏
        title_layout = QHBoxLayout()
        info_label = QLabel("设备信息")
        self.toggle_button = QToolButton()
        self.toggle_button.setArrowType(Qt.ArrowType.RightArrow)
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_device_info)
        title_layout.addWidget(self.toggle_button)
        title_layout.addWidget(info_label)
        title_layout.addStretch()
        info_layout.addLayout(title_layout)
        
        # 创建设备信息文本框
        self.device_info_text = QTextEdit()
        self.device_info_text.setReadOnly(True)
        self.device_info_text.setMaximumHeight(200)
        self.device_info_text.hide()  # 默认隐藏
        info_layout.addWidget(self.device_info_text)
        
        layout.addLayout(info_layout)
    
    def toggle_device_info(self):
        """切换设备信息显示状态"""
        if self.toggle_button.isChecked():
            self.toggle_button.setArrowType(Qt.ArrowType.DownArrow)
            self.device_info_text.show()
        else:
            self.toggle_button.setArrowType(Qt.ArrowType.RightArrow)
            self.device_info_text.hide()
    
    def update_device_info(self):
        """更新设备信息显示"""
        try:
            if self.api_client:
                device_info = self.api_client.get_device_info()
                formatted_info = (
                    f"设备ID: {device_info.get('deviceID', 'N/A')}\n"
                    f"硬件版本: {device_info.get('hardwareVersion', 'N/A')}\n"
                    f"软件版本: {device_info.get('softwareVersion', 'N/A')}\n"
                    f"制造商ID: {device_info.get('manufacturerId', 'N/A')}\n"
                    f"制造商名称: {device_info.get('manufacturerName', 'N/A')}\n"
                    f"型号ID: {device_info.get('modelId', 'N/A')}\n"
                    f"型号名称: {device_info.get('modelName', 'N/A')}"
                )
                self.device_info_text.setText(formatted_info)
                self.device_info = device_info
        except Exception as e:
            logger.error(f"获取设备信息失败: {str(e)}")
            self.device_info_text.setText("获取设备信息失败")
    
    def load_connection_config(self):
        """加载上次的连接配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.ip_input.setText(config.get('ip', '10.160.129.66'))
                    self.port_input.setText(config.get('port', '1448'))
            else:
                # 如果配置文件不存在，使用默认值
                self.ip_input.setText("10.160.129.66")
                self.port_input.setText("1448")
        except Exception as e:
            logger.error(f"加载连接配置失败: {str(e)}")
            # 使用默认值
            self.ip_input.setText("10.160.129.66")
            self.port_input.setText("1448")
    
    def save_connection_config(self):
        """保存连接配置"""
        try:
            config = {
                'ip': self.ip_input.text().strip(),
                'port': self.port_input.text().strip()
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            logger.error(f"保存连接配置失败: {str(e)}")
    
    def check_device_online(self, ip: str, port: int) -> bool:
        """检查设备是否在线"""
        try:
            # 创建socket连接
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)  # 设置超时时间为2秒
            
            # 尝试连接
            result = sock.connect_ex((ip, port))
            sock.close()
            
            return result == 0
        except Exception as e:
            logger.error(f"检查设备在线状态失败: {str(e)}")
            return False
    
    def handle_connection(self):
        """处理连接按钮点击事件"""
        if not self.connected:
            # 获取输入值
            ip = self.ip_input.text().strip()
            port = self.port_input.text().strip()
            
            # 验证输入
            if not ip or not port:
                QMessageBox.warning(self, "输入错误", "IP地址和端口号不能为空")
                return
            
            try:
                # 检查端口号是否有效
                port_num = int(port)
                if not (1 <= port_num <= 65535):
                    raise ValueError("端口号必须在1-65535之间")
                
                # 检查设备是否在线
                if not self.check_device_online(ip, port_num):
                    QMessageBox.critical(self, "连接错误", "设备不在线，请检查设备是否开机")
                    logger.error(f"设备不在线: {ip}:{port}")
                    return
                
                # 创建API客户端并测试连接
                base_url = f"http://{ip}:{port}"
                self.api_client = RobotAPI(base_url)
                
                # 测试连接 - 尝试获取设备信息
                self.api_client.get_device_info()
                
                # 连接成功，保存配置
                self.save_connection_config()
                
                # 连接成功
                self.connected = True
                self.connect_button.setText("断开")
                self.ip_input.setEnabled(False)
                self.port_input.setEnabled(False)
                self.connection_status_changed.emit(True)
                self.api_client_changed.emit(self.api_client)
                
                # 自动获取并显示设备信息
                self.update_device_info()
                self.toggle_button.setChecked(True)
                self.toggle_device_info()
                
                logger.info(f"已连接到设备 {ip}:{port}")
                QMessageBox.information(self, "连接成功", f"已成功连接到设备 {ip}:{port}")
            except ValueError as e:
                QMessageBox.critical(self, "输入错误", str(e))
                logger.error(f"输入错误: {str(e)}")
            except requests.exceptions.ConnectionError:
                QMessageBox.critical(self, "连接错误", "无法连接到设备，请检查IP地址和端口是否正确")
                logger.error(f"连接失败: 无法连接到设备 {ip}:{port}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"连接失败: {str(e)}")
                logger.error(f"连接失败: {str(e)}")
        else:
            # 断开连接
            self.connected = False
            self.connect_button.setText("连接")
            self.ip_input.setEnabled(True)
            self.port_input.setEnabled(True)
            self.api_client = None
            self.device_info = None
            self.device_info_text.clear()
            self.connection_status_changed.emit(False)
            self.api_client_changed.emit(None)
            logger.info("已断开设备连接")
    
    def open_api_doc(self):
        """打开在线API文档"""
        ip = self.ip_input.text().strip()
        port = self.port_input.text().strip()
        
        if not ip or not port:
            QMessageBox.warning(self, "输入错误", "IP地址和端口号不能为空")
            return
            
        try:
            # 检查端口号是否有效
            port_num = int(port)
            if not (1 <= port_num <= 65535):
                raise ValueError("端口号必须在1-65535之间")
            
            # 构建API文档URL
            api_doc_url = f"http://{ip}:{port}/index.html"
            
            # 在浏览器中打开API文档
            webbrowser.open(api_doc_url)
            
        except ValueError as e:
            QMessageBox.critical(self, "输入错误", str(e))
            logger.error(f"输入错误: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"打开API文档失败: {str(e)}")
            logger.error(f"打开API文档失败: {str(e)}") 