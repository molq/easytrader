<!--
 * @Author: wb812225邱洪明
 * @Date: 2025-11-17 21:05:57
 * @LastEditTime: 2025-11-17 21:35:38
 * @LastEditors: wb812225邱洪明
 * @Description: file content
-->

**项目级规则用于帮助 Agent 理解您的代码库和遵循您的项目约定**
1. 本项目使用虚拟环境
创建并激活虚拟环境：

```bash
uv venv --python 3.12
source .venv/bin/activate  # Unix/macOS 系统
# .venv\Scripts\activate  # windows 系统
```

2. 安装依赖：

```bash
uv pip install -r requirements.txt
```

​

3. 执行可编辑模式安装命令

```bash
uv pip install -e .

```


