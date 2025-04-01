from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QGroupBox, QTextEdit, QTabWidget,
                             QFormLayout, QSpinBox, QDoubleSpinBox, QCheckBox,
                             QComboBox, QMessageBox, QLineEdit, QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt
from loguru import logger
from src.api.robot_api import RobotAPI
import json

class ApiTestWidget(QGroupBox):
    def __init__(self):
        super().__init__("API测试")
        self.init_ui()
        self.setEnabled(False)
        self.api_client = None
    
    def set_api_client(self, api_client: RobotAPI):
        """设置API客户端"""
        self.api_client = api_client
        self.setEnabled(api_client is not None)
    
    def init_ui(self):
        """初始化UI"""
        main_layout = QVBoxLayout()
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)
        
        # 创建货架尺寸输入区域（移到顶部）
        shelf_size_group = QGroupBox("货架尺寸配置")
        shelf_size_layout = QFormLayout()
        
        self.shelf_diameter_input = QLineEdit()
        self.shelf_diameter_input.setPlaceholderText("默认: 0.04")
        self.shelf_diameter_input.setText("0.04")
        
        self.shelf_length_input = QLineEdit()
        self.shelf_length_input.setPlaceholderText("默认: 0.62")
        self.shelf_length_input.setText("0.62")
        
        self.shelf_width_input = QLineEdit()
        self.shelf_width_input.setPlaceholderText("默认: 0.7")
        self.shelf_width_input.setText("0.7")
        
        shelf_size_layout.addRow("货架腿直径(m):", self.shelf_diameter_input)
        shelf_size_layout.addRow("货架长度(m):", self.shelf_length_input)
        shelf_size_layout.addRow("货架宽度(m):", self.shelf_width_input)
        shelf_size_group.setLayout(shelf_size_layout)
        layout.addWidget(shelf_size_group)
        
        # 创建同步地图按钮
        sync_map_group = QGroupBox("地图操作")
        sync_map_layout = QHBoxLayout()
        self.sync_map_btn = QPushButton("同步地图")
        self.sync_map_btn.clicked.connect(self.sync_map)
        sync_map_layout.addWidget(self.sync_map_btn)
        
        # 添加查询地图按钮
        self.query_map_btn = QPushButton("查询地图")
        self.query_map_btn.clicked.connect(self.query_map)
        sync_map_layout.addWidget(self.query_map_btn)
        
        # 添加查询Lora按钮
        self.query_lora_btn = QPushButton("查询Lora")
        self.query_lora_btn.clicked.connect(self.query_lora)
        sync_map_layout.addWidget(self.query_lora_btn)
        
        sync_map_group.setLayout(sync_map_layout)
        layout.addWidget(sync_map_group)
        
        # 创建设备查询区域
        device_query_group = QGroupBox("设备查询")
        device_query_layout = QHBoxLayout()
        
        # 添加查询定位质量按钮
        self.query_localization_btn = QPushButton("查询定位质量")
        self.query_localization_btn.clicked.connect(self.query_localization)
        device_query_layout.addWidget(self.query_localization_btn)
        
        # 添加查询电量按钮
        self.query_power_btn = QPushButton("查询电量")
        self.query_power_btn.clicked.connect(self.query_power)
        device_query_layout.addWidget(self.query_power_btn)
        
        # 添加查询健康状态按钮
        self.query_health_btn = QPushButton("查询健康状态")
        self.query_health_btn.clicked.connect(self.query_health)
        device_query_layout.addWidget(self.query_health_btn)
        
        device_query_group.setLayout(device_query_layout)
        layout.addWidget(device_query_group)
        
        # 创建API信息显示区域
        api_info_group = QGroupBox("API请求信息")
        api_info_layout = QVBoxLayout()
        self.api_info_text = QTextEdit()
        self.api_info_text.setReadOnly(True)
        api_info_layout.addWidget(self.api_info_text)
        api_info_group.setLayout(api_info_layout)
        layout.addWidget(api_info_group)
        
        # 创建响应信息显示区域
        response_group = QGroupBox("响应信息")
        response_layout = QVBoxLayout()
        self.response_text = QTextEdit()
        self.response_text.setReadOnly(True)
        response_layout.addWidget(self.response_text)
        response_group.setLayout(response_layout)
        layout.addWidget(response_group)
        
        # 创建操作按钮区域
        button_group = QGroupBox("操作按钮")
        button_layout = QVBoxLayout()
        
        # Landing Pose生成
        landing_pose_group = QGroupBox("Landing Pose生成")
        landing_pose_layout = QHBoxLayout()
        self.distance_input = QLineEdit()
        self.distance_input.setPlaceholderText("距离")
        self.distance_input.setText("1.0")
        self.reversed_check = QCheckBox("反向")
        self.reversed_check.setChecked(True)
        self.generate_pose_btn = QPushButton("生成Landing Pose")
        self.generate_pose_btn.clicked.connect(self.generate_landing_pose)
        landing_pose_layout.addWidget(QLabel("距离:"))
        landing_pose_layout.addWidget(self.distance_input)
        landing_pose_layout.addWidget(self.reversed_check)
        landing_pose_layout.addWidget(self.generate_pose_btn)
        landing_pose_group.setLayout(landing_pose_layout)
        button_layout.addWidget(landing_pose_group)
        
        # 货架对接
        docking_group = QGroupBox("货架对接")
        docking_layout = QGridLayout()
        self.docking_mode = QComboBox()
        self.docking_mode.addItems(["坐标方式", "POI方式"])
        self.docking_mode.currentTextChanged.connect(self.on_docking_mode_changed)
        
        # 坐标输入框
        self.x_input = QLineEdit()
        self.x_input.setPlaceholderText("X坐标")
        self.y_input = QLineEdit()
        self.y_input.setPlaceholderText("Y坐标")
        self.yaw_input = QLineEdit()
        self.yaw_input.setPlaceholderText("Yaw角度")
        
        # POI输入框
        self.poi_input = QLineEdit()
        self.poi_input.setPlaceholderText("POI名称")
        self.poi_input.setEnabled(False)
        
        self.dock_btn = QPushButton("货架对接")
        self.dock_btn.clicked.connect(self.execute_docking)
        
        docking_layout.addWidget(QLabel("模式:"), 0, 0)
        docking_layout.addWidget(self.docking_mode, 0, 1)
        docking_layout.addWidget(QLabel("X:"), 1, 0)
        docking_layout.addWidget(self.x_input, 1, 1)
        docking_layout.addWidget(QLabel("Y:"), 1, 2)
        docking_layout.addWidget(self.y_input, 1, 3)
        docking_layout.addWidget(QLabel("Yaw:"), 1, 4)
        docking_layout.addWidget(self.yaw_input, 1, 5)
        docking_layout.addWidget(QLabel("POI:"), 2, 0)
        docking_layout.addWidget(self.poi_input, 2, 1, 1, 3)
        docking_layout.addWidget(self.dock_btn, 2, 4, 1, 2)
        docking_group.setLayout(docking_layout)
        button_layout.addWidget(docking_group)
        
        # 货架控制
        shelf_control_group = QGroupBox("货架控制")
        shelf_control_layout = QHBoxLayout()
        self.lift_btn = QPushButton("顶升货架")
        self.lift_btn.clicked.connect(self.lift_shelf)
        self.lower_btn = QPushButton("放下货架")
        self.lower_btn.clicked.connect(self.lower_shelf)
        self.backoff_btn = QPushButton("退出货架")
        self.backoff_btn.clicked.connect(self.backoff_shelf)
        shelf_control_layout.addWidget(self.lift_btn)
        shelf_control_layout.addWidget(self.lower_btn)
        shelf_control_layout.addWidget(self.backoff_btn)
        shelf_control_group.setLayout(shelf_control_layout)
        button_layout.addWidget(shelf_control_group)
        
        # 搬运控制
        move_control_group = QGroupBox("搬运控制")
        move_control_layout = QGridLayout()
        self.move_mode = QComboBox()
        self.move_mode.addItems(["坐标方式", "POI方式"])
        self.move_mode.currentTextChanged.connect(self.on_move_mode_changed)
        
        # 坐标输入框
        self.move_x_input = QLineEdit()
        self.move_x_input.setPlaceholderText("X坐标")
        self.move_y_input = QLineEdit()
        self.move_y_input.setPlaceholderText("Y坐标")
        self.move_yaw_input = QLineEdit()
        self.move_yaw_input.setPlaceholderText("Yaw角度")
        
        # POI输入框
        self.move_poi_input = QLineEdit()
        self.move_poi_input.setPlaceholderText("POI名称")
        self.move_poi_input.setEnabled(False)
        
        self.move_btn = QPushButton("搬运货架")
        self.move_btn.clicked.connect(self.move_shelf)
        
        move_control_layout.addWidget(QLabel("模式:"), 0, 0)
        move_control_layout.addWidget(self.move_mode, 0, 1)
        move_control_layout.addWidget(QLabel("X:"), 1, 0)
        move_control_layout.addWidget(self.move_x_input, 1, 1)
        move_control_layout.addWidget(QLabel("Y:"), 1, 2)
        move_control_layout.addWidget(self.move_y_input, 1, 3)
        move_control_layout.addWidget(QLabel("Yaw:"), 1, 4)
        move_control_layout.addWidget(self.move_yaw_input, 1, 5)
        move_control_layout.addWidget(QLabel("POI:"), 2, 0)
        move_control_layout.addWidget(self.move_poi_input, 2, 1, 1, 3)
        move_control_layout.addWidget(self.move_btn, 2, 4, 1, 2)
        move_control_group.setLayout(move_control_layout)
        button_layout.addWidget(move_control_group)
        
        # 回桩
        home_group = QGroupBox("回桩控制")
        home_layout = QHBoxLayout()
        self.go_home_btn = QPushButton("回桩")
        self.go_home_btn.clicked.connect(self.go_home)
        home_layout.addWidget(self.go_home_btn)
        home_group.setLayout(home_layout)
        button_layout.addWidget(home_group)
        
        button_group.setLayout(button_layout)
        layout.addWidget(button_group)
        
        # 设置滚动区域
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        
        self.setLayout(main_layout)
    
    def on_docking_mode_changed(self, mode: str):
        """处理对接模式变化"""
        is_poi_mode = mode == "POI方式"
        self.poi_input.setEnabled(is_poi_mode)
        self.x_input.setEnabled(not is_poi_mode)
        self.y_input.setEnabled(not is_poi_mode)
        self.yaw_input.setEnabled(not is_poi_mode)
    
    def on_move_mode_changed(self, mode: str):
        """处理搬运模式变化"""
        is_poi_mode = mode == "POI方式"
        self.move_poi_input.setEnabled(is_poi_mode)
        self.move_x_input.setEnabled(not is_poi_mode)
        self.move_y_input.setEnabled(not is_poi_mode)
        self.move_yaw_input.setEnabled(not is_poi_mode)
    
    def move_shelf(self):
        """搬运货架"""
        if not self.api_client:
            QMessageBox.warning(self, "错误", "请先连接设备")
            return
            
        try:
            mode = self.move_mode.currentText()
            
            # 获取货架尺寸
            shelf_diameter = float(self.shelf_diameter_input.text())
            shelf_length = float(self.shelf_length_input.text())
            shelf_width = float(self.shelf_width_input.text())
            
            api_info = {
                "request": {
                    "url": f"{self.api_client.base_url}/api/core/motion/v1/actions",
                    "method": "POST"
                }
            }
            
            if mode == "坐标方式":
                x = float(self.move_x_input.text())
                y = float(self.move_y_input.text())
                yaw = float(self.move_yaw_input.text())
                response = self.api_client.move_to_target(x, y, yaw)
                api_info["request"]["data"] = {
                    "action_name": "slamtec.agent.actions.JackTopMoveToAction",
                    "options": {
                        "targets": [
                            {
                                "x": x,
                                "y": y,
                                "yaw":yaw
                            }
                        ],
                        "modify_params_move_options": {
                            "move_options": {
                                "mode": 0,                           
                                "flags": ["precise", "with_yaw"],
                                "yaw":yaw
                            },
                            "robot_line_speed": 0.7,         
                            "align_distance": -1,         
                            "backward_docking": True      
                        }
                    }
                }
            else:
                poi_name = self.move_poi_input.text()
                if not poi_name:
                    QMessageBox.warning(self, "错误", "请输入POI名称")
                    return
                response = self.api_client.move_to_poi(poi_name)
                api_info["request"]["data"] = {
                    "action_name": "slamtec.agent.actions.JackTopMoveToAction",
                    "options": {
                        "target": {
                            "poi_name": poi_name
                        },
                        "modify_params_move_options": {
                            "move_options": {
                                "mode": 0,                           
                                "flags": ["precise", "with_yaw"]
                            },
                            "robot_line_speed": 0.7,         
                            "align_distance": -1,         
                            "backward_docking": True      
                        }
                    }
                }
            
            # 显示API请求信息
            self.api_info_text.setText(f"请求URL: {api_info['request']['url']}\n"
                                     f"请求方法: {api_info['request']['method']}\n"
                                     f"请求参数: {json.dumps(api_info['request']['data'], indent=2, ensure_ascii=False)}")
            
            # 显示响应信息
            self.response_text.setText(f"响应数据: {json.dumps(response, indent=2, ensure_ascii=False)}")
            
            # 显示成功消息
            QMessageBox.information(self, "成功", "搬运货架命令已发送")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"搬运货架失败: {str(e)}")
            logger.error(f"搬运货架失败: {str(e)}")
    
    def generate_landing_pose(self):
        """生成Landing Pose"""
        if not self.api_client:
            QMessageBox.warning(self, "错误", "请先连接设备")
            return
            
        try:
            distance = float(self.distance_input.text())
            reversed = self.reversed_check.isChecked()
            
            # 显示API信息
            api_info = {
                "endpoint": "/api/industry/v1/generate_landing_pose",
                "method": "POST",
                "request": {
                    "distance": distance,
                    "reversed": reversed
                }
            }
            self.api_info_text.setText(json.dumps(api_info, indent=2, ensure_ascii=False))
            
            logger.info(f"正在生成Landing Pose: 距离={distance}, 反向={reversed}")
            response = self.api_client.generate_landing_pose(distance, reversed)
            
            # 格式化显示响应
            formatted_response = json.dumps(response, indent=2, ensure_ascii=False)
            self.response_text.setText(formatted_response)
            
            # 自动填充货架对接坐标
            if response and 'landing_pose' in response:
                landing_pose = response['landing_pose']
                self.x_input.setText(str(round(landing_pose.get('x', 0), 3)))
                self.y_input.setText(str(round(landing_pose.get('y', 0), 3)))
                self.yaw_input.setText(str(round(landing_pose.get('yaw', 0), 3)))
                # 切换到坐标方式
                self.docking_mode.setCurrentText("坐标方式")
                # 启用坐标输入框
                self.x_input.setEnabled(True)
                self.y_input.setEnabled(True)
                self.yaw_input.setEnabled(True)
                # 禁用POI输入框
                self.poi_input.setEnabled(False)
            
            logger.info("Landing Pose生成完成")
            QMessageBox.information(self, "成功", "Landing Pose生成完成，已自动填充对接坐标")
        except Exception as e:
            logger.error(f"生成Landing Pose失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"生成Landing Pose失败: {str(e)}")
    
    def execute_docking(self):
        """执行货架对接"""
        if not self.api_client:
            return
            
        try:
            mode = self.docking_mode.currentText()
            
            # 获取货架尺寸
            shelf_diameter = float(self.shelf_diameter_input.text())
            shelf_length = float(self.shelf_length_input.text())
            shelf_width = float(self.shelf_width_input.text())
            
            # 显示API信息
            api_info = {
                "endpoint": "/api/core/motion/v1/actions",
                "method": "POST",
                "request": {
                    "action_name": "slamtec.agent.actions.SchedulableMoveToTagAction",
                    "options": {}
                }
            }
            
            if mode == "坐标方式":
                x = float(self.x_input.text())
                y = float(self.y_input.text())
                yaw = float(self.yaw_input.text())
                
                api_info["request"]["options"] = {
                    "target": {
                        "x": x,
                        "y": y,
                        "yaw": yaw
                    },
                    "move_to_tag_options": {
                        "move_options": {
                            "mode": 0,  #0：自由导航，2：轨道优先
                            "flags": []
                        },
                        "tag_type": 3,             #0：二维码， 2：反光板，3：货架
                        "backward_docking": True,  #false为正入，true为倒入
                        "reflect_tag_num": 2,     #至少识别2个货架腿
                        "dock_allowance": 0.2,     #进入货架预留距离，正入时更改为0
                        "shelves_size": [
                            {
                                "shelf_columnar_diameter": shelf_diameter,   #货架腿宽度/直径
                                "shelf_columnar_length": shelf_length,     #货架长----货架前后腿距离（外侧边界）
                                "shelf_columnar_width": shelf_width        #货架宽度----货架左右腿距离（外侧边界）
                            }
                        ]
                    }
                }
                response = self.api_client.dock_to_shelf(x, y, yaw)
            else:  # POI模式
                poi_name = self.poi_input.text().strip()
                if not poi_name:
                    raise ValueError("请输入POI名称")
                    
                api_info["request"]["options"] = {
                    "target": {
                        "poi_name": poi_name
                    },
                    "move_to_tag_options": {
                        "move_options": {
                            "mode": 2
                        },
                        "tag_type": 3,
                        "backward_docking": True,
                        "reflect_tag_num": 2,
                        "dock_allowance": 0.2,
                        "shelves_size": [
                            {
                                "shelf_columnar_diameter": shelf_diameter,   #货架腿宽度/直径
                                "shelf_columnar_length": shelf_length,     #货架长----货架前后腿距离（外侧边界）
                                "shelf_columnar_width": shelf_width        #货架宽度----货架左右腿距离（外侧边界）
                            }
                        ]
                    }
                }
                response = self.api_client.dock_to_poi(poi_name)
            
            self.api_info_text.setText(json.dumps(api_info, indent=2, ensure_ascii=False))
            
            # 格式化显示响应
            formatted_response = json.dumps(response, indent=2, ensure_ascii=False)
            self.response_text.setText(formatted_response)
            logger.info("货架对接执行完成")
            QMessageBox.information(self, "成功", "货架对接指令已发送")
        except Exception as e:
            logger.error(f"货架对接执行失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"货架对接执行失败: {str(e)}")
    
    def lift_shelf(self):
        """顶升货架"""
        if not self.api_client:
            return
            
        try:
            # 显示API信息
            api_info = {
                "endpoint": "/api/core/motion/v1/actions",
                "method": "POST",
                "request": {
                    "action_name": "slamtec.agent.actions.JackMoveAction",
                    "options": {
                        "move_direction": "Up"
                    }
                }
            }
            self.api_info_text.setText(json.dumps(api_info, indent=2, ensure_ascii=False))
            
            logger.info("正在顶升货架...")
            response = self.api_client.lift_shelf()
            
            # 格式化显示响应
            formatted_response = json.dumps(response, indent=2, ensure_ascii=False)
            self.response_text.setText(formatted_response)
            logger.info("货架顶升完成")
            QMessageBox.information(self, "成功", "顶升指令已发送")
        except Exception as e:
            logger.error(f"顶升货架失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"顶升货架失败: {str(e)}")
    
    def lower_shelf(self):
        """放下货架"""
        if not self.api_client:
            return
            
        try:
            # 显示API信息
            api_info = {
                "endpoint": "/api/core/motion/v1/actions",
                "method": "POST",
                "request": {
                    "action_name": "slamtec.agent.actions.JackMoveAction",
                    "options": {
                        "move_direction": "Down"
                    }
                }
            }
            self.api_info_text.setText(json.dumps(api_info, indent=2, ensure_ascii=False))
            
            logger.info("正在放下货架...")
            response = self.api_client.lower_shelf()
            
            # 格式化显示响应
            formatted_response = json.dumps(response, indent=2, ensure_ascii=False)
            self.response_text.setText(formatted_response)
            logger.info("货架放下完成")
            QMessageBox.information(self, "成功", "放下指令已发送")
        except Exception as e:
            logger.error(f"放下货架失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"放下货架失败: {str(e)}")
    
    def backoff_shelf(self):
        """退出货架"""
        if not self.api_client:
            return
            
        try:
            # 显示API信息
            api_info = {
                "endpoint": "/api/core/motion/v1/actions",
                "method": "POST",
                "request": {
                    "action_name": "slamtec.agent.actions.BackOffFromTagAction",
                    "options": {
                        "backup_mode": 1,
                        "tag_type": 3,
                        "back_up_distance": 1,
                        "backward_docking": True
                    }
                }
            }
            self.api_info_text.setText(json.dumps(api_info, indent=2, ensure_ascii=False))
            
            logger.info("正在退出货架...")
            response = self.api_client.backoff_shelf()
            
            # 格式化显示响应
            formatted_response = json.dumps(response, indent=2, ensure_ascii=False)
            self.response_text.setText(formatted_response)
            logger.info("货架退出完成")
            QMessageBox.information(self, "成功", "退出指令已发送")
        except Exception as e:
            logger.error(f"退出货架失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"退出货架失败: {str(e)}")
    
    def go_home(self):
        """回桩"""
        if not self.api_client:
            return
            
        try:
            # 显示API信息
            api_info = {
                "endpoint": "/api/multi-floor/motion/v1/gohomeaction",
                "method": "POST",
                "request": {}
            }
            self.api_info_text.setText(json.dumps(api_info, indent=2, ensure_ascii=False))
            
            logger.info("正在执行回桩...")
            response = self.api_client.go_home()
            
            # 格式化显示响应
            formatted_response = json.dumps(response, indent=2, ensure_ascii=False)
            self.response_text.setText(formatted_response)
            logger.info("回桩完成")
            QMessageBox.information(self, "成功", "回桩指令已发送")
        except Exception as e:
            logger.error(f"回桩失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"回桩失败: {str(e)}")
    
    def sync_map(self):
        """同步地图"""
        if not self.api_client:
            QMessageBox.warning(self, "错误", "请先连接设备")
            return
            
        try:
            # 显示API信息
            api_info = {
                "endpoint": "/api/multi-floor/map/v1/stcm/:sync",
                "method": "POST",
                "request": {}
            }
            self.api_info_text.setText(json.dumps(api_info, indent=2, ensure_ascii=False))
            
            # 调用同步地图API
            response = self.api_client.sync_map()
            
            # 显示响应信息
            self.response_text.setText(json.dumps(response, indent=2, ensure_ascii=False))
            
            # 显示成功消息
            QMessageBox.information(self, "成功", "地图同步成功")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"同步地图失败: {str(e)}")
            logger.error(f"同步地图失败: {str(e)}")
    
    def query_map(self):
        """查询当前地图信息"""
        try:
            if not self.api_client:
                QMessageBox.warning(self, "错误", "请先连接设备")
                return
                
            # 记录API请求信息
            api_info = {
                "endpoint": "/api/multi-floor/map/v1/floors/:current",
                "method": "GET",
                "description": "查询当前地图信息"
            }
            self.api_info_text.setText(json.dumps(api_info, indent=2, ensure_ascii=False))
            
            # 发送请求
            response = self.api_client.get("/api/multi-floor/map/v1/floors/:current")
            
            # 显示响应信息
            self.response_text.setText(json.dumps(response, indent=2, ensure_ascii=False))
            
        except Exception as e:
            error_msg = f"查询地图失败: {str(e)}"
            self.response_text.setText(error_msg)
            logger.error(error_msg)
            QMessageBox.critical(self, "错误", error_msg)
    
    def query_lora(self):
        """查询Lora状态"""
        try:
            if not self.api_client:
                QMessageBox.warning(self, "错误", "请先连接设备")
                return
                
            # 记录API请求信息
            api_info = {
                "endpoint": "/api/swarm/network/v1/lora/status",
                "method": "GET",
                "description": "查询Lora状态"
            }
            self.api_info_text.setText(json.dumps(api_info, indent=2, ensure_ascii=False))
            
            # 发送请求
            response = self.api_client.get("/api/swarm/network/v1/lora/status")
            
            # 显示响应信息
            self.response_text.setText(json.dumps(response, indent=2, ensure_ascii=False))
            
        except Exception as e:
            error_msg = f"查询Lora状态失败: {str(e)}"
            self.response_text.setText(error_msg)
            logger.error(error_msg)
            QMessageBox.critical(self, "错误", error_msg)
    
    def query_localization(self):
        """查询定位质量"""
        try:
            if not self.api_client:
                QMessageBox.warning(self, "错误", "请先连接设备")
                return
                
            # 记录API请求信息
            api_info = {
                "endpoint": "/api/core/slam/v1/localization/quality",
                "method": "GET",
                "description": "查询定位质量"
            }
            self.api_info_text.setText(json.dumps(api_info, indent=2, ensure_ascii=False))
            
            # 发送请求
            response = self.api_client.get("/api/core/slam/v1/localization/quality")
            
            # 显示响应信息
            self.response_text.setText(json.dumps(response, indent=2, ensure_ascii=False))
            
        except Exception as e:
            error_msg = f"查询定位质量失败: {str(e)}"
            self.response_text.setText(error_msg)
            logger.error(error_msg)
            QMessageBox.critical(self, "错误", error_msg)
    
    def query_power(self):
        """查询电源信息"""
        try:
            if not self.api_client:
                QMessageBox.warning(self, "错误", "请先连接设备")
                return
                
            # 记录API请求信息
            api_info = {
                "endpoint": "/api/core/system/v1/power/status",
                "method": "GET",
                "description": "查询电源信息"
            }
            self.api_info_text.setText(json.dumps(api_info, indent=2, ensure_ascii=False))
            
            # 发送请求
            response = self.api_client.get("/api/core/system/v1/power/status")
            
            # 显示响应信息
            self.response_text.setText(json.dumps(response, indent=2, ensure_ascii=False))
            
        except Exception as e:
            error_msg = f"查询电源信息失败: {str(e)}"
            self.response_text.setText(error_msg)
            logger.error(error_msg)
            QMessageBox.critical(self, "错误", error_msg)
    
    def query_health(self):
        """查询健康状态"""
        try:
            if not self.api_client:
                QMessageBox.warning(self, "错误", "请先连接设备")
                return
                
            # 记录API请求信息
            api_info = {
                "endpoint": "/api/core/system/v1/robot/health",
                "method": "GET",
                "description": "查询健康状态"
            }
            self.api_info_text.setText(json.dumps(api_info, indent=2, ensure_ascii=False))
            
            # 发送请求
            response = self.api_client.get("/api/core/system/v1/robot/health")
            
            # 显示响应信息
            self.response_text.setText(json.dumps(response, indent=2, ensure_ascii=False))
            
        except Exception as e:
            error_msg = f"查询健康状态失败: {str(e)}"
            self.response_text.setText(error_msg)
            logger.error(error_msg)
            QMessageBox.critical(self, "错误", error_msg)