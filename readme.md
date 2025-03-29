# 项目名称
Slamtec Restful API 新手上路

## 项目简介
本项目主要通过演示如何快速机器人底盘的Restful API 进行底盘接口的调试和开发，方便刚买底盘的客户快速上手使用产品，提高使用效率。基于python开发桌面程序。

## 功能需求
### 1. 新手引导模块
- [ ] 首次启动引导流程
通过输入需要连接设备的IP地址和端口号，点击"连接"按钮
- [ ] 交互式教程
- [ ] 功能提示

### 2. 核心功能
- [ ] 显示设备信息
  - 详细描述
  - 接口依赖：通过"获取设备信息"接口
  - 连接设备成功后，显示设备的所有信息
- [ ] 同步地图
  - 详细描述：设置一个"同步地图"的按钮，点击后可进行同步地图，返回200后提示同步地图成功
  - 接口依赖：通过"同步地图"接口
  - 预期行为
- [ ] 接口演示 
  - 详细描述：
按照接口顺序分别是：创建landing_pose、- 通过坐标值进行货架对接、通过跨楼层POI方式进行货架对接、搬运货架至目标点x,y,yaw、搬运货架至目标POI、退出货架、顶升货架、放下货架、回桩、查询action_id状态；
response内的请求参数可以弹窗提示一个窗口进行请求的参数的更新和修改；
- 接口依赖：通过"创建landing_pose、- 通过坐标值进行货架对接、通过跨楼层POI方式进行货架对接、搬运货架至目标点x,y,yaw、搬运货架至目标POI、退出货架、顶升货架、放下货架、回桩、查询action_id状态"接口
  - 预期行为
  请求的日志和返回的日志有固定的窗口进行显示；
  根据响应的参数状态，进行状态值的显示；
### 3. 用户界面

#### 3.1 连接配置界面
- **设备连接区域**
  - [ ] IP地址输入框
  - [ ] 端口号输入框
  - [ ] 连接状态指示器
  - [ ] 连接/断开按钮
  - [ ] 连接错误提示

#### 3.2 主界面布局
- **顶部导航栏**
  - [ ] 设备信息显示
    - 设备ID
    - 硬件版本
    - 软件版本
    - 制造商信息
  - [ ] 连接状态指示
  - [ ] 系统设置入口

- **左侧功能导航**
  - [ ] 地图操作模块
    - 同步地图按钮
    - 地图显示区域
  - [ ] 接口调试模块
    - 基础操作
    - 货架操作
    - 移动控制

- **主操作区**
  - [ ] 接口调试面板
    - 参数配置区
      - 表单输入区
      - 参数验证提示
    - 请求发送按钮
    - 响应数据显示
  - [ ] 日志显示面板
    - 请求日志
    - 响应日志
    - 错误信息

#### 3.3 功能操作面板
- **货架操作模块**
  - [ ] Landing Pose 生成
    - 距离输入
    - 方向选择
    - 生成结果显示
  - [ ] 货架对接操作
    - 坐标输入（x, y, yaw）
    - POI 选择
    - 对接参数配置
  - [ ] 货架控制
    - 顶升/放下控制
    - 搬运目标设置
    - 退出货架操作

- **状态监控面板**
  - [ ] Action 状态显示
    - action_id 显示
    - 执行状态
    - 结果展示
    - 错误信息
  - [ ] 实时状态更新
    - 自动刷新开关
    - 刷新间隔设置

#### 3.4 交互反馈
- **操作提示**
  - [ ] 参数输入提示
  - [ ] 操作步骤引导
  - [ ] 错误处理提示
  - [ ] 成功反馈展示

- **加载状态**
  - [ ] 接口调用加载
  - [ ] 地图同步进度
  - [ ] 数据刷新提示

#### 3.5 响应式设计
- **桌面端优化**
  - [ ] 宽屏布局
  - [ ] 多面板并列显示
  - [ ] 快捷键支持

#### 3.6 辅助功能
- **调试工具**
  - [ ] 接口测试历史
  - [ ] 参数模板保存
  - [ ] 快速填充功能

- **文档支持**
  - [ ] 接口说明
  - [ ] 参数说明
  - [ ] 常见问题解答

#### 3.7 主题支持
- [ ] 明暗主题切换
- [ ] 自定义主题色
- [ ] 字体大小调节

## 技术规格
### API 集成
- 基础 URL：`http://10.160.129.66:1448`
- 认证方式：Bearer Token
- 主要接口列表：
  - `GET /api/core/system/v1/robot/info` - 获取设备信息
 Request Body:{}
  响应：{
    "deviceID": "E6579ABFFF9FC6A9E1A753BE43554245",
    "hardwareVersion": "7.0",
    "manufacturerId": 255,
    "manufacturerName": "Slamtec",
    "modelId": 1013,
    "modelName": "phoebus-lite",
    "softwareVersion": "6.1.3-rtm-generic+20250111"
}
  - `POST /api/multi-floor/map/v1/stcm/:sync` - 同步地图
Request Body: {}
Response: 200 OK


  - `/api/industry/v1/generate_landing_pose` - 创建landing_pose
  Response Body：{
    "distance": 1,
    "reversed": true
}
响应：{
    "landing_pose": {
        "pitch": 0,
        "roll": 0,
        "x": 0.67697411352979153,
        "y": -2.1463924284922351,
        "yaw": 2.9420654842868927,
        "z": 0
    },
    "robot_pose": {
        "pitch": 0,
        "roll": 0,
        "x": -0.30318629170993627,
        "y": -1.9481865254512498,
        "yaw": -0.19952716930290038,
        "z": 0
    }
}
  - `POST /api/core/motion/v1/actions` - 通过坐标值进行货架对接
   Response Body：{
"action_name":"slamtec.agent.actions.SchedulableMoveToTagAction",
"options":{
"target":{
"x":16.46,    # x,y,yaw使用生成对接点返回的landing_pose中的x,y,yaw
"y":-9.12,
"yaw": -0.6
},
"move_to_tag_options":{
"move_options":{
"mode": 0,  #0：自由导航，2：轨道优先
"flags":[]
},
"tag_type":3,             #0：二维码， 2：反光板，3：货架
"backward_docking":true,  #false为正入，true为倒入
"reflect_tag_num": 2,     #至少识别2个货架腿
"dock_allowance":0.2,     #进入货架预留距离，正入时更改为0
"shelves_size":[
{
"shelf_columnar_diameter": 0.04,   #货架腿宽度/直径
"shelf_columnar_length": 0.62,     #货架长----货架前后腿距离（外侧边界）
"shelf_columnar_width": 0.7        #货架宽度----货架左右腿距离（外侧边界）
},
{
"shelf_columnar_diameter": 0.04,
"shelf_columnar_length": 0.62,
"shelf_columnar_width": 0.8
}
]
}
}
}
响应：{
    "action_id": 14,
    "action_name": "slamtec.agent.actions.SchedulableMoveToTagAction",
    "stage": "INITIALIZING",
    "state": {
        "reason": "",     #如果 result 是-1，则该字段表示失败的原因
        "result": 0,      #0：成功， -1： 失败， -2：被取消
        "status": 0       #0：新创建，1：正在运行， 4：已结束
    }
}
  - `POST /api/core/motion/v1/actions` - 通过跨楼层POI方式进行货架对接
  Response Body：{
    "action_name": "slamtec.agent.actions.SchedulableMoveToTagAction",
    "options": {
        "target": {
            "poi_name": "对接点0210"
        },
        "move_to_tag_options": {
            "move_options": {
                "mode": 2
            },
            "tag_type": 3,
            "backward_docking": true,
            "reflect_tag_num": 2,
            "dock_allowance": 0.2,
            "shelves_columnar_diameter": 0.04,
            "shelves_length": 0.62,
            "shelves_width": 0.7
        }
    }
}
响应：{
    "action_id": 18,
    "action_name": "slamtec.agent.actions.SchedulableMoveToTagAction",
    "stage": "INITIALIZING",
    "state": {
        "reason": "",     #如果 result 是-1，则该字段表示失败的原因
        "result": 0,      #0：成功， -1： 失败， -2：被取消
        "status": 0       #0：新创建，1：正在运行， 4：已结束
    }
}
  - `POST /api/core/motion/v1/actions` - 搬运货架至目标点x,y,yaw
 Response Body：  {
    "action_name":"slamtec.agent.actions.JackTopMoveToAction",
    "options":{
         "targets":[                    
           {
            "x": 12.670000076293945,
            "y": -6.4600000381469727,
           }
         ],
         "modify_params_move_options":{
             "move_options":{
                 "mode": 0,                           
                 "flags":["precise","with_yaw"],
                 
             },
             "robot_line_speed": 0.7,         
             "align_distance": -1,         
             "backward_docking": true      
         }
    }
}
响应： {
    "action_id": 17,
    "action_name": "slamtec.agent.actions.JackTopMoveToAction",
    "stage": "",
    "state": {
        "reason": "",    #如果 result 是-1，则该字段表示失败的原因
        "result": 0,     #0：成功， -1： 失败， -2：被取消
        "status": 0      #0：新创建，1：正在运行， 4：已结束
    }
}
  - `POST /api/core/motion/v1/actions` - 搬运货架至目标POI
   Response Body： {
"action_name":"slamtec.agent.actions.JackTopMoveToAction",
"options":{
"target":{
"poi_name": "A101"
},
"modify_params_move_options":{
"move_options":{
"mode": 0,
"flags":["precise","with_yaw"]
},
"robot_line_speed": 0.7,
"align_distance": -1,
"backward_docking": true
}
}
}

  - `POST /api/core/motion/v1/actions` - 退出货架
 Response Body：    {
    "action_name": "slamtec.agent.actions.BackOffFromTagAction",
    "options": {
        "backup_mode": 1,     
        "tag_type": 3,
        "back_up_distance": 1,   
        "backward_docking": true 
    }
}
响应：{
    "action_id": 19,
    "action_name": "slamtec.agent.actions.BackOffFromTagAction",
    "stage": "",
    "state": {
        "reason": "",
        "result": 0,
        "status": 0
    }
}
  - `POST /api/core/motion/v1/actions` - 顶升货架
  Response Body：{
    "action_name": "slamtec.agent.actions.JackMoveAction",
    "options": {
        "move_direction": "Up"
    }
}
响应：{
    "action_id": 20,
    "action_name": "slamtec.agent.actions.JackMoveAction",
    "stage": "INIT",
    "state": {
        "reason": "",
        "result": 0,
        "status": 0
    }
}
  - `POST /api/core/motion/v1/actions` - 放下货架
  Response Body：{
    "action_name": "slamtec.agent.actions.JackMoveAction",
    "options": {
        "move_direction": "Down"
    }
}
响应：{
    "action_id": 21,
    "action_name": "slamtec.agent.actions.JackMoveAction",
    "stage": "INIT",
    "state": {
        "reason": "",
        "result": 0,
        "status": 0
    }
}
  - `POST /api/multi-floor/motion/v1/gohomeaction` - 回桩
   Response Body： {}
   响应：{
    "action_id": 22,
    "action_name": "slamtec.agent.actions.MultiFloorBackHomeAction",
    "stage": "INITIALIZING",
    "state": {
        "reason": "",
        "result": 0,
        "status": 0
    }
}
  - `GET /api/core/motion/v1/actions/{action_id}` - 查询action的状态
  Response Body： {}
  响应：{
    "action_id": 24,
    "state": {
        "reason": "",
        "result": 0,
        "status": 4
    }
}

# Slamtec API 调试工具

## 项目简介
本项目是一个基于 Python 和 PyQt6 开发的 Slamtec 机器人 API 调试工具，提供了友好的图形界面来测试和调试机器人的各项功能。

## 功能特点
- 设备连接与状态显示
- 设备信息查询
- 地图同步
- Landing Pose 生成
- 货架对接（坐标/POI方式）
- 货架控制（顶升/放下/退出）
- 搬运控制
- 回桩功能

## 环境要求
- Python 3.8 或更高版本
- Windows 10 或更高版本

## 安装依赖
```bash
pip install -r requirements.txt
```

## 运行方式

### 直接运行源码
```bash
python run.py
```

### 打包为可执行文件
1. 运行打包脚本：
```bash
build.bat
```
2. 打包完成后，可执行文件将位于 `dist` 目录中
3. 运行 `dist/Slamtec_API_Tool.exe`

## 配置说明
1. 程序首次运行时会在同目录下创建 `.env` 文件
2. 在 `.env` 文件中配置机器人的 API 基础地址：
```
API_BASE_URL=http://your.robot.ip:port
```

## 使用说明
1. 启动程序后，输入设备的 IP 地址和端口号
2. 点击"连接"按钮建立连接
3. 连接成功后即可使用各项功能
4. 所有 API 调用的请求和响应信息都会实时显示在界面上

## 注意事项
- 确保电脑和机器人在同一网络环境下
- 确保防火墙没有阻止程序的网络访问
- 如果遇到连接问题，请检查 IP 地址和端口号是否正确

## 常见问题
1. 如果打包后运行提示缺少 DLL：
   - 确保系统已安装 Visual C++ Redistributable
   - 或者使用 `--onefile` 模式重新打包

2. 如果程序无法连接到设备：
   - 检查网络连接
   - 确认设备 IP 和端口是否正确
   - 检查设备是否开启了 API 服务

## 技术支持
如有问题，请提交 Issue 或联系技术支持。

# 配置用户信息
git config --global user.email "353058362@qq.com"
git config --global user.name "carl0820"

# 初始化仓库
git init

# 添加所有文件
git add .

# 创建首次提交
git commit -m "初始化提交：添加项目文件"

## 多平台兼容设计

### 技术选择
- **核心框架**：Electron + React
  - 桌面端原生体验
  - Web技术开发
  - 跨平台支持(Windows/Mac/Linux)

- **移动端适配**
  - PWA (Progressive Web App) 支持
  - 响应式布局设计
  - 触控优化

### 平台特性支持
| 功能 | 桌面端 | 移动端 |
|------|--------|--------|
| API调用 | ✓ | ✓ |
| 地图显示 | 高清大图 | 简化版 |
| 实时监控 | ✓ | 简化版 |
| 离线模式 | ✓ | 部分支持 |
| 本地存储 | 无限制 | 受限 |

## 更新开发环境
### 框架选择
- **桌面应用框架**：Electron v27+
  - 用途：创建跨平台桌面应用
  - 优势：使用Web技术，易于开发

- **前端框架**：React 18+
  - 用途：构建响应式用户界面
  - 特性：支持组件复用和状态管理

- **UI组件库**：Ant Design 5.0+
  - 用途：提供桌面和移动端兼容组件
  - 优势：内置响应式设计

### 额外依赖
- **跨平台支持**
  ```json
  {
    "electron": "^27.0.0",
    "electron-builder": "^24.0.0",
    "react-responsive": "^9.0.0",
    "workbox-webpack-plugin": "^7.0.0"
  }
  ```
  - 用途：桌面打包和PWA支持

- **移动端触控**
  ```json
  {
    "react-swipeable": "^7.0.0",
    "hammer.js": "^2.0.8"
  }
  ```
  - 用途：触控手势支持

- **离线支持**
  ```json
  {
    "localforage": "^1.10.0",
    "dexie": "^3.2.0"
  }
  ```
  - 用途：本地数据存储和同步

## 更新项目结构
