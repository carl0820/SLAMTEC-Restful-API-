import os
import sys
import traceback
from loguru import logger

def setup_logging():
    """设置日志配置"""
    try:
        # 确保日志目录存在
        os.makedirs("logs", exist_ok=True)
        
        # 移除所有已存在的处理器
        logger.remove()
        
        # 添加文件日志处理器
        logger.add("logs/app.log", 
                  rotation="500 MB", 
                  level="DEBUG",
                  format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
                  backtrace=True, 
                  diagnose=True)
        
        # 添加控制台日志处理器
        logger.add(sys.stderr, 
                  level="DEBUG",
                  format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
                  backtrace=True, 
                  diagnose=True)
        
        logger.info("Logging setup completed")
    except Exception as e:
        print(f"Failed to setup logging: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

def check_dependencies():
    """检查必要的依赖是否已安装"""
    try:
        import PyQt5
        import requests
        import dotenv
        logger.info("All required dependencies are installed")
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {str(e)}")
        return False

def main():
    """主程序入口"""
    try:
        # 设置日志
        setup_logging()
        logger.info("Starting application...")
        
        # 检查依赖
        if not check_dependencies():
            logger.error("Missing required dependencies")
            input("Press Enter to exit...")
            sys.exit(1)
        
        # 设置 PyQt5 的异常处理
        sys.excepthook = lambda type, value, tb: logger.opt(exception=True).error("Uncaught exception: {}", value)
        
        # 添加源代码目录到 Python 路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(current_dir, 'src')
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
            logger.debug(f"Added {src_dir} to Python path")
        
        # 导入主程序
        logger.debug("Importing main module...")
        from src.main import main as app_main
        
        # 运行主程序
        logger.info("Running main application...")
        app_main()
        
    except ImportError as e:
        logger.error(f"Failed to import required modules: {str(e)}")
        logger.error(traceback.format_exc())
        input("Press Enter to exit...")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        logger.error(traceback.format_exc())
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()