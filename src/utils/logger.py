import logging
import os
from datetime import datetime

def setup_logger(name):
    # 创建日志目录
    log_dir = os.path.join('src', 'log')
    os.makedirs(log_dir, exist_ok=True)

    # 创建日志文件名（使用当前日期）
    log_file = os.path.join(log_dir, f'{datetime.now().strftime("%Y-%m-%d")}.log')

    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 创建文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 创建格式器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 设置格式器
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger 