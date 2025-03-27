# utils/logger.py

import logging
import os

def setup_logger(name: str, log_file: str, level=logging.INFO):
    """
    ساخت لاگر سفارشی برای هر بخش
    """
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", log_file)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False

    return logger
