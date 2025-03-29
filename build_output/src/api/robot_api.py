import requests
from loguru import logger

class RobotAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def get(self, endpoint: str):
        """发送GET请求到指定端点"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_device_info(self):
        """获取设备信息"""
        url = f"{self.base_url}/api/core/system/v1/robot/info"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def sync_map(self):
        """同步地图"""
        url = f"{self.base_url}/api/multi-floor/map/v1/stcm/:sync"
        response = self.session.post(url)
        response.raise_for_status()
        return response.status_code == 200
    
    def generate_landing_pose(self, distance: float, reversed: bool = False):
        """生成Landing Pose"""
        url = f"{self.base_url}/api/industry/v1/generate_landing_pose"
        data = {
            "distance": distance,
            "reversed": reversed
        }
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def dock_to_shelf(self, x: float, y: float, yaw: float):
        """通过坐标值进行货架对接"""
        url = f"{self.base_url}/api/core/motion/v1/actions"
        data = {
            "action_name": "slamtec.agent.actions.SchedulableMoveToTagAction",
            "options": {
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
                            "shelf_columnar_diameter": 0.04,   #货架腿宽度/直径
                            "shelf_columnar_length": 0.62,     #货架长----货架前后腿距离（外侧边界）
                            "shelf_columnar_width": 0.7        #货架宽度----货架左右腿距离（外侧边界）
                        }
                    ]
                }
            }
        }
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def dock_to_poi(self, poi_name: str):
        """通过POI方式进行货架对接"""
        url = f"{self.base_url}/api/core/motion/v1/actions"
        data = {
            "action_name": "slamtec.agent.actions.SchedulableMoveToTagAction",
            "options": {
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
                            "shelf_columnar_diameter": 0.04,   #货架腿宽度/直径
                            "shelf_columnar_length": 0.62,     #货架长----货架前后腿距离（外侧边界）
                            "shelf_columnar_width": 0.7        #货架宽度----货架左右腿距离（外侧边界）
                        }
                    ]
                }
            }
        }
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def move_to_target(self, x: float, y: float, yaw: float):
        """搬运货架至目标点x,y,yaw"""
        url = f"{self.base_url}/api/core/motion/v1/actions"
        data = {
            "action_name": "slamtec.agent.actions.JackTopMoveToAction",
            "options": {
                "targets": [
                    {
                        "x": x,
                        "y": y,
                        "yaw": yaw
                    }
                ],
                "modify_params_move_options": {
                    "move_options": {
                        "mode": 0,
                        "flags": ["precise", "with_yaw"],
                        "yaw": 1.57
                    },
                    "robot_line_speed": 0.7,
                    "align_distance": -1,
                    "backward_docking": True
                }
            }
        }
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def backoff_shelf(self):
        """退出货架"""
        url = f"{self.base_url}/api/core/motion/v1/actions"
        data = {
            "action_name": "slamtec.agent.actions.BackOffFromTagAction",
            "options": {
                "backup_mode": 1,
                "tag_type": 3,
                "back_up_distance": 1,
                "backward_docking": True
            }
        }
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def lift_shelf(self):
        """顶升货架"""
        url = f"{self.base_url}/api/core/motion/v1/actions"
        data = {
            "action_name": "slamtec.agent.actions.JackMoveAction",
            "options": {
                "move_direction": "Up"
            }
        }
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def lower_shelf(self):
        """放下货架"""
        url = f"{self.base_url}/api/core/motion/v1/actions"
        data = {
            "action_name": "slamtec.agent.actions.JackMoveAction",
            "options": {
                "move_direction": "Down"
            }
        }
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def go_home(self):
        """回桩"""
        url = f"{self.base_url}/api/multi-floor/motion/v1/gohomeaction"
        response = self.session.post(url)
        response.raise_for_status()
        return response.json()
    
    def get_action_status(self, action_id: int):
        """获取action状态"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/core/motion/v1/actions/{action_id}"
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"获取action状态失败: {str(e)}")
            raise 