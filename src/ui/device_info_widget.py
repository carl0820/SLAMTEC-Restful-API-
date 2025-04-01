from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QGroupBox, QMessageBox, QTextEdit,
                             QLabel, QGridLayout)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from loguru import logger

class DeviceInfoWidget(QGroupBox):
    def __init__(self, api_client=None):
        super().__init__("设备信息")
        self.api_client = api_client
        self.init_ui()
        
        # 定义状态颜色
        self.status_colors = {
            0: "#808080",  # 新创建 - 灰色
            1: "#0000FF",  # 正在运行 - 蓝色
            4: "#000000"   # 已结束 - 黑色（最终状态由result决定颜色）
        }
        
        self.result_colors = {
            0: "#008000",  # 成功 - 绿色
            -1: "#FF0000", # 失败 - 红色
            -2: "#FFA500"  # 被取消 - 橙色
        }
        
        # 保存最后一次任务的信息
        self.last_action = None
        self._current_action_id = None
        
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
        
        # 任务状态信息
        self.action_id_label = QLabel("任务ID: --")
        self.action_name_label = QLabel("任务名称: --")
        self.action_stage_label = QLabel("任务阶段: --")
        self.action_status_label = QLabel("任务状态: --")
        self.action_result_label = QLabel("任务结果: --")
        self.action_reason_label = QLabel("任务原因: --")
        
        # 添加到网格布局
        info_layout.addWidget(self.battery_label, 0, 0)
        info_layout.addWidget(self.docking_label, 0, 1)
        info_layout.addWidget(self.charging_label, 1, 0)
        info_layout.addWidget(self.power_stage_label, 1, 1)
        info_layout.addWidget(self.sleep_mode_label, 2, 0)
        info_layout.addWidget(self.localization_label, 2, 1)
        
        # 添加任务状态到网格布局
        info_layout.addWidget(self.action_id_label, 3, 0)
        info_layout.addWidget(self.action_name_label, 3, 1)
        info_layout.addWidget(self.action_stage_label, 4, 0)
        info_layout.addWidget(self.action_status_label, 4, 1)
        info_layout.addWidget(self.action_result_label, 5, 0)
        info_layout.addWidget(self.action_reason_label, 5, 1)
        
        layout.addLayout(info_layout)
    
    def set_api_client(self, api_client):
        """设置API客户端"""
        self.api_client = api_client
    
    def set_label_color(self, label, color):
        """设置标签文字颜色"""
        label.setStyleSheet(f"color: {color}")
    
    def update_info(self, power_info, localization_quality, current_action=None):
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
            
            # 如果有新任务且任务ID不为0，更新最后一次任务信息
            if current_action and current_action.get('action_id', 0) != 0:
                self.last_action = current_action.copy()  # 保存当前任务的副本
                self._display_action_info(current_action)
            elif self.last_action and self.last_action.get('action_id', 0) != 0:  # 如果没有新任务但有最后一次有效任务的信息
                # 查询最后一次任务的状态
                last_action_status = self.api_client.get_action_status(self.last_action['action_id'])
                self._display_action_info(last_action_status)
            else:  # 如果既没有新任务也没有最后一次有效任务的信息
                self._clear_action_info()
            
        except Exception as e:
            error_msg = f"更新设备信息失败: {str(e)}"
            logger.error(error_msg)
            QMessageBox.critical(self, "错误", error_msg)
    
    def _display_action_info(self, action_info):
        """显示任务信息"""
        try:
            action_id = action_info.get('action_id', '--')
            action_name = action_info.get('action_name', '--')
            stage = action_info.get('stage', '--')
            state = action_info.get('state', {})
            status = state.get('status', '--')
            result = state.get('result', '--')
            reason = state.get('reason', '')

            # 记录日志，帮助调试
            logger.debug(f"显示任务信息: action_id={action_id}, stage={stage}, status={status}, result={result}")

            # 更新任务ID和名称
            self.action_id_label.setText(f"任务ID: {action_id}")
            self.action_name_label.setText(f"任务名称: {action_name}")
            self.set_label_color(self.action_id_label, "#000000")
            self.set_label_color(self.action_name_label, "#000000")

            # 获取阶段描述
            stage_text = {
                "INITIALIZING": "初始化中",
                "GOING_TO_TARGET": "正在前往目标点",
                "DOCKING": "正在对接",
                "LIFTING": "正在顶升",
                "LOWERING": "正在下降",
                "BACKING_OFF": "正在退出",
                "FINISHED": "已完成",
                "FAILED": "已失败",
                "CANCELED": "已取消"
            }.get(stage, stage if stage else "--")
            
            # 更新任务阶段
            self.action_stage_label.setText(f"任务阶段: {stage_text}")
            
            # 根据状态设置颜色和文本
            if isinstance(status, int):
                status_text = {
                    0: "新创建",
                    1: "正在运行",
                    4: "已结束"
                }.get(status, "未知")
                
                # 更新任务状态
                self.action_status_label.setText(f"任务状态: {status} ({status_text})")
                
                # 更新任务结果
                if isinstance(result, int):
                    result_text = {
                        0: "成功",
                        -1: "失败",
                        -2: "被取消"
                    }.get(result, "未知")
                    
                    if status == 4:  # 任务已结束
                        # 更新任务结果
                        self.action_result_label.setText(f"任务结果: {result} ({result_text})")
                        # 设置结束状态的颜色
                        color = self.result_colors.get(result, "#000000")
                        self.set_label_color(self.action_result_label, color)
                        self.set_label_color(self.action_status_label, color)
                        self.set_label_color(self.action_stage_label, color)
                    else:  # 任务未结束
                        # 设置运行状态的颜色
                        color = self.status_colors.get(status, "#000000")
                        self.set_label_color(self.action_status_label, color)
                        if status == 1:  # 正在运行
                            self.action_result_label.setText(f"任务结果: -- ({stage_text})")
                            self.set_label_color(self.action_result_label, "#0000FF")
                            self.set_label_color(self.action_stage_label, "#0000FF")
                        else:  # 新创建
                            self.action_result_label.setText("任务结果: -- (等待开始)")
                            self.set_label_color(self.action_result_label, "#808080")
                            self.set_label_color(self.action_stage_label, "#808080")
                else:
                    # 如果result不是整数，显示默认值
                    if status == 1:  # 正在运行
                        self.action_result_label.setText(f"任务结果: -- ({stage_text})")
                        self.set_label_color(self.action_result_label, "#0000FF")
                        self.set_label_color(self.action_stage_label, "#0000FF")
                    else:  # 新创建或其他状态
                        self.action_result_label.setText("任务结果: -- (等待开始)")
                        self.set_label_color(self.action_result_label, "#808080")
                        self.set_label_color(self.action_stage_label, "#808080")

            # 更新任务原因
            if status == 4 and result == -1 and reason:
                self.action_reason_label.setText(f"任务原因: {reason}")
                self.set_label_color(self.action_reason_label, "#FF0000")
            else:
                self.action_reason_label.setText("任务原因: 无")
                self.set_label_color(self.action_reason_label, "#000000")
        except Exception as e:
            logger.error(f"显示任务信息失败: {str(e)}")
            raise
    
    def _clear_action_info(self):
        """清除任务信息"""
        # 清空任务状态信息
        self.action_id_label.setText("任务ID: --")
        self.action_name_label.setText("任务名称: --")
        self.action_stage_label.setText("任务阶段: --")
        self.action_status_label.setText("任务状态: --")
        self.action_result_label.setText("任务结果: --")
        self.action_reason_label.setText("任务原因: --")
        
        # 重置所有标签颜色为黑色
        for label in [self.action_id_label, self.action_name_label, self.action_stage_label,
                     self.action_status_label, self.action_result_label, self.action_reason_label]:
            self.set_label_color(label, "#000000")
    
    def clear_info(self):
        """清空设备信息"""
        self.battery_label.setText("电池电量: --")
        self.docking_label.setText("充电状态: --")
        self.charging_label.setText("是否充电: --")
        self.power_stage_label.setText("电源状态: --")
        self.sleep_mode_label.setText("睡眠模式: --")
        self.localization_label.setText("定位质量: --")
        # 清空任务状态信息
        self.action_id_label.setText("任务ID: --")
        self.action_name_label.setText("任务名称: --")
        self.action_stage_label.setText("任务阶段: --")
        self.action_status_label.setText("任务状态: --")
        self.action_result_label.setText("任务结果: --")
        self.action_reason_label.setText("任务原因: --")
        
        # 重置所有标签颜色为黑色
        for label in [self.action_id_label, self.action_name_label, self.action_stage_label,
                     self.action_status_label, self.action_result_label, self.action_reason_label]:
            self.set_label_color(label, "#000000") 