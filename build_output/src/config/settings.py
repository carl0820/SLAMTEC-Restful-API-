import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API配置
API_BASE_URL = os.getenv("API_BASE_URL", "http://10.160.129.66:1448")

# 日志配置
LOG_DIR = "logs"
LOG_FILE = "app.log"
LOG_ROTATION = "500 MB"

# 货架参数配置
SHELF_PARAMS = {
    "columnar_diameter": 0.04,
    "columnar_length": 0.62,
    "columnar_width": 0.7,
    "reflect_tag_num": 2,
    "dock_allowance": 0.2
}

# 移动参数配置
MOVE_PARAMS = {
    "line_speed": 0.7,
    "align_distance": -1,
    "backward_docking": True
} 