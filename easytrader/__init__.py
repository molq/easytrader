# -*- coding: utf-8 -*-
import os
import urllib3

from easytrader import exceptions
from easytrader.api import use, follower
from easytrader.log import logger
from easytrader.notifier import init_notifier, get_notifier

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__version__ = "0.23.7"
__author__ = "shidenggui"

# 尝试加载 .env 文件（如果安装了 python-dotenv）
try:
    from dotenv import load_dotenv
    load_dotenv()  # 加载 .env 文件到环境变量
except ImportError:
    # 如果没有安装 python-dotenv，跳过
    pass

# 从环境变量自动初始化 ntfy 通知
_ntfy_server = os.getenv('NTFY_SERVER')
_ntfy_topic = os.getenv('NTFY_TOPIC')
_ntfy_token = os.getenv('NTFY_TOKEN')

if _ntfy_server and _ntfy_topic:
    init_notifier(
        server_url=_ntfy_server,
        topic=_ntfy_topic,
        token=_ntfy_token
    )
    logger.info(f"已从环境变量自动初始化 ntfy 通知: {_ntfy_server}/{_ntfy_topic}")
