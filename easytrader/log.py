# -*- coding: utf-8 -*-
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


class LogManager:
    """日志管理器，提供统一的日志配置和管理"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # 创建logs目录
        self.log_dir = "logs"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # 日志格式
        self.detail_fmt = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(name)s] %(filename)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.simple_fmt = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # 创建各类日志记录器
        self.logger = self._setup_logger("easytrader", "easytrader.log")
        self.follow_logger = self._setup_logger("easytrader.follow", "follow.log", simple=True)
        self.trade_logger = self._setup_logger("easytrader.trade", "trade.log", simple=True)
        
        self._initialized = True
    
    def _setup_logger(self, name, filename, simple=False):
        """
        设置日志记录器
        :param name: 日志记录器名称
        :param filename: 日志文件名
        :param simple: 是否使用简单格式（用于跟单和交易日志）
        :return: 配置好的logger对象
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.propagate = False
        
        # 清除已有的handlers
        logger.handlers.clear()
        
        # 文件处理器 - 使用RotatingFileHandler实现日志轮转
        log_file = os.path.join(self.log_dir, filename)
        fh = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=10,
            encoding='utf-8'
        )
        fh.setLevel(logging.INFO)
        fh.setFormatter(self.simple_fmt if simple else self.detail_fmt)
        logger.addHandler(fh)
        
        # 控制台处理器（仅主logger输出到控制台）
        if name == "easytrader":
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(self.detail_fmt)
            logger.addHandler(ch)
        
        return logger
    
    def get_logger(self):
        """获取主日志记录器"""
        return self.logger
    
    def get_follow_logger(self):
        """获取跟单日志记录器"""
        return self.follow_logger
    
    def get_trade_logger(self):
        """获取交易日志记录器"""
        return self.trade_logger


# 创建全局日志管理器实例
_log_manager = LogManager()

# 导出主logger（保持向后兼容）
logger = _log_manager.get_logger()

# 导出专用logger
follow_logger = _log_manager.get_follow_logger()
trade_logger = _log_manager.get_trade_logger()


def get_logger():
    """获取主日志记录器"""
    return logger


def get_follow_logger():
    """获取跟单日志记录器"""
    return follow_logger


def get_trade_logger():
    """获取交易日志记录器"""
    return trade_logger
