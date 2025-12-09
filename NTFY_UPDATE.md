# ntfy 即时消息通知功能更新说明

## 更新概述

本次更新为 easytrader 添加了 ntfy 即时消息通知功能，可以在所有交易操作时自动发送通知消息。

## 新增功能

### 1. ntfy 通知模块 (`easytrader/notifier.py`)

新增了完整的 ntfy 通知模块，支持：

- 交易委托通知（买入、卖出、市价买入、市价卖出等）
- 委托成功通知
- 委托失败通知
- 撤单通知
- 全部撤单通知
- 新股申购通知

### 2. 集成支持

已在以下交易客户端中集成 ntfy 通知：

- **ClientTrader** (`easytrader/clienttrader.py`)
  - 买入/卖出
  - 市价买入/市价卖出
  - 正回购/逆回购
  - 撤单/全部撤单
  - 新股申购

- **MiniqmtTrader** (`easytrader/miniqmt/miniqmt_trader.py`)
  - 限价买入/卖出
  - 市价买入/卖出
  - 撤单

- **XueQiuTrader** (`easytrader/xqtrader.py`)
  - 买入/卖出
  - 撤单

- **WebTrader** (`easytrader/webtrader.py`)
  - 基础支持（子类继承）

## 使用方法

### 方式一：使用环境变量（推荐）

easytrader 支持从环境变量自动初始化 ntfy 通知服务。

#### 1. 安装依赖

确保已安装 `python-dotenv`：

```bash
pip install python-dotenv
```

或重新安装所有依赖：

```bash
pip install -r requirements.txt
```

#### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填入配置：

```bash
# .env 文件
NTFY_SERVER=https://ntfy.example.com
NTFY_TOPIC=my_trade_notifications_a3b9c7d2
NTFY_TOKEN=tk_AgQdq7mVBoFD37zQVN29RhuMzNIz2
```

**注意**：.env 文件需要放在项目根目录。

#### 3. 直接使用

```python
import easytrader

# ntfy 通知会自动从环境变量初始化
# 无需手动调用 init_notifier()

user = easytrader.use('ht_client')
user.prepare('ht.json')

# 执行交易会自动发送通知
result = user.buy('162411', price=0.55, amount=100)
```

**注意**：
- 只有同时配置了 `NTFY_SERVER` 和 `NTFY_TOPIC` 才会自动启用通知
- `NTFY_TOKEN` 可选，如果服务器不需要认证可以留空
- 如果不配置环境变量，通知功能不会启用，不影响正常使用

### 方式二：手动初始化

如果不想使用环境变量，也可以手动初始化：

```python
import easytrader

# 手动初始化（会覆盖环境变量配置）
easytrader.init_notifier(
    server_url="https://ntfy.example.com",
    topic="mysecrets",
    token="tk_AgQdq7mVBoFD37zQVN29RhuMzNIz2"
)

user = easytrader.use('ht_client')
user.prepare('ht.json')
result = user.buy('162411', price=0.55, amount=100)
```

## 通知示例

### 买入委托通知

```
标题: 交易委托: 买入
内容: 
证券: 162411
价格: 0.55
数量: 100
标签: 📈💰
优先级: 4（高）
```

### 委托成功通知

```
标题: ✅ 委托成功: 买入
内容:
证券: 162411
价格: 0.55
数量: 100
委托单号: 12345
标签: ✅📈
优先级: 4（高）
```

### 委托失败通知

```
标题: ❌ 委托失败: 买入
内容:
证券: 162411
价格: 0.55
数量: 100
错误: 资金不足
标签: ❌⚠️
优先级: 5（最高）
```

## 文件变更清单

### 新增文件
- `easytrader/notifier.py` - ntfy 通知模块
- `docs/ntfy_notification.md` - 详细使用文档
- `tests/test_ntfy_notification.py` - 测试示例
- `.env.example` - 环境变量配置示例
- `NTFY_UPDATE.md` - 本更新说明文档

### 修改文件
- `easytrader/__init__.py` - 添加环境变量自动初始化（使用 python-dotenv），导出 `init_notifier` 和 `get_notifier` 函数
- `requirements.txt` - 添加 `python-dotenv>=0.19.0` 依赖
- `easytrader/clienttrader.py` - 集成 ntfy 通知
- `easytrader/miniqmt/miniqmt_trader.py` - 集成 ntfy 通知
- `easytrader/webtrader.py` - 添加 notifier 支持
- `easytrader/xqtrader.py` - 集成 ntfy 通知

## 特性说明

### 1. 环境变量自动初始化
配置环境变量后，导入 easytrader 时自动初始化通知服务

### 2. 自动通知
所有交易操作会自动发送通知，无需额外代码

### 3. 可选功能
如果不配置环境变量或不调用 `init_notifier()`，通知功能不会启用，不影响现有代码

### 4. 异步发送
通知发送不会阻塞交易操作，即使发送失败也不影响交易

### 5. 详细信息
通知包含完整的交易信息：证券代码、价格、数量、结果等

### 6. emoji 标签
使用 emoji 图标标记不同类型的通知，易于识别

### 7. 优先级设置
- 普通操作：优先级 3
- 重要操作（交易、撤单）：优先级 4
- 错误操作：优先级 5（最高）

## 安全建议

1. **使用随机主题名**：避免使用容易猜测的主题名
2. **配置访问令牌**：使用 Bearer token 保护你的通知
3. **自建服务器**：对于敏感信息，建议自建 ntfy 服务器
4. **保护 .env 文件**：
   - 将 `.env` 添加到 `.gitignore`
   - 确保只有你可以读取 `.env` 文件
   - 不要将 `.env` 提交到版本控制系统
5. **使用 .env.example**：提供配置模板但不包含敏感信息

## 测试

运行测试示例：

```bash
python tests/test_ntfy_notification.py
```

记得先修改测试文件中的配置信息。

## 接收通知

### 移动应用
- iOS: https://apps.apple.com/us/app/ntfy/id1625396347
- Android: https://play.google.com/store/apps/details?id=io.heckel.ntfy

### Web 浏览器
访问 `https://你的服务器地址/你的主题名`

### 命令行
```bash
curl -s https://ntfy.example.com/mysecrets/json
```

## 详细文档

查看完整文档：[docs/ntfy_notification.md](docs/ntfy_notification.md)

## 参考资料

- [ntfy 官方网站](https://ntfy.sh/)
- [ntfy 官方文档](https://docs.ntfy.sh/)
- [ntfy GitHub](https://github.com/binwiederhier/ntfy)

## 兼容性

- 完全向后兼容，不影响现有代码
- 支持所有交易客户端类型
- Python 3.x 兼容
- 需要 requests 库（已包含在依赖中）

## 示例场景

### 场景1: 个人交易监控
使用手机接收所有交易通知，随时随地了解交易状态

### 场景2: 多账户管理
为不同账户配置不同的主题，分别接收通知

### 场景3: 团队协作
团队成员订阅同一主题，共同监控交易操作

### 场景4: 异常告警
配合日志系统，在交易异常时立即收到高优先级通知

---

更新日期: 2025-12-09
版本: easytrader v0.23.7+