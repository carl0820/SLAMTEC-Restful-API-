from flask import Flask, jsonify, request
import time
import random
import threading
import logging
from datetime import datetime
import uuid
import sys

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,  # 改为DEBUG级别以显示更多信息
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

app = Flask(__name__)

# 模拟设备状态
device_status = {
    "deviceID": "E6579ABFFF9FC6A9E1A753BE43554245",
    "hardwareVersion": "7.0",
    "manufacturerId": 255,
    "manufacturerName": "Slamtec",
    "modelId": 1013,
    "modelName": "phoebus-lite",
    "softwareVersion": "6.1.3-rtm-generic+20250111",
    "batteryPercentage": 85,
    "dockingStatus": "not_on_dock",
    "isCharging": False,
    "isDCConnected": False,
    "powerStage": "running",
    "sleepMode": "awake",
    "localization_quality": 53,
    "lora_state": "Running",
    "current_floor": {
        "building": "default",
        "elevator": "",
        "floor": "1f",
        "map_id": str(uuid.uuid4())
    }
}

# 模拟设备数据
device_data = {
    "position": {"x": 0.0, "y": 0.0, "theta": 0.0},
    "map_data": "base64_encoded_map_data",
    "health_status": {
        "baseError": [],
        "hasDepthCameraDisconnected": False,
        "hasError": False,
        "hasFatal": False,
        "hasLidarDisconnected": False,
        "hasSdpDisconnected": False,
        "hasSystemEmergencyStop": False,
        "hasWarning": False
    }
}

# 存储action状态
action_status = {}

def update_device_data():
    """后台任务：定期更新设备数据"""
    logging.info("Starting device data update thread")
    while True:
        try:
            # 模拟数据变化
            device_status["batteryPercentage"] = max(0, device_status["batteryPercentage"] - random.uniform(0, 0.1))
            device_status["localization_quality"] = max(0, min(100, device_status["localization_quality"] + random.uniform(-1, 1)))
            device_data["position"]["x"] += random.uniform(-0.1, 0.1)
            device_data["position"]["y"] += random.uniform(-0.1, 0.1)
            device_data["position"]["theta"] += random.uniform(-0.1, 0.1)
            
            # 更新健康状态
            if device_status["batteryPercentage"] < 20:
                device_data["health_status"]["hasWarning"] = True
                device_data["health_status"]["baseError"].append({
                    "component": 2,
                    "componentErrorCode": 256,
                    "componentErrorDeviceId": -1,
                    "componentErrorType": 3074,
                    "errorCode": 16908544,
                    "id": 1,
                    "level": 1,
                    "message": "power low"
                })
            else:
                device_data["health_status"]["hasWarning"] = False
                device_data["health_status"]["baseError"] = []
                
            time.sleep(5)  # 每5秒更新一次
        except Exception as e:
            logging.error(f"Error in update_device_data: {str(e)}")
            time.sleep(5)  # 发生错误时等待5秒后继续

@app.before_request
def log_request_info():
    """记录请求信息"""
    logging.debug('Headers: %s', request.headers)
    logging.debug('Body: %s', request.get_data())

@app.after_request
def log_response_info(response):
    """记录响应信息"""
    logging.debug('Response: %s', response.get_data())
    return response

@app.route('/api/core/system/v1/robot/info', methods=['GET'])
def get_robot_info():
    """获取设备信息"""
    try:
        return jsonify({
            "deviceID": device_status["deviceID"],
            "hardwareVersion": device_status["hardwareVersion"],
            "manufacturerId": device_status["manufacturerId"],
            "manufacturerName": device_status["manufacturerName"],
            "modelId": device_status["modelId"],
            "modelName": device_status["modelName"],
            "softwareVersion": device_status["softwareVersion"]
        })
    except Exception as e:
        logging.error(f"Error in get_robot_info: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/multi-floor/map/v1/stcm/:sync', methods=['POST'])
def sync_map():
    """同步地图"""
    try:
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logging.error(f"Error in sync_map: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/industry/v1/generate_landing_pose', methods=['POST'])
def generate_landing_pose():
    """创建landing_pose"""
    try:
        data = request.get_json()
        distance = data.get("distance", 1)
        reversed = data.get("reversed", True)
        
        return jsonify({
            "landing_pose": {
                "pitch": 0,
                "roll": 0,
                "x": random.uniform(0, 2),
                "y": random.uniform(-2, 0),
                "yaw": random.uniform(-3.14, 3.14),
                "z": 0
            },
            "robot_pose": {
                "pitch": 0,
                "roll": 0,
                "x": random.uniform(-1, 0),
                "y": random.uniform(-2, -1),
                "yaw": random.uniform(-0.5, 0.5),
                "z": 0
            }
        })
    except Exception as e:
        logging.error(f"Error in generate_landing_pose: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/core/motion/v1/actions', methods=['POST'])
def create_action():
    """创建动作"""
    try:
        data = request.get_json()
        action_name = data.get("action_name")
        
        # 生成新的action_id
        action_id = len(action_status) + 1
        
        # 创建action状态
        action_status[action_id] = {
            "action_id": action_id,
            "action_name": action_name,
            "stage": "INITIALIZING",
            "state": {
                "reason": "",
                "result": 0,
                "status": 0
            }
        }
        
        return jsonify(action_status[action_id])
    except Exception as e:
        logging.error(f"Error in create_action: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/core/motion/v1/actions/<int:action_id>', methods=['GET'])
def get_action_status(action_id):
    """获取action状态"""
    try:
        if action_id in action_status:
            return jsonify(action_status[action_id])
        return jsonify({"error": "Action not found"}), 404
    except Exception as e:
        logging.error(f"Error in get_action_status: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/multi-floor/motion/v1/gohomeaction', methods=['POST'])
def go_home():
    """回桩"""
    try:
        action_id = len(action_status) + 1
        action_status[action_id] = {
            "action_id": action_id,
            "action_name": "slamtec.agent.actions.MultiFloorBackHomeAction",
            "stage": "INITIALIZING",
            "state": {
                "reason": "",
                "result": 0,
                "status": 0
            }
        }
        return jsonify(action_status[action_id])
    except Exception as e:
        logging.error(f"Error in go_home: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/multi-floor/map/v1/floors/:current', methods=['GET'])
def get_current_floor():
    """获取当前地图信息"""
    try:
        return jsonify(device_status["current_floor"])
    except Exception as e:
        logging.error(f"Error in get_current_floor: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/swarm/network/v1/lora/status', methods=['GET'])
def get_lora_status():
    """获取LoRa状态"""
    try:
        return jsonify({"state": device_status["lora_state"]})
    except Exception as e:
        logging.error(f"Error in get_lora_status: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/core/slam/v1/localization/quality', methods=['GET'])
def get_localization_quality():
    """获取定位质量"""
    try:
        return jsonify(device_status["localization_quality"])
    except Exception as e:
        logging.error(f"Error in get_localization_quality: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/core/system/v1/power/status', methods=['GET'])
def get_power_status():
    """获取电源信息"""
    try:
        return jsonify({
            "batteryPercentage": device_status["batteryPercentage"],
            "dockingStatus": device_status["dockingStatus"],
            "isCharging": device_status["isCharging"],
            "isDCConnected": device_status["isDCConnected"],
            "powerStage": device_status["powerStage"],
            "sleepMode": device_status["sleepMode"]
        })
    except Exception as e:
        logging.error(f"Error in get_power_status: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/core/system/v1/robot/health', methods=['GET'])
def get_robot_health():
    """获取健康状态"""
    try:
        return jsonify(device_data["health_status"])
    except Exception as e:
        logging.error(f"Error in get_robot_health: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        # 启动后台任务
        background_thread = threading.Thread(target=update_device_data)
        background_thread.daemon = True
        background_thread.start()
        
        logging.info("Starting SLAMTEC Mock Server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logging.error(f"Failed to start server: {str(e)}")
        sys.exit(1) 