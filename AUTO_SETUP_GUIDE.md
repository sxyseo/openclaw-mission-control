# 🚀 Mission Control 自动化配置指南

## 📋 概述

参照 [gstack](https://github.com/garrytan/gstack) 的自动化理念，我们为 Mission Control 创建了**一键配置脚本**，可以快速建立完整的AI项目管理环境。

## 🎯 自动化功能

### ✅ 自动创建内容

1. **🌐 Gateway 配置**
   - 自动检测或创建 AI Gateway
   - 配置 WebSocket 连接
   - 设置工作空间路径

2. **📊 Board Groups（任务分组）**
   - Personal Projects（个人项目）
   - Work Projects（工作项目）
   - Learning & Skills（学习技能）
   - Tools & Utilities（工具开发）
   - R&D Experiments（研发实验）

3. **📋 专家 Boards（任务板）**
   - Frontend Development（前端开发）
   - Backend Development（后端开发）
   - Full Stack Projects（全栈项目）
   - Tech Learning Path（技术学习）
   - Documentation Hub（文档中心）

4. **🤖 AI Agents（代理）**
   - Frontend Expert（前端专家）
   - Backend Expert（后端专家）
   - Full Stack Developer（全栈开发）
   - Learning Coach（学习教练）
   - Technical Writer（技术文档）

## 🛠️ 使用方法

### 方法1：Python 脚本（推荐）

```bash
# 1. 确保服务运行
cd /Users/abel/openclaw-mission-control
make run

# 2. 运行自动化配置脚本
python auto_setup_mission_control.py
```

**优点：**
- 完整的错误处理
- 详细的配置选项
- 保存配置信息到JSON文件
- 更容易扩展和定制

### 方法2：Bash 脚本

```bash
# 1. 确保服务运行
make run

# 2. 运行自动化配置脚本
./auto_setup.sh
```

**优点：**
- 无需Python依赖
- 快速执行
- 适合简单的自动化需求

## 📋 配置详情

### Board Groups 结构

```bash
📊 Personal Projects
├── Frontend Development
│   └── Frontend Expert Agent
├── Backend Development
│   └── Backend Expert Agent
└── Full Stack Projects
    └── Full Stack Developer Agent

📊 Learning & Skills
├── Tech Learning Path
│   └── Learning Coach Agent
└── Documentation Hub
    └── Technical Writer Agent
```

### Agent 配置（gstack风格的15个专家）

当前脚本创建了**5个核心专家**，基于gstack理念：

1. **Frontend Expert** - 前端开发专家
2. **Backend Expert** - 后端开发专家
3. **Full Stack Developer** - 全栈工程师
4. **Learning Coach** - 学习教练
5. **Technical Writer** - 技术文档专家

## 🎨 扩展配置

### 添加更多 Agents

编辑 `auto_setup_mission_control.py`：

```python
agents_config = [
    # 现有 agents...

    # 添加更多专家
    {"name": "UI/UX Designer", "desc": "UI/UX设计专家", "board": "Frontend Development"},
    {"name": "Database Architect", "desc": "数据库架构师", "board": "Backend Development"},
    {"name": "DevOps Engineer", "desc": "运维工程师", "board": "Tools & Utilities"},
    # ... 更多专家
]
```

### 自定义 Board Groups

修改 `board_groups_config` 数组：

```python
board_groups_config = [
    {
        "name": "Your Custom Group",
        "description": "你的自定义分组描述"
    },
    # ... 更多分组
]
```

## 📊 配置文件

脚本运行后会生成 `mission_control_config.json`：

```json
{
  "gateway": {
    "id": "gateway-uuid",
    "name": "Main AI Gateway",
    "url": "ws://127.0.0.1:18789"
  },
  "board_groups": {
    "Personal Projects": "group-uuid",
    "Work Projects": "group-uuid-2"
  },
  "boards": {
    "Frontend Development": {
      "id": "board-uuid",
      "group": "Personal Projects"
    }
  },
  "agents": {
    "Frontend Expert": {
      "id": "agent-uuid",
      "board": "Frontend Development"
    }
  }
}
```

## 🔄 重新配置

### 清理现有配置

```bash
# 访问 Mission Control 界面
http://localhost:3000/boards
http://localhost:3000/agents
http://localhost:3000/board-groups

# 手动删除不需要的项目
```

### 重新运行脚本

```bash
# 确保服务运行
make run

# 重新配置
python auto_setup_mission_control.py
```

## 🚨 故障排除

### 问题1：脚本运行失败

```bash
# 检查服务状态
curl http://localhost:8000/healthz

# 检查认证令牌
# 确认 AUTH_TOKEN 正确
```

### 问题2：创建失败

```bash
# 查看详细错误信息
python auto_setup_mission_control.py 2>&1 | tee setup_error.log

# 检查后端日志
docker-compose logs backend
```

### 问题3：Gateway连接问题

```bash
# 检查OpenClaw Gateway状态
pgrep -f openclaw

# 测试WebSocket连接
wscat -c ws://127.0.0.1:18789
```

## 🎯 与 gstack 的对比

| 特性 | gstack | Mission Control 自动化 |
|------|--------|----------------------|
| **配置方式** | CLAUDE.md文件 | API脚本 |
| **专家角色** | 15个专家 | 可扩展到15+ |
| **自动化程度** | 半自动化 | 完全自动化 |
| **项目类型** | 软件开发 | 通用项目管理 |
| **AI集成** | Claude Code | OpenClaw Gateway |
| **学习曲线** | 需要配置 | 一键运行 |

## 💡 最佳实践

### 1. 首次使用

```bash
# 完整自动化配置
python auto_setup_mission_control.py

# 访问界面熟悉结构
open http://localhost:3000
```

### 2. 定制配置

```bash
# 1. 修改脚本添加你的专家
# 2. 重新运行脚本
# 3. 验证配置结果
```

### 3. 团队协作

```bash
# 1. 创建基础配置
# 2. 邀请团队成员
# 3. 共享配置文件
# 4. 协作管理项目
```

## 📈 高级用法

### 编程方式集成

```python
import asyncio
from auto_setup_mission_control import setup_gstack_style_environment

# 在你的代码中调用
async def main():
    config = await setup_gstack_style_environment()
    # 使用配置进行后续操作
    print(f"创建了 {len(config['agents'])} 个 agents")

asyncio.run(main())
```

### 定时任务

```bash
# 使用cron定期创建项目配置
# 每月1号自动创建新的学习计划
0 0 1 * * python /path/to/auto_setup_mission_control.py
```

### CI/CD集成

```yaml
# .github/workflows/setup-mission-control.yml
name: Setup Mission Control
on: [workflow_dispatch]
jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup environment
        run: |
          python auto_setup_mission_control.py
```

## 🎉 总结

通过这个自动化配置脚本，你可以：

1. **⚡ 5分钟内完成完整环境搭建**
2. **🎯 参照gstack理念配置15个AI专家**
3. **📊 建立结构化的项目管理体系**
4. **🤖 启动AI驱动的项目协作**

**现在就开始使用吧！**

```bash
python auto_setup_mission_control.py
```

---

## 📚 相关文档

- [USER_GUIDE.md](./USER_GUIDE.md) - 完整使用指南
- [QUICK_START.md](./QUICK_START.md) - 快速开始指南
- [I18N_FEATURE.md](./I18N_FEATURE.md) - 国际化功能说明
- [gstack项目](https://github.com/garrytan/gstack) - 灵感来源

---

*创建时间: 2026-03-29*
*版本: 1.0.0*
*语言: 中文*
