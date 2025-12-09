"""
优化的跟单程序
功能特性：
1. 完整的异常处理和错误恢复
2. 自动重连机制（连接失败后自动重连）
3. 优雅退出（Ctrl+C 信号处理）
4. 详细的日志记录
5. 健康检查和状态监控
"""
import easytrader
from easytrader.log import logger, follow_logger
from easytrader.miniqmt.miniqmt_trader import MiniqmtTrader
from easytrader.xq_follower import XueQiuFollower
import time
import sys
import signal
import threading
from typing import Optional

# ==============================================================================
# 配置部分
# ==============================================================================

# MiniQMT 连接配置
MINIQMT_CONFIG = {
    'miniqmt_path': r"D:\国金QMT交易端模拟\userdata_mini",
    'stock_account': "62500888",
    'reconnect_enabled': True,      # 启用自动重连
    'reconnect_interval': 5,         # 重连间隔（秒）
    'max_reconnect_attempts': 0,     # 最大重连次数，0表示无限重连
}

# 雪球配置
XUEQIU_CONFIG = {
    'cookies': "cookiesu=911741358545830; smidV2=20250307224226891d4776dee78eb8916ec6d39dccc26100de281ff8d605f20; device_id=5ba82b71970b271d37e98b61d26e8eae; s=bp134pqcwo; Hm_lvt_1db88642e346389874251b5a1eded6e3=1741358546,1742048088; u=5974712115; bid=71e7421c8bdd04512ff569539a2640a6_min9hua8; remember=1; xq_a_token=64aca9edbac17928f087765e51a10f5ac84a5656; xqat=64aca9edbac17928f087765e51a10f5ac84a5656; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjU5NzQ3MTIxMTUsImlzcyI6InVjIiwiZXhwIjoxNzY3Mjc0MjEwLCJjdG0iOjE3NjQ3NzI2MTk4MzEsImNpZCI6ImQ5ZDBuNEFadXAifQ.NJdqZhoYBkbgCSyEdpb7ZoF3N6VlPE6AKPCd7fDR7SSv_M_T53MNyeojTIYbxba48iU4RqVxajdpgmFgCFQgCqJDLKadtbgDdhB1ArK8IE-Kd9_VDOkVI2gaUc1XwSvXtSqvMep-hT-otzd0bwMTPbT3VI7E1-T5KA0IeN_R0r3hQW8-J9Qx8SMgAKleDNZw9aqD3aFBGwkDAdvjxFIxAXpkScSbkMGXxU2qdR1hdVKrW1zGfYC-rEi2yZy0EkneAf7pWUCZnXdYItJEQIPuXEYYLMtsMQSGxt676CX9ZtnV1pfU9cPO2s8JFTL9tQK9upK9XSFEDlKAAHAYqgU3vg; xq_r_token=a30379137e3e11d0eaf8fb6eda6c8931f854e968; xq_is_login=1; _c_WBKFRo=2vlqk3EfftMIGBiu188PcEpzGgEbisnsnZNqm9yB; _nb_ioWEgULi=; acw_tc=ac11000117648586588812248e732b4e792ec29739b486e936dfc5d27bdccb; is_overseas=0; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=Fp4C1oqfK09Stw/gU9gv1ijsgkQyrzOYY95GPbg0WLYxxLw346MPKP5dNce3l3wMnp+LLxgChsVG9/RgeGlbPA%3D%3D; ssxmod_itna=1-iqRxR7qQqeqEG0CiDOii=DkAeiOeDXDULqiQGgADFqAPqDHWzOUADODUokDDvd/QBDDuGsy7CqDsnDxiNDA240iDC4eLz4XPWBP8QF8D5xmKnYCgGxAa0k0bKeT89iRsOIstZSp3e_qt4YYonnRDiDB3DbqDyWB05xxGGA4GwDGoD34DiDDPDb_rDALqD7qDF9QWbd6TDm4GW9eGfDDoDY8u3xitYDDUvWeG2tOTCKRThDDNh8FYo2h5hmZFPy6qhPahkOGh=x0UTDBLdeHA=Z1lRP3ckyUk7TfbDzkzDtLntWprhs2ua=PjDr4IuDDhhBxYUis7DNY08W0tD2tQwH/w4D2D8YqKGxe4qmYbnRYxxDGSGAWd8QqGGzydsMLsGYhjDQP_iebh2OYVotyBKSA5yx5Q0Nol4485BGtAnDeiDD; ssxmod_itna2=1-iqRxR7qQqeqEG0CiDOii=DkAeiOeDXDULqiQGgADFqAPqDHWzOUADODUokDDvd/QBDDuGsy7D4DWGe4_Euv=k_QytsD22ihizrZ3WD"
}

# 跟单配置
FOLLOW_CONFIG = {
    'strategies': ["ZH3381319"],      # 跟随的雪球组合
    'initial_assets': 100000,          # 初始资金
    'track_interval': 2,              # 轮询间隔（秒）
    'trade_cmd_expire_seconds': 12000000,   # 交易指令过期时间（秒）
    'cmd_cache': True,                 # 是否缓存已执行指令
    'slippage': 0.0,                   # 滑点设置
}

# ==============================================================================
# 全局变量
# ==============================================================================

# 退出标志
exit_flag = threading.Event()

# 交易客户端和跟单对象
user: Optional[MiniqmtTrader] = None
follower: Optional[XueQiuFollower] = None


# ==============================================================================
# 信号处理函数
# ==============================================================================

def signal_handler(signum, frame):
    """
    处理退出信号（Ctrl+C）
    """
    logger.info("\n收到退出信号，正在优雅退出...")
    follow_logger.info("收到退出信号，准备停止跟单系统")
    
    exit_flag.set()
    
    # 停止自动重连
    if user is not None:
        try:
            user.stop_reconnect()
            logger.info("已停止自动重连")
        except Exception as e:
            logger.error(f"停止自动重连时出错: {e}")
    
    logger.info("程序已安全退出")
    follow_logger.info("跟单系统已停止")
    sys.exit(0)


# ==============================================================================
# 连接管理函数
# ==============================================================================

def connect_miniqmt(max_retry: int = 3) -> MiniqmtTrader:
    """
    连接到 MiniQMT 交易端（带重试机制）
    
    Args:
        max_retry: 最大重试次数
        
    Returns:
        MiniqmtTrader 实例
        
    Raises:
        RuntimeError: 如果连接失败
    """
    trader = easytrader.use('miniqmt')
    
    for attempt in range(1, max_retry + 1):
        try:
            logger.info(f"[尝试 {attempt}/{max_retry}] 正在连接到 MiniQMT...")
            follow_logger.info(f"连接 MiniQMT 第 {attempt} 次尝试")
            
            trader.connect(**MINIQMT_CONFIG)
            
            # 验证连接是否成功（等待最多30秒）
            wait_time = 30
            start_time = time.time()
            while time.time() - start_time < wait_time:
                try:
                    # 尝试获取资金状况来验证连接
                    balance = trader.balance
                    logger.info(f"✓ MiniQMT 连接成功！资金状况: {balance}")
                    follow_logger.info(f"MiniQMT 连接成功，当前资金: {balance}")
                    return trader
                except RuntimeError as e:
                    if "尚未连接" in str(e) or "正在重连" in str(e):
                        # 还在连接中，继续等待
                        time.sleep(1)
                        continue
                    else:
                        raise
            
            logger.warning(f"连接超时，准备重试...")
            
        except Exception as e:
            logger.error(f"✗ 第 {attempt} 次连接失败: {str(e)}")
            follow_logger.error(f"MiniQMT 连接失败 (尝试 {attempt}): {str(e)}")
            
            if attempt < max_retry:
                wait_seconds = 5
                logger.info(f"等待 {wait_seconds} 秒后重试...")
                time.sleep(wait_seconds)
            else:
                error_msg = f"MiniQMT 连接失败，已重试 {max_retry} 次"
                logger.error(error_msg)
                follow_logger.error(error_msg)
                raise RuntimeError(error_msg)
    
    raise RuntimeError("无法连接到 MiniQMT")


def login_xueqiu(max_retry: int = 3) -> XueQiuFollower:
    """
    登录雪球（带重试机制）
    
    Args:
        max_retry: 最大重试次数
        
    Returns:
        XueQiuFollower 实例
        
    Raises:
        RuntimeError: 如果登录失败
    """
    xq_follower = easytrader.follower(platform="xq")
    
    for attempt in range(1, max_retry + 1):
        try:
            logger.info(f"[尝试 {attempt}/{max_retry}] 正在登录雪球...")
            follow_logger.info(f"登录雪球第 {attempt} 次尝试")
            
            xq_follower.login(**XUEQIU_CONFIG)
            
            logger.info("✓ 雪球登录成功！")
            follow_logger.info("雪球登录成功")
            return xq_follower
            
        except Exception as e:
            logger.error(f"✗ 第 {attempt} 次登录失败: {str(e)}")
            follow_logger.error(f"雪球登录失败 (尝试 {attempt}): {str(e)}")
            
            if attempt < max_retry:
                wait_seconds = 3
                logger.info(f"等待 {wait_seconds} 秒后重试...")
                time.sleep(wait_seconds)
            else:
                error_msg = f"雪球登录失败，已重试 {max_retry} 次"
                logger.error(error_msg)
                follow_logger.error(error_msg)
                raise RuntimeError(error_msg)
    
    raise RuntimeError("无法登录雪球")


# ==============================================================================
# 健康检查函数
# ==============================================================================

def check_connection_health(trader: MiniqmtTrader) -> bool:
    """
    检查交易客户端连接健康状态
    
    Args:
        trader: MiniqmtTrader 实例
        
    Returns:
        bool: 连接是否健康
    """
    try:
        # 尝试获取资金状况
        _ = trader.balance
        return True
    except RuntimeError as e:
        if "正在重连" in str(e):
            logger.info("检测到正在重连中...")
            return False
        elif "尚未连接" in str(e):
            logger.warning("检测到连接已断开")
            return False
        else:
            logger.error(f"健康检查异常: {e}")
            return False
    except Exception as e:
        logger.error(f"健康检查出错: {e}", exc_info=True)
        return False


def health_monitor_worker(trader: MiniqmtTrader, interval: int = 60):
    """
    健康监控工作线程
    
    Args:
        trader: MiniqmtTrader 实例
        interval: 检查间隔（秒）
    """
    logger.info(f"启动健康监控线程，检查间隔: {interval} 秒")
    
    consecutive_failures = 0
    max_consecutive_failures = 5
    
    while not exit_flag.is_set():
        try:
            is_healthy = check_connection_health(trader)
            
            if is_healthy:
                if consecutive_failures > 0:
                    logger.info("连接已恢复正常")
                    follow_logger.info("MiniQMT 连接已恢复")
                consecutive_failures = 0
            else:
                consecutive_failures += 1
                logger.warning(f"连接异常 (连续 {consecutive_failures} 次)")
                
                if consecutive_failures >= max_consecutive_failures:
                    logger.error(f"连接持续异常超过 {max_consecutive_failures} 次，建议检查系统")
                    follow_logger.error(f"连接持续异常，已连续失败 {consecutive_failures} 次")
            
            # 等待下次检查
            for _ in range(interval):
                if exit_flag.is_set():
                    break
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"健康监控出错: {e}", exc_info=True)
            time.sleep(5)
    
    logger.info("健康监控线程已退出")


# ==============================================================================
# 主程序
# ==============================================================================

def main():
    """
    主程序入口
    """
    global user, follower
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("=" * 80)
    logger.info("启动优化版跟单程序")
    logger.info("=" * 80)
    follow_logger.info("跟单系统启动")
    
    try:
        # ======================================================================
        # 步骤 1: 连接 MiniQMT
        # ======================================================================
        logger.info("\n[步骤 1/4] 连接 MiniQMT 交易端...")
        user = connect_miniqmt(max_retry=3)
        
        # 显示账户信息
        try:
            balance = user.balance
            position = user.position
            logger.info(f"\n账户资金状况:")
            for b in balance:
                logger.info(f"  总资产: {b.get('total_asset', 'N/A')}")
                logger.info(f"  可用资金: {b.get('cash', 'N/A')}")
                logger.info(f"  持仓市值: {b.get('market_value', 'N/A')}")
            
            logger.info(f"\n当前持仓 (共 {len(position)} 只):")
            for pos in position:
                logger.info(
                    f"  {pos.get('stock_code', 'N/A')}: "
                    f"数量={pos.get('volume', 0)}, "
                    f"可用={pos.get('can_use_volume', 0)}, "
                    f"成本={pos.get('avg_price', 0):.2f}"
                )
            
            follow_logger.info(f"账户总资产: {balance[0].get('total_asset', 0)}, 持仓数: {len(position)}")
            
        except Exception as e:
            logger.warning(f"获取账户信息时出错: {e}")
        
        # ======================================================================
        # 步骤 2: 登录雪球
        # ======================================================================
        logger.info("\n[步骤 2/4] 登录雪球平台...")
        follower = login_xueqiu(max_retry=3)
        
        # ======================================================================
        # 步骤 3: 启动健康监控
        # ======================================================================
        logger.info("\n[步骤 3/4] 启动健康监控...")
        monitor_thread = threading.Thread(
            target=health_monitor_worker,
            args=(user, 60),  # 每60秒检查一次
            daemon=True
        )
        monitor_thread.start()
        
        # ======================================================================
        # 步骤 4: 开始跟单
        # ======================================================================
        logger.info("\n[步骤 4/4] 开始跟单...")
        logger.info(f"跟随策略: {FOLLOW_CONFIG['strategies']}")
        logger.info(f"初始资金: {FOLLOW_CONFIG['initial_assets']}")
        logger.info(f"轮询间隔: {FOLLOW_CONFIG['track_interval']} 秒")
        logger.info(f"指令过期时间: {FOLLOW_CONFIG['trade_cmd_expire_seconds']} 秒")
        logger.info(f"滑点设置: {FOLLOW_CONFIG['slippage'] * 100}%")
        logger.info("-" * 80)
        
        follow_logger.info(
            f"开始跟单 - 策略:{FOLLOW_CONFIG['strategies']}, "
            f"资金:{FOLLOW_CONFIG['initial_assets']}, "
            f"间隔:{FOLLOW_CONFIG['track_interval']}秒"
        )
        
        # 启动跟单（这是一个阻塞调用）
        follower.follow(
            users=user,
            strategies=FOLLOW_CONFIG['strategies'],
            initial_assets=FOLLOW_CONFIG['initial_assets'],
            track_interval=FOLLOW_CONFIG['track_interval'],
            trade_cmd_expire_seconds=FOLLOW_CONFIG['trade_cmd_expire_seconds'],
            cmd_cache=FOLLOW_CONFIG['cmd_cache'],
            slippage=FOLLOW_CONFIG['slippage'],
        )
        
    except KeyboardInterrupt:
        logger.info("\n用户中断程序")
        follow_logger.info("用户手动中断")
        
    except Exception as e:
        logger.error(f"\n程序运行出错: {str(e)}", exc_info=True)
        follow_logger.error(f"程序异常: {str(e)}")
        
    finally:
        # 清理资源
        logger.info("\n正在清理资源...")
        
        if user is not None:
            try:
                user.stop_reconnect()
                logger.info("已停止自动重连")
            except Exception as e:
                logger.error(f"停止重连时出错: {e}")
        
        logger.info("程序已结束")
        follow_logger.info("跟单系统已关闭")


# ==============================================================================
# 程序入口
# ==============================================================================

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"程序启动失败: {str(e)}", exc_info=True)
        follow_logger.error(f"启动失败: {str(e)}")
        sys.exit(1)