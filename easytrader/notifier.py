# -*- coding: utf-8 -*-
"""
ntfy 即时消息通知模块
用于发送交易相关的即时通知
"""
import requests
from typing import Optional
from easytrader.log import logger


class NtfyNotifier:
    """ntfy 消息通知器"""
    
    def __init__(self, server_url: str = None, topic: str = None, token: str = None):
        """
        初始化 ntfy 通知器
        
        :param server_url: ntfy 服务器地址，例如 "https://ntfy.example.com"
        :param topic: ntfy 主题，例如 "mysecrets"
        :param token: Bearer token，例如 "tk_AgQdq7mVBoFD37zQVN29RhuMzNIz2"
        """
        self.server_url = server_url
        self.topic = topic
        self.token = token
        self.enabled = False
        
        if server_url and topic:
            self.enabled = True
            logger.info(f"ntfy 通知已启用: {server_url}/{topic}")
        else:
            logger.info("ntfy 通知未配置，将不发送通知")
    
    def send(self, message: str, title: str = None, priority: str = None, tags: list = None, markdown: bool = True) -> bool:
        """
        发送 ntfy 通知
        
        :param message: 消息内容
        :param title: 消息标题（可选）
        :param priority: 优先级 1-5（可选），5最高
        :param tags: 标签列表（可选），例如 ["warning", "stock"]
        :param markdown: 是否使用 Markdown 格式（默认 True）
        :return: 是否发送成功
        """
        if not self.enabled:
            return False
        
        try:
            url = f"{self.server_url}/{self.topic}"
            headers = {}
            
            # 添加认证token
            if self.token:
                headers["Authorization"] = f"Bearer {self.token}"
            
            # 添加标题 - 需要特殊处理 UTF-8 编码
            # requests 库默认用 latin-1 编码 headers，但 ntfy 支持 UTF-8
            # 解决方法：先用 UTF-8 编码为 bytes，再用 latin-1 解码
            # 这样可以让 UTF-8 字符通过 requests 的 latin-1 编码
            if title:
                headers["Title"] = title.encode('utf-8').decode('latin-1')
            
            # 添加优先级
            if priority:
                headers["Priority"] = str(priority)
            
            # 添加标签
            if tags:
                headers["Tags"] = ",".join(tags)
            
            # 启用 Markdown 格式
            if markdown:
                headers["Markdown"] = "yes"
            
            response = requests.post(url, data=message.encode('utf-8'), headers=headers, timeout=5)
            
            if response.status_code == 200:
                logger.debug(f"ntfy 通知发送成功: {title or message[:50]}")
                return True
            else:
                logger.warning(f"ntfy 通知发送失败: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"发送 ntfy 通知时出错: {str(e)}")
            return False
    
    def notify_trade(self, action: str, security: str, price: float, amount: int, result: str = None):
        """
        发送交易通知
        
        :param action: 交易动作（买入/卖出/市价买入/市价卖出等）
        :param security: 证券代码
        :param price: 价格
        :param amount: 数量
        :param result: 交易结果（可选）
        """
        # ntfy 支持 UTF-8 标题（包括中文和 emoji）
        title = f"📊 交易委托: {action}"
        
        # 使用 Markdown 格式
        message = f"""**证券代码**: `{security}`
**委托价格**: ¥{price:.2f}
**委托数量**: {amount} 股"""
        
        if result:
            message += f"\n**结果**: {result}"
        
        tags = ["chart_with_upwards_trend", "moneybag"]
        priority = "4"  # 高优先级
        
        self.send(message, title=title, priority=priority, tags=tags, markdown=True)
    
    def notify_entrust_success(self, action: str, security: str, price: float, amount: int, entrust_no: str = None):
        """
        发送委托成功通知
        
        :param action: 交易动作
        :param security: 证券代码
        :param price: 价格
        :param amount: 数量
        :param entrust_no: 委托单号
        """
        # ntfy 支持 UTF-8 标题
        title = f"✅ 委托成功: {action}"
        
        # 使用 Markdown 格式
        message = f"""**证券代码**: `{security}`
**成交价格**: ¥{price:.2f}
**成交数量**: {amount} 股"""
        
        if entrust_no:
            message += f"\n**委托单号**: `{entrust_no}`"
        
        message += f"\n\n✅ 委托已成功提交"
        
        tags = ["white_check_mark", "chart_with_upwards_trend"]
        priority = "4"
        
        self.send(message, title=title, priority=priority, tags=tags, markdown=True)
    
    def notify_entrust_failed(self, action: str, security: str, price: float, amount: int, error: str):
        """
        发送委托失败通知
        
        :param action: 交易动作
        :param security: 证券代码
        :param price: 价格
        :param amount: 数量
        :param error: 错误信息
        """
        # ntfy 支持 UTF-8 标题
        title = f"❌ 委托失败: {action}"
        
        # 使用 Markdown 格式
        message = f"""**证券代码**: `{security}`
**委托价格**: ¥{price:.2f}
**委托数量**: {amount} 股

⚠️ **错误信息**:
```
{error}
```"""
        
        tags = ["x", "warning"]
        priority = "5"  # 最高优先级
        
        self.send(message, title=title, priority=priority, tags=tags, markdown=True)
    
    def notify_cancel(self, entrust_no: str, result: str = "success"):
        """
        发送撤单通知
        
        :param entrust_no: 委托单号
        :param result: 撤单结果
        """
        # ntfy 支持 UTF-8 标题
        title = "🔄 撤单操作"
        
        # 使用 Markdown 格式
        status_icon = "✅" if "成功" in result or result.lower() == "success" else "❌"
        message = f"""**委托单号**: `{entrust_no}`
{status_icon} **撤单结果**: {result}"""
        
        tags = ["arrows_counterclockwise"]
        priority = "3"
        
        self.send(message, title=title, priority=priority, tags=tags, markdown=True)
    
    def notify_cancel_all(self, result: str = "success"):
        """
        发送全部撤单通知
        
        :param result: 撤单结果
        """
        # ntfy 支持 UTF-8 标题
        title = "🔄 全部撤单"
        
        # 使用 Markdown 格式
        status_icon = "✅" if "成功" in result or result.lower() == "success" else "❌"
        message = f"""{status_icon} **操作结果**: {result}

⚠️ 已尝试撤销所有未成交委托"""
        
        tags = ["arrows_counterclockwise", "warning"]
        priority = "4"
        
        self.send(message, title=title, priority=priority, tags=tags, markdown=True)
    
    def notify_auto_ipo(self, result: str):
        """
        发送新股申购通知
        
        :param result: 申购结果
        """
        # ntfy 支持 UTF-8 标题
        title = "🎯 新股申购"
        
        # 使用 Markdown 格式
        message = f"""📋 **申购结果**:
{result}

💡 请在交易软件中查看详细申购信息"""
        
        tags = ["dart", "moneybag"]
        priority = "4"
        
        self.send(message, title=title, priority=priority, tags=tags, markdown=True)


# 全局通知器实例
_notifier: Optional[NtfyNotifier] = None


def init_notifier(server_url: str = None, topic: str = None, token: str = None):
    """
    初始化全局通知器
    
    :param server_url: ntfy 服务器地址
    :param topic: ntfy 主题
    :param token: Bearer token
    """
    global _notifier
    _notifier = NtfyNotifier(server_url=server_url, topic=topic, token=token)
    return _notifier


def get_notifier() -> Optional[NtfyNotifier]:
    """
    获取全局通知器实例
    
    :return: NtfyNotifier 实例或 None
    """
    return _notifier