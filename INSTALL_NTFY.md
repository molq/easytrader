# ntfy 通知功能快速安装指南

## 问题：配置了 .env 但没有生效？

这是因为需要安装 `python-dotenv` 库来读取 .env 文件。

## 解决方案

### 步骤 1: 安装 python-dotenv

```bash
pip install python-dotenv
```

或者重新安装所有依赖：

```bash
pip install -r requirements.txt
```

### 步骤 2: 确认 .env 文件位置

`.env` 文件需要放在**你运行 Python 脚本的目录**（通常是项目根目录）。

例如，如果你的项目结构是：
```
your_project/
├── .env          # .env 文件应该在这里
├── your_script.py
└── easytrader/
```

### 步骤 3: 配置 .env 文件

编辑 `.env` 文件，添加以下内容：

```bash
NTFY_SERVER=https://ntfy.sh
NTFY_TOPIC=your_unique_topic_name_12345
NTFY_TOKEN=
```

**重要提示**：
- `NTFY_SERVER` 和 `NTFY_TOPIC` 必须同时配置才能启用通知
- `NTFY_TOKEN` 是可选的，如果你的服务器不需要认证可以留空

### 步骤 4: 重启 Python 程序

安装 `python-dotenv` 后，需要重新启动你的 Python 程序。

### 步骤 5: 验证是否生效

运行你的交易程序，检查日志输出。如果看到以下信息说明配置成功：

```
已从环境变量自动初始化 ntfy 通知: https://ntfy.sh/your_unique_topic_name_12345
```

## 测试通知功能

运行测试脚本：

```bash
python tests/test_ntfy_notification.py
```

记得先修改测试脚本中的配置信息。

## 常见问题

### Q: 我已经安装了 python-dotenv，但还是没有生效？

A: 检查以下几点：
1. `.env` 文件是否在正确的位置（运行脚本的目录）
2. `.env` 文件中是否同时配置了 `NTFY_SERVER` 和 `NTFY_TOPIC`
3. 是否重启了 Python 程序
4. 查看程序启动日志，确认是否有 "已从环境变量自动初始化 ntfy 通知" 的信息

### Q: 我不想使用 .env 文件，可以直接设置环境变量吗？

A: 可以！在运行 Python 程序前设置环境变量：

**Windows (cmd):**
```cmd
set NTFY_SERVER=https://ntfy.sh
set NTFY_TOPIC=your_topic
python your_script.py
```

**Windows (PowerShell):**
```powershell
$env:NTFY_SERVER="https://ntfy.sh"
$env:NTFY_TOPIC="your_topic"
python your_script.py
```

**Linux/Mac:**
```bash
export NTFY_SERVER=https://ntfy.sh
export NTFY_TOPIC=your_topic
python your_script.py
```

### Q: 可以不用环境变量，直接在代码中配置吗？

A: 可以！在代码中手动初始化：

```python
import easytrader

# 手动初始化（会覆盖环境变量）
easytrader.init_notifier(
    server_url="https://ntfy.sh",
    topic="your_topic",
    token=None  # 可选
)

# 然后正常使用
user = easytrader.use('ht_client')
user.prepare('ht.json')
user.buy('162411', price=0.55, amount=100)
```

## 需要帮助？

查看完整文档：
- [docs/ntfy_notification.md](docs/ntfy_notification.md) - 详细使用文档
- [NTFY_UPDATE.md](NTFY_UPDATE.md) - 功能更新说明