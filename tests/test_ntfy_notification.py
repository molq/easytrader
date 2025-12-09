# -*- coding: utf-8 -*-
"""
ntfy 通知功能测试示例

注意：此测试需要配置有效的 ntfy 服务器信息才能运行
"""
import easytrader


def test_ntfy_notification():
    """
    测试 ntfy 通知功能
    
    使用前请修改以下配置：
    - NTFY_SERVER: 你的 ntfy 服务器地址
    - NTFY_TOPIC: 你的主题名称
    - NTFY_TOKEN: 你的访问令牌（可选）
    """
    
    # 配置信息（请修改为你自己的）
    NTFY_SERVER = "https://ntfy.sh"  # 或使用你自己的服务器
    NTFY_TOPIC = "test_easytrader_12345"  # 请使用唯一的主题名
    NTFY_TOKEN = None  # 如果需要认证，填入你的 token
    
    # 初始化通知器
    print("初始化 ntfy 通知器...")
    easytrader.init_notifier(
        server_url=NTFY_SERVER,
        topic=NTFY_TOPIC,
        token=NTFY_TOKEN
    )
    print(f"通知器已初始化: {NTFY_SERVER}/{NTFY_TOPIC}")
    
    # 获取通知器实例并测试发送
    notifier = easytrader.get_notifier()
    
    if notifier and notifier.enabled:
        print("\n开始发送测试通知...")
        
        # 测试1: 发送简单消息
        print("1. 发送简单消息...")
        notifier.send("这是一条测试消息", title="测试", priority="3")
        
        # 测试2: 发送交易委托通知
        print("2. 发送交易委托通知...")
        notifier.notify_trade("买入", "000001", 10.5, 100)
        
        # 测试3: 发送委托成功通知
        print("3. 发送委托成功通知...")
        notifier.notify_entrust_success("买入", "000001", 10.5, 100, "12345")
        
        # 测试4: 发送委托失败通知
        print("4. 发送委托失败通知...")
        notifier.notify_entrust_failed("卖出", "000001", 11.0, 100, "资金不足")
        
        # 测试5: 发送撤单通知
        print("5. 发送撤单通知...")
        notifier.notify_cancel("12345", "成功")
        
        # 测试6: 发送全部撤单通知
        print("6. 发送全部撤单通知...")
        notifier.notify_cancel_all("成功")
        
        # 测试7: 发送新股申购通知
        print("7. 发送新股申购通知...")
        notifier.notify_auto_ipo("共3只新股，可申购2只")
        
        print("\n✅ 所有测试通知已发送！")
        print(f"请在 ntfy 应用或网页 {NTFY_SERVER}/{NTFY_TOPIC} 中查看通知")
    else:
        print("❌ 通知器未启用或初始化失败")


if __name__ == "__main__":
    test_ntfy_notification()