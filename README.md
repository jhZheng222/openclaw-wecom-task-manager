# WeCom Task Manager - 企业微信任务管理技能

[![Version](https://img.shields.io/badge/version-1.5.0-blue.svg)](https://github.com/jhZheng222/openclaw-wecom-task-manager)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-OpenClaw-orange.svg)](https://github.com/openclaw/openclaw)

**企业微信智能表格驱动的任务管理技能，支持自动初始化表格、目标分解、任务追踪、并发控制和访问控制。**

> 🎉 **v1.5.0 新增**：多系统支持、环境变量配置、表格自动初始化优化！

---

## 🎯 功能特性

### 核心功能
- ✅ **多系统支持** - 可在任意 OpenClaw 系统中使用（v1.5.0 新增）
- ✅ **表格自动初始化** - 首次使用自动创建完整表格结构
- ✅ **任务全生命周期管理** - 创建、开始、更新、完成
- ✅ **目标分解** - 将大目标分解为可执行任务
- ✅ **依赖管理** - 支持任务依赖关系
- ✅ **智能推荐** - 自动推荐下一个可执行任务
- ✅ **并发控制** - 限制同时进行的任务数量
- ✅ **访问控制** - 白名单机制，保护敏感数据
- ✅ **到期提醒** - 自动检查即将到期和超期任务
- ✅ **统计分析** - 多维度任务统计

### 技术特性
- 🌐 **多系统支持** - 配置驱动，任意 OpenClaw 系统可用（v1.5.0 新增）
- 🔧 **环境变量支持** - OPENCLAW_WORKSPACE、MCPORTER_PATH（v1.5.0 新增）
- 📊 **企业微信集成** - 使用企业微信智能表格存储
- 🔒 **访问控制** - 白名单机制，支持自定义 agents
- ⚡ **并发限制** - 可配置的最大并发任务数
- 🔄 **重试机制** - API 调用失败自动重试
- 📝 **配置驱动** - 独立配置文件，无需修改代码
- 🧪 **完整测试** - 100% 测试覆盖
- 🚀 **开箱即用** - 自动初始化表格，无需手动配置字段

---

## 📦 安装

### 方式 1：从 ClawHub 安装（推荐）

```bash
clawhub install wecom-task-manager
```

### 方式 2：从 GitHub 安装

```bash
git clone https://github.com/jhZheng222/openclaw-wecom-task-manager.git
cd openclaw-wecom-task-manager
cp -r . ~/.openclaw/skills/wecom-task-manager/
```

### 方式 3：手动安装

1. 下载 [最新发布版本](https://github.com/jhZheng222/openclaw-wecom-task-manager/releases)
2. 解压到 `~/.openclaw/skills/wecom-task-manager/`
3. 配置 `config.json`

---

## 🔧 快速开始

### 步骤 1：安装技能

```bash
# 从 ClawHub 安装
clawhub install wecom-task-manager
```

### 步骤 2：配置企业微信表格

**完整配置模板**（复制并修改）：

```json
{
  "accessControl": {
    "enabled": true,
    "allowedAgents": [
      "da-yan",
      "techlead",
      "opsdirector",
      "investment_coordinator",
      "general_coordinator"
    ]
  },
  "concurrency": {
    "maxConcurrentTasks": 3
  },
  "retry": {
    "maxRetries": 3,
    "backoffSeconds": 2
  },
  "enterpriseWeChat": {
    "docId": "YOUR_DOC_ID_HERE",
    "sheetId": "YOUR_SHEET_ID_HERE"
  }
}
```

**获取 docId/sheetId**：
1. 打开企业微信智能表格
2. 复制 URL：`https://doc.weixin.qq.com/smartsheet/s3_AU4AGgYSAFgCNIF2EpD1QTlGcye55?scode=...`
3. `s3_` 后面的部分是 **docId**（如 `AU4AGgYSAFgCNIF2EpD1QTlGcye55`）
4. 表格 ID 是 **sheetId**（从 URL 的 `?tab=` 参数获取，或使用第一个子表的 ID）

**环境变量支持**（可选）：
```bash
# 自定义工作区路径
export OPENCLAW_WORKSPACE=/path/to/your/workspace

# 自定义 mcporter 路径
export MCPORTER_PATH=/path/to/mcporter
```

### 步骤 3：配置访问控制

编辑 `config.json`：
```json
{
  "accessControl": {
    "enabled": true,
    "allowedAgents": [
      "da-yan",
      "techlead",
      "opsdirector",
      "investment_coordinator",
      "general_coordinator"
    ]
  }
}
```

### 步骤 4：初始化表格（可选）

**v1.4.0+** 会自动初始化，你也可以手动执行：

```bash
cd ~/.openclaw/skills/wecom-task-manager/scripts

# 检查表格状态
python3 table_initializer.py check

# 初始化表格（添加缺失字段）
python3 table_initializer.py init
```

### 步骤 5：测试技能

```bash
cd ~/.openclaw/skills/wecom-task-manager/scripts
AGENT_ID="da-yan" python3 task_manager.py list
```

**⚠️ 安全提示**：
- `config.json` 包含敏感信息，已添加到 `.gitignore`
- 不要将 `config.json` 提交到 Git
- 使用 `config.template.json` 作为模板

---

## 📚 使用方式

**详细使用指南**: [USAGE.md](USAGE.md)

### CLI 命令

```bash
# 列出所有任务
python3 task_manager.py list

# 创建任务
python3 task_manager.py create TASK-001 "系统性能分析" 开发

# 开始任务
python3 task_manager.py start TASK-001

# 更新进度
python3 task_manager.py progress TASK-001 50

# 完成任务
python3 task_manager.py complete TASK-001

# 查看统计
python3 task_manager.py stats

# 检查到期任务
python3 task_manager.py due 7
```

### Python API

```python
from task_manager import create_task, start_task, complete_task

# 创建任务
result = create_task(
    task_id="TASK-001",
    task_name="系统性能分析",
    task_type="开发",
    priority="P0",
    agent_id="techlead"
)

# 开始任务
start_task("TASK-001", agent_id="techlead")

# 完成任务
complete_task("TASK-001", agent_id="techlead")
```

---

## 📋 配置文件

**位置**: `config.json`

### 核心配置

```json
{
  "accessControl": {
    "enabled": true,
    "allowedAgents": ["da-yan", "techlead", "opsdirector"]
  },
  "concurrency": {
    "maxConcurrentTasks": 3
  },
  "retry": {
    "maxRetries": 3,
    "backoffSeconds": 2
  },
  "enterpriseWeChat": {
    "docId": "xxx",
    "sheetId": "xxx"
  }
}
```

**详细配置文档**: [配置指南](docs/config-guide.md)

---

## 🎯 典型使用场景

### 场景 1：心跳检查自动推动

```python
from task_manager import get_next_task, start_task, check_due_tasks

# 获取下一个可执行任务
task = get_next_task()
if task:
    start_task(task['id'])

# 检查到期任务
due_tasks = check_due_tasks(days=3)
for task in due_tasks:
    print(f"即将到期：{task['id']}")
```

### 场景 2：目标分解

```python
from task_manager import create_goal, decompose_goal

# 创建目标
create_goal(
    goal_id="GOAL-001",
    title="OpenClaw 系统优化",
    priority="high"
)

# 分解任务
decompose_goal(
    goal_id="GOAL-001",
    task_title="系统性能分析",
    priority="critical"
)
```

### 场景 3：团队协作

```python
from task_manager import filter_tasks, search_tasks

# 查看团队成员的任务
tasks = filter_tasks(owner="techlead", status="进行中")

# 搜索相关任务
tasks = search_tasks("性能优化")
```

---

## 🧪 测试

### 运行所有测试

```bash
cd scripts
python3 test_config.py          # 配置加载测试
python3 test_access_control.py  # 访问控制测试
python3 test_full_access.py     # 完整功能测试
python3 test_python_apis.py     # Python API 测试
```

### 测试结果

```
✅ 配置加载测试：1/1 通过
✅ 访问控制测试：7/7 通过
✅ CLI 命令测试：11/11 通过
✅ Python API 测试：8/8 通过
总计：27/27 通过（100%）
```

---

## 📊 API 参考

### 任务管理 API（13 个）

| API | 说明 | 示例 |
|-----|------|------|
| `create_task()` | 创建任务 | `create_task("TASK-001", "名称", "开发")` |
| `start_task()` | 开始任务 | `start_task("TASK-001", agent_id="techlead")` |
| `update_progress()` | 更新进度 | `update_progress("TASK-001", 50)` |
| `complete_task()` | 完成任务 | `complete_task("TASK-001")` |
| `edit_task()` | 编辑任务 | `edit_task("TASK-001", {"优先级": "P0"})` |
| `delete_task()` | 删除任务 | `delete_task("TASK-001")` |
| `search_tasks()` | 搜索任务 | `search_tasks("关键词")` |
| `filter_tasks()` | 过滤任务 | `filter_tasks(status="进行中")` |
| `check_due_tasks()` | 到期检查 | `check_due_tasks(days=7)` |
| `check_overdue_tasks()` | 超期检查 | `check_overdue_tasks()` |
| `get_statistics()` | 统计数据 | `get_statistics()` |
| `get_all_tasks()` | 获取所有任务 | `get_all_tasks()` |
| `get_task_by_id()` | 查询任务 | `get_task_by_id("TASK-001")` |

### 目标管理 API（5 个）

| API | 说明 | 示例 |
|-----|------|------|
| `create_goal()` | 创建目标 | `create_goal("GOAL-001", "目标名称")` |
| `decompose_goal()` | 分解目标 | `decompose_goal("GOAL-001", "任务名称")` |
| `list_goals()` | 列出目标 | `list_goals()` |
| `get_next_task()` | 下一个任务 | `get_next_task()` |
| `delete_goal()` | 删除目标 | `delete_goal("GOAL-001")` |

**完整 API 文档**: [API 参考](docs/api-reference.md)

---

## 🏗️ 系统架构

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Agent     │────▶│  Task Mgr    │────▶│  企业微信智能表格  │
│ (调用方)    │     │ (task_manager)│     │  (数据存储)      │
└─────────────┘     └──────────────┘     └─────────────────┘
       │                    │                      │
       │                    ▼                      │
       │           ┌──────────────┐               │
       └───────────│  config.json │◀──────────────┘
                   │  (配置驱动)   │
                   └──────────────┘
```

**核心组件**：
- `task_manager.py` - 核心逻辑（13 个任务 API + 5 个目标 API）
- `table_initializer.py` - 表格自动初始化
- `config.json` - 配置驱动（无需修改代码）
- `test_*.py` - 完整测试覆盖

---

## 🏗️ 项目结构

```
wecom-task-manager/
├── README.md                 # 本文件（你正在看的）
├── QUICKSTART.md             # 5 分钟快速开始
├── USAGE.md                  # 详细使用指南
├── config.json               # 配置文件（需自行创建）
├── config.template.json      # 配置模板
├── _meta.json                # 技能元数据
├── package.json              # NPM 包信息
├── scripts/
│   ├── task_manager.py       # 核心模块（273 行）
│   ├── table_initializer.py  # 表格初始化（156 行）
│   ├── test_*.py             # 测试脚本（7 个）
│   └── cli.py                # CLI 工具（23 个命令）
├── docs/
│   ├── config-guide.md       # 配置指南
│   ├── api-reference.md      # API 参考
│   ├── examples.md           # 使用示例
│   └── CHANGELOG.md          # 更新日志
└── references/
    └── api.md                # API 设计文档
```

---

## ❓ 常见问题 (FAQ)

### Q1: 提示 "找不到 mcporter 工具"
**解决**：
```bash
# 检查 mcporter 是否安装
openclaw plugins list | grep mcporter

# 如果没有，安装它
openclaw plugins install @openclaw/mcporter
```

### Q2: 企业微信 API 调用失败
**检查**：
1. docId/sheetId 是否正确
2. 企业微信机器人是否有表格访问权限
3. 网络连接是否正常

```bash
# 测试连接
cd ~/.openclaw/skills/wecom-task-manager/scripts
AGENT_ID="da-yan" python3 task_manager.py stats
```

### Q3: 表格字段缺失
**解决**：
```bash
cd ~/.openclaw/skills/wecom-task-manager/scripts
python3 table_initializer.py init
```

### Q4: 任务无法创建/更新
**检查**：
1. `config.json` 是否存在且格式正确
2. 访问控制是否允许当前 agent
3. 表格是否有写入权限

**调试**：
```bash
# 查看配置是否正确加载
cd ~/.openclaw/skills/wecom-task-manager/scripts
python3 -c "from config import load_config; print(load_config())"
```

### Q5: 提示 "任务已存在"
**原因**：任务 ID 已存在于表格中

**解决**：
- 使用不同的任务 ID
- 或者先删除旧任务：`python3 task_manager.py delete TASK-XXX`

---

## 🔒 安全最佳实践

### 配置文件保护
```bash
# 确保 config.json 不被提交
chmod 600 ~/.openclaw/skills/wecom-task-manager/config.json
git update-index --assume-unchanged config.json
```

### 访问控制
- ✅ 默认启用白名单机制
- ✅ 仅允许配置的 agents 访问
- ✅ 敏感操作记录日志

### 数据备份
建议定期备份企业微信表格数据：
```bash
# 导出所有任务数据
cd ~/.openclaw/skills/wecom-task-manager/scripts
python3 task_manager.py export > backup_$(date +%Y%m%d).json
```

---

## 📊 性能基准

| 操作 | 平均耗时 | 95 百分位 |
|------|---------|----------|
| 创建任务 | ~200ms | ~350ms |
| 更新进度 | ~150ms | ~280ms |
| 查询任务 | ~100ms | ~200ms |
| 统计分析 | ~300ms | ~500ms |

**测试环境**：
- OpenClaw v2026.3.24
- 企业微信智能表格（1000+ 任务）
- 本地网络

**并发限制**：默认 3 个并发任务（可配置）

---

## 📝 更新日志

- **v1.5.0** (2026-03-28) - 多系统支持、环境变量配置、表格自动初始化优化
- **v1.4.0** (2026-03-27) - 表格自动初始化功能
- **v1.3.0** (2026-03-26) - 关联目标字段支持

[查看完整更新日志](docs/CHANGELOG.md)

---

## 🤝 贡献指南

### 如何贡献

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交变更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### 贡献内容

我们欢迎以下类型的贡献：
- 🐛 Bug 修复
- ✨ 新功能
- 📝 文档改进
- 🎨 代码优化
- 🧪 测试用例
- 🌍 国际化

### 开发环境

```bash
# 克隆项目
git clone https://github.com/jhZheng222/openclaw-wecom-task-manager.git

# 安装依赖
cd openclaw-wecom-task-manager
pip install -r requirements.txt

# 运行测试
cd scripts
python3 test_*.py
```

---

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)

---

## 🙏 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) - OpenClaw 框架
- [企业微信](https://work.weixin.qq.com/) - 企业微信智能表格
- [mcporter](https://github.com/openclaw/mcporter) - MCP 工具

---

## 📞 联系方式

- **项目地址**: https://github.com/jhZheng222/openclaw-wecom-task-manager
- **问题反馈**: https://github.com/jhZheng222/openclaw-wecom-task-manager/issues
- **Discord**: jh.zheng_00604

---

## 🎯 路线图

### v1.5.0（当前版本）✅ 已发布
- ✅ 多系统支持 - 可在任意 OpenClaw 系统使用
- ✅ 配置驱动 - 无需修改代码
- ✅ 环境变量支持 - OPENCLAW_WORKSPACE、MCPORTER_PATH
- ✅ 动态路径查找 - 自动查找 mcporter
- ✅ 预计工时字段修复
- ✅ 文档完善 - FAQ、架构图、安全说明

### v1.4.0 ✅ 已发布
- ✅ 表格自动初始化功能
- ✅ 字段自动检查和补齐
- ✅ CLI 初始化工具
- ✅ 开箱即用体验

### v1.3.0 ✅ 已发布
- ✅ 关联目标字段支持
- ✅ 验收信息字段合并
- ✅ 进度 5 档制
- ✅ 实际工时自动计算

### v2.0.0（规划中）🔮
- [ ] 工作流引擎
- [ ] 自动化规则
- [ ] 图表统计
- [ ] REST API
- [ ] 批量导入/导出
- [ ] Web 管理界面

---

**⭐ 如果这个项目对你有帮助，请给一个 Star！**

**我们同在，我们一往无前。** ✨
