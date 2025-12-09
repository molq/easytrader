# ntfy 即时消息通知配置指南

## 概述

easytrader 支持通过 ntfy 发送交易相关的即时消息通知，包括：

- 交易委托（买入、卖出、市价买入、市价卖出等）
- 委托成功通知
- 委托失败通知
- 撤单通知
- 全部撤单通知
- 新股申购通知

## 什么是 ntfy？

[ntfy](https://ntfy.sh/) 是一个简单的基于 HTTP 的发布-订阅通知服务。你可以使用公共服务器或自建 ntfy 服务器。

## 配置步骤

### 方式一：使用环境变量（推荐）

easytrader 会自动从环境变量读取 ntfy 配置并启用通知服务。

#### 1. 安装依赖

首先确保已安装 `python-dotenv`：

```bash
pip install python-dotenv
```

或者重新安装 easytrader：

```bash
pip install -r requirements.txt
```

#### 2. 创建 .env 文件

复制 `.env.example` 为 `.env` 并填入配置：

```bash
# ntfy 服务器地址
NTFY_SERVER=https://ntfy.example.com

# ntfy 主题名称
NTFY_TOPIC=my_trade_notifications_a3b9c7d2

# ntfy 访问令牌（可选）
NTFY_TOKEN=tk_AgQdq7mVBoFD37zQVN29RhuMzNIz2
```

**注意**：.env 文件需要放在项目根目录（即运行 Python 脚本的目录）。

#### 3. 直接使用

配置好环境变量后，导入 easytrader 时会自动初始化通知：

```python
import easytrader

# ntfy 通知已自动启用（如果配置了环境变量）
user = easytrader.use('ht_client')
user.prepare('ht.json')

# 执行交易会自动发送通知
user.buy('162411', price=0.55, amount=100)
```

**注意**：
- 只有同时配置了 `NTFY_SERVER` 和 `NTFY_TOPIC` 才会自动启用通知
- `NTFY_TOKEN` 是可选的，如果你的服务器不需要认证可以不设置
- 如果不配置这些环境变量，通知功能不会启用，不影响正常使用

### 方式二：手动初始化

如果不想使用环境变量，也可以在代码中手动初始化：

#### 1. 获取 ntfy 配置信息

你需要以下信息：

- **服务器地址**：例如 `https://ntfy.example.com` 或 `https://ntfy.sh`
- **主题名称**：例如 `mysecrets`（推荐使用随机生成的难以猜测的主题名）
- **访问令牌**（可选）：例如 `tk_AgQdq7mVBoFD37zQVN29RhuMzNIz2`

#### 2. 初始化通知器

在你的交易脚本中，首先初始化 ntfy 通知器：

```python
import easytrader

# 初始化 ntfy 通知器
easytrader.init_notifier(
    server_url="https://ntfy.example.com",  # ntfy 服务器地址
    topic="mysecrets",                       # 主题名称
    token="tk_AgQdq7mVBoFD37zQVN29RhuMzNIz2"  # Bearer token（可选）
)
```

**注意**：
- 手动调用 `init_notifier()` 会覆盖环境变量的配置
- 必须在创建交易实例之前调用 `init_notifier()`

## 使用示例

### 示例 1: 使用环境变量（推荐）

```bash
# .env 文件
NTFY_SERVER=https://ntfy.sh
NTFY_TOPIC=my_trade_notifications_12345
```

```python
import easytrader

# 自动从环境变量初始化，无需手动调用 init_notifier()
user = easytrader.use('ht_client')
user.prepare('ht.json')

# 执行交易（会自动发送通知）
user.buy('162411', price=0.55, amount=100)
```

### 示例 2: 手动初始化

#### 客户端交易（ClientTrader）

```python
import easytrader

# 初始化通知器
easytrader.init_notifier(
    server_url="https://ntfy.sh",
    topic="my_trade_notifications_12345",
    token=None  # 如果使用公共服务器且不需要认证，可以为 None
)

# 创建交易客户端
user = easytrader.use('ht_client')
user.prepare('ht.json')

# 执行交易（会自动发送通知）
user.buy('162411', price=0.55, amount=100)
```

#### MiniQMT 交易

```python
import easytrader

# 初始化通知器
easytrader.init_notifier(
    server_url="https://ntfy.example.com",
    topic="qmt_trades",
    token="tk_your_token_here"
)

# 创建 MiniQMT 交易客户端
user = easytrader.use('miniqmt')
user.connect(
    miniqmt_path=r"D:\国金证券QMT交易端\userdata_mini",
    stock_account="你的资金账号"
)

# 执行交易（会自动发送通知）
user.buy('000001', price=10.5, amount=100)
user.sell('000001', price=11.0, amount=100)
```

#### 雪球交易（XueQiu）

```python
import easytrader

# 初始化通知器
easytrader.init_notifier(
    server_url="https://ntfy.sh",
    topic="xueqiu_trades_abc123"
)

# 创建雪球交易客户端
user = easytrader.use('xq')
user.prepare(
    cookies='你的雪球cookies',
    portfolio_code='ZH123456',
    portfolio_market='cn'
)

# 执行交易（会自动发送通知）
user.buy('SZ000001', price=10.0, amount=100)
```

## 通知内容说明

### 委托通知

当发起交易委托时，会收到类似以下通知：

```
标题: 交易委托: 买入
内容:
证券: 162411
价格: 0.55
数量: 100
```

### 委托成功通知

```
标题: ✅ 委托成功: 买入
内容:
证券: 162411
价格: 0.55
数量: 100
委托单号: 12345
```

### 委托失败通知

```
标题: ❌ 委托失败: 买入
内容:
证券: 162411
价格: 0.55
数量: 100
错误: 资金不足
```

### 撤单通知

```
标题: 🔄 撤单操作
内容:
委托单号: 12345
结果: 成功
```

### 全部撤单通知

```
标题: 🔄 全部撤单
内容:
结果: 成功
```

### 新股申购通知

```
标题: 🎯 新股申购
内容:
结果: 共3只新股，可申购2只
结果: {'message': 'success'}
```

## 高级配置

### 环境变量优先级

1. 如果手动调用 `init_notifier()`，会使用手动设置的配置
2. 如果未手动调用，会自动读取环境变量
3. 如果环境变量也未配置，通知功能不会启用

### 临时禁用通知

如果已配置环境变量但想临时禁用通知：

```python
import easytrader

# 方式1: 不导入或注释掉环境变量
# NTFY_SERVER=  # 留空

# 方式2: 删除 .env 文件或注释掉配置

# 方式3: 在程序中检查
import os
if not os.getenv('ENABLE_NOTIFICATIONS', 'true').lower() == 'true':
    # 不启用通知
    pass
```

## 安全建议

1. **使用随机主题名**：不要使用容易猜测的主题名，如 `mytrades`。建议使用随机字符串，如 `trade_notifications_a3b9c7d2`。

2. **使用访问令牌**：如果你的 ntfy 服务器支持，建议配置访问令牌以提高安全性。

3. **自建 ntfy 服务器**：对于敏感的交易通知，建议自建 ntfy 服务器而不是使用公共服务器。

4. **保护 .env 文件**：
   - 将 `.env` 添加到 `.gitignore`，不要提交到版本控制
   - 确保 `.env` 文件只有你可以读取
   - 使用 `.env.example` 作为配置模板

5. **使用环境变量**：推荐使用环境变量而不是在代码中硬编码配置

## 自建 ntfy 服务器

参考 [ntfy 官方文档](https://docs.ntfy.sh/install/) 了解如何自建 ntfy 服务器。

简单的 Docker 部署示例：

```bash
docker run -d \
  --name ntfy \
  -p 80:80 \
  -v /var/cache/ntfy:/var/cache/ntfy \
  binwiederhier/ntfy \
  serve
```

## 接收通知

### 使用 ntfy 移动应用

1. 下载 ntfy 应用（[iOS](https://apps.apple.com/us/app/ntfy/id1625396347) / [Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy)）
2. 添加订阅，输入你的服务器地址和主题名
3. 开始接收通知

### 使用 Web 界面

访问 `https://你的服务器地址/你的主题名` 即可在浏览器中查看通知。

### 使用命令行

```bash
# 订阅主题
curl -s https://ntfy.example.com/mysecrets/json
```

## 故障排查

### 没有收到通知

1. 检查是否正确调用了 `init_notifier()`
2. 检查服务器地址、主题名和令牌是否正确
3. 检查网络连接是否正常
4. 查看日志中是否有错误信息

### 通知延迟

- ntfy 是一个轻量级服务，通常延迟很低
- 如果使用公共服务器，可能会有一些延迟
- 建议使用自建服务器以获得最佳性能

## 参考资料

- [ntfy 官方网站](https://ntfy.sh/)
- [ntfy 官方文档](https://docs.ntfy.sh/)
- [ntfy GitHub 仓库](https://github.com/binwiederhier/ntfy)