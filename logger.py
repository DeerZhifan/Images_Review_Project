# -*- coding: utf-8 -*-

from algo.setting import config

import os
import logging
from logging.handlers import RotatingFileHandler


class Logger(object):
    """日志记录"""
    def __init__(self):
        # 初始化
        logger_name = config['logger']['logger_name']
        self.logger = logging.getLogger(name=logger_name)
        self.logger.setLevel(logging.WARNING)

        # 日志格式
        fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        date_fmt = '%Y-%m-%d %H:%M:%S'

        # 设置日志路径和文件名
        log_path = config['logger']['log_path']
        log_name = config['logger']['log_name']
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        file_name = os.path.join(log_path, log_name)

        # 每个日志文件最多10MB
        rt_hander = RotatingFileHandler(filename=file_name, maxBytes=10*1024*1024)
        formatter = logging.Formatter(fmt, datefmt=date_fmt)
        rt_hander.setFormatter(formatter)
        self.logger.addHandler(rt_hander)

    def get_log(self):
        """返回logger供调用"""
        return self.logger


log = Logger().get_log()
