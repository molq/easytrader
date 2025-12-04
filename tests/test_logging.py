# -*- coding: utf-8 -*-
"""
日志系统测试脚本
测试新的日志记录功能，包括主日志、跟单日志和交易日志
"""
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from easytrader.log import logger, follow_logger, trade_logger


def test_basic_logging():
    """测试基础日志功能"""
    print("\n=== 测试基础日志功能 ===")
    
    logger.info("这是主日志的INFO消息")
    logger.warning("这是主日志的WARNING消息")
    logger.error("这是主日志的ERROR消息")
    
    print("\n主日志测试完成")


def test_follow_logging():
    """测试跟单日志功能"""
    print("\n=== 测试跟单日志功能 ===")
    
    follow_logger.info("跟单系统登录成功")
    follow_logger.info("开始跟踪雪球策略: 测试策略 (ID:ZH123456 资产:100000.00)")
    follow_logger.info("策略[测试策略] 新指令 - 股票:sh600000 动作:buy 数量:1000 价格:10.50 时间:2024-01-01 10:00:00")
    follow_logger.info("策略[测试策略] 指令执行成功 - 股票:sh600000 动作:buy 数量:1000 价格:10.55 结果:{'entrust_no': '123456'}")
    follow_logger.warning("策略[测试策略] 指令超时被丢弃 - 股票:sh600001 动作:sell 超时:130.5秒")
    follow_logger.error("策略[测试策略] 指令执行失败 - 股票:sh600002 动作:buy 数量:1000 价格:15.20 错误:资金不足")
    
    print("跟单日志测试完成")


def test_trade_logging():
    """测试交易日志功能"""
    print("\n=== 测试交易日志功能 ===")
    
    trade_logger.info("自动登录成功")
    trade_logger.info("买入 - 证券:sh600000 价格:10.50 数量:1000")
    trade_logger.info("买入结果 - 证券:sh600000 结果:{'entrust_no': '123456'}")
    trade_logger.info("卖出 - 证券:sh600001 价格:15.80 数量:500")
    trade_logger.info("卖出结果 - 证券:sh600001 结果:{'entrust_no': '123457'}")
    trade_logger.info("撤单操作 - 委托号:123456 结果:{'message': 'success'}")
    trade_logger.warning("撤单失败 - 委托号:123458 原因:委托单状态错误不能撤单")
    trade_logger.info("新股申购 - 共3只新股，可申购2只")
    trade_logger.info("新股申购结果: {'message': 'success'}")
    
    print("交易日志测试完成")


def test_log_files_created():
    """检查日志文件是否创建"""
    print("\n=== 检查日志文件 ===")
    
    log_dir = "logs"
    expected_files = [
        "easytrader.log",
        "follow.log",
        "trade.log"
    ]
    
    if not os.path.exists(log_dir):
        print(f"错误: 日志目录 {log_dir} 不存在")
        return False
    
    all_exist = True
    for filename in expected_files:
        filepath = os.path.join(log_dir, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"✓ {filename} 已创建 (大小: {size} 字节)")
        else:
            print(f"✗ {filename} 未找到")
            all_exist = False
    
    return all_exist


def main():
    """主测试函数"""
    print("=" * 60)
    print("日志系统测试")
    print("=" * 60)
    
    # 执行各项测试
    test_basic_logging()
    test_follow_logging()
    test_trade_logging()
    
    # 检查日志文件
    if test_log_files_created():
        print("\n" + "=" * 60)
        print("所有测试通过！")
        print("=" * 60)
        print("\n日志文件位置:")
        print(f"  主日志: logs/easytrader.log")
        print(f"  跟单日志: logs/follow.log")
        print(f"  交易日志: logs/trade.log")
        print("\n提示: 可以打开这些文件查看详细的日志内容")
    else:
        print("\n" + "=" * 60)
        print("警告: 部分日志文件未创建")
        print("=" * 60)


if __name__ == "__main__":
    main()