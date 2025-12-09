# miniqmt

miniqmt 是券商官方的低门槛 Python 量化交易接口，基于券商的讯投 QMT 服务。详情可以[进群](https://easytrader.readthedocs.io/zh-cn/master/#_2)交流。

## 安装 miniqmt 组件

miniqmt 功能依赖 `xtquant` 库，因为这个库比较大(100 MB+)，所以需要单独安装

```python
pip install easytrader[miniqmt]
``` 

## 引入

```python
import easytrader
```

## 初始化客户端

```python
user = easytrader.use('miniqmt')
```

## 连接 QMT 客户端

需要通过 `connect` 方法连接到 QMT 客户端。

**注意：登录 QMT 客户端时必须勾选极简模式/独立交易模式，否则无法连接**

```python
user.connect(
    miniqmt_path=r"D:\国金证券QMT交易端\userdata_mini",  # QMT 客户端下的 miniqmt 安装路径
    stock_account="你的资金账号",  # 资金账号
    trader_callback=None,  # 默认使用 `easytrader.miniqmt.DefaultXtQuantTraderCallback`
    reconnect_enabled=True,  # 是否启用自动重连，默认 True
    reconnect_interval=5,  # 重连间隔（秒），默认 5 秒
    max_reconnect_attempts=0,  # 最大重连次数，0 表示无限重连，默认 0
)
```

**参数说明：**

- `miniqmt_path`: QMT 客户端下的 miniqmt 安装路径，例如 `r"D:\国金证券QMT交易端\userdata_mini"`
    - 注意：不建议安装在 C 盘。在 C 盘每次都需要用管理员权限运行客户端，才能正常连接
- `stock_account`: 资金账号
- `trader_callback`: 交易回调对象，默认使用 `easytrader.miniqmt.DefaultXtQuantTraderCallback`
- `reconnect_enabled`: 是否启用自动重连功能，默认为 `True`
- `reconnect_interval`: 重连间隔时间（秒），默认为 `5` 秒
- `max_reconnect_attempts`: 最大重连次数，`0` 表示无限重连，默认为 `0`

### 自动重连功能

从最新版本开始，easytrader 为 miniqmt 添加了自动重连功能。当连接断开时，系统会自动尝试重新连接。

**功能特点：**

- 连接断开时自动触发重连
- 可配置重连间隔和最大重连次数
- 详细的日志输出，方便排查连接问题
- 线程安全，不会阻塞主程序

**使用示例：**

```python
# 启用自动重连（默认配置）
user.connect(
    miniqmt_path=r"D:\国金证券QMT交易端\userdata_mini",
    stock_account="你的资金账号",
)

# 自定义重连配置
user.connect(
    miniqmt_path=r"D:\国金证券QMT交易端\userdata_mini",
    stock_account="你的资金账号",
    reconnect_enabled=True,  # 启用自动重连
    reconnect_interval=10,  # 每10秒重连一次
    max_reconnect_attempts=10,  # 最多重连10次
)

# 禁用自动重连
user.connect(
    miniqmt_path=r"D:\国金证券QMT交易端\userdata_mini",
    stock_account="你的资金账号",
    reconnect_enabled=False,  # 禁用自动重连
)

# 手动停止自动重连
user.stop_reconnect()
```

**日志输出示例：**

```
INFO - 正在连接到 MiniQMT...
INFO - MiniQMT 路径: D:\国金证券QMT交易端\userdata_mini
INFO - 资金账号: 1234567890
INFO - 自动重连: 启用
INFO - 重连间隔: 5 秒
INFO - 最大重连次数: 无限
INFO - 创建 XtQuantTrader 实例，会话ID: 123456
INFO - 正在尝试连接...
INFO - ✓ 成功连接到 MiniQMT, 账号: 1234567890
INFO - ✓ 已订阅账户: 1234567890

# 当连接断开时
WARNING - MiniQMT 连接已断开
INFO - 准备触发自动重连...
WARNING - 第 1 次重连尝试 (间隔 5 秒)...
INFO - 正在连接到 MiniQMT...
INFO - ✓ 成功连接到 MiniQMT, 账号: 1234567890
INFO - 重连成功！
```

## 交易相关

### 获取资金状况

```python
user.balance

# return
# qmt 官网文档 https://dict.thinktrader.net/nativeApi/xttrader.html?id=7zqjlm#%E8%B5%84%E4%BA%A7xtasset
[{
  'total_asset': 1000000.0,  # 总资产
  'market_value': 400000.0,  # 持仓市值
  'cash': 600000.0,  # 可用资金
  'frozen_cash': 0.0,  # 冻结资金
  'account_type': 2,  # 账户类型
  'account_id': '你的资金账号'  # 账户ID
}]
```

### 获取持仓

```python
user.position

# return
# qmt 官网文档 https://dict.thinktrader.net/nativeApi/xttrader.html?id=7zqjlm#%E6%8C%81%E4%BB%93xtposition
[{'security': '162411',
  'stock_code': '162411.SZ',
  'volume': 100,
  'can_use_volume': 100,
  'open_price': 0.618,
  'market_value': 63.8,
  'frozen_volume': 0,
  'on_road_volume': 0,
  'yesterday_volume': 100,
  'avg_price': 0.618,
  'direction': 48,
  'account_type': 2,
  'account_id': '1111111111'}]

```

### 限价买入

```python
user.buy('600036', price=35.5, amount=100)

# return
{'entrust_no': 123456}
```

**注意事项**

- 成功发送委托后的订单编号为大于 0 的正整数，如果为 -1 表示委托失败，失败具体原因请查看 `DefaultXtQuantTraderCallback.on_order_error` 回调
- 注：非交易时间下单可以拿到订单编号，但 `on_order_error` 回调会报错：
  ```
  下单失败回调: order_id=10231, error_id=-61, error_msg=限价买入 [SZ162411] [COUNTER] [12313][当前时间不允许此类证券交易]
  ```

### 限价卖出

```python
user.sell('600036', price=36.0, amount=100)

# return
{'entrust_no': 123456}
```

### 市价买入

```python
user.market_buy('600036', amount=100, ttype='对手方最优价格委托')

# return
{'entrust_no': 123456}
```

**市价委托类型（ttype）可选值**:

深市可选:

- 对手方最优价格委托（默认）
- 本方最优价格委托
- 即时成交剩余撤销委托
- 最优五档即时成交剩余撤销
- 全额成交或撤销委托

沪市可选:

- 对手方最优价格委托（默认）
- 最优五档即时成交剩余撤销
- 最优五档即时成交剩转限价
- 本方最优价格委托

### 市价卖出

```python
user.market_sell('600036', amount=100, ttype='对手方最优价格委托')

# return
{'entrust_no': 123456}
```

### 撤单

```python
user.cancel_entrust(123456)  # 传入之前买入或卖出时返回的订单编号

# return
{'success': True, 'message': 'success'} # 成功
{'success': False, 'message': 'failed'} # 失败
```

### 查询当日委托

```python
user.today_entrusts

# return
# qmt 官网文档 https://dict.thinktrader.net/nativeApi/xttrader.html?id=7zqjlm#%E5%A7%94%E6%89%98xtorder
[{'security': '162411',
  'stock_code': '162411.SZ',
  'order_id': 3456,
  'order_sysid': '1111',
  'order_time': 1634278451,
  'order_type': 23,
  'order_type_name': '买入', # ['买入', '卖出']
  'order_volume': 100,
  'price_type': 50,
  'price_type_name': '限价',
  'price': 0.62,
  'traded_volume': 100,
  'traded_price': 0.613,
  'order_status': 56,
  'order_status_name': '已成', # ['已报', '已成', '部成', '已撤', '部撤']
  'status_msg': '',
  'offset_flag': 48,
  'offset_flag_name': '买入', # ['买入', '卖出']
  'strategy_name': '',
  'order_remark': '',
  'direction': 48,
  'direction_name': '多', # ['多', '空']
  'account_type': 2,
  'account_id': '1111111111'}]
```

### 查询当日成交

```python
user.today_trades

# return
# qmt 官网文档 https://dict.thinktrader.net/nativeApi/xttrader.html?id=7zqjlm#%E6%88%90%E4%BA%A4xttrade
[{'security': '162411',
  'stock_code': '162411.SZ',
  'traded_id': '0303222200422222',
  'traded_time': 1634278451,
  'traded_price': 0.613,
  'traded_volume': 100,
  'traded_amount': 61.3,
  'order_id': 1111,
  'order_type': 23,
  'order_type_name': '买入',
  'offset_flag': 48,
  'offset_flag_name': '买入',
  'account_id': '1111111111',
  'account_type': 2,
  'order_sysid': '1111',
  'strategy_name': '',
  'order_remark': ''}]
```


## 进阶功能

### 获取原始交易对象

通过获取原始对象，可以直接调用 miniqmt 的接口进行更多高级操作，具体请参考 [miniqmt 官方文档](https://dict.thinktrader.net/nativeApi/xttrader.html)

```python
# 获取 XtQuantTrader 对象
trader = user.trader

# 获取 StockAccount 对象
account = user.account
```


### 2. 交易回调处理

MiniqmtTrader 默认使用 `DefaultXtQuantTraderCallback` 类处理交易回调，但您可以通过继承 `XtQuantTraderCallback` 类来创建自定义回调处理：

```python
from xtquant.xttrader import XtQuantTraderCallback

class MyTraderCallback(XtQuantTraderCallback):
    def on_disconnected(self):
        print("连接断开")

    def on_account_status(self, status):
        print(f"账户状态: {status.account_id}, 状态: {status.status}")

    def on_stock_order(self, order):
        print(f"委托回调: {order.stock_code}, 状态: {order.order_status}")

    def on_stock_trade(self, trade):
        print(f"成交回调: {trade.stock_code}, 价格: {trade.traded_price}")

    def on_order_error(self, order_error):
        print(f"下单失败: {order_error.order_id}, 错误: {order_error.error_msg}")

    def on_cancel_error(self, cancel_error):
        print(f"撤单失败: {cancel_error.order_id}, 错误: {cancel_error.error_msg}")

# 连接时使用自定义回调
user.connect(
    miniqmt_path=r"D:\国金证券QMT交易端\userdata_mini",
    stock_account="你的资金账号",
    trader_callback=MyTraderCallback()
)
```