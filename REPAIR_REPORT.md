# wecom-task-manager 技能修复报告

## 修复日期
2026-03-29

## 问题描述
wecom-task-manager 技能无法正确获取企业微信智能表格中的全部任务数据。

### 根本原因
1. **错误的命令调用**：代码中 `run_wecom_mcp()` 函数试图调用 `wecom_mcp call doc` 命令，但这个命令不存在于 PATH 中
2. **MCP 调用方式错误**：wecom_mcp 实际上是通过 OpenClaw MCP 系统调用的，不是独立 CLI
3. **输出截断问题**：subprocess 的 `capture_output` 有约 64KB 缓冲区限制，而完整数据约 120KB

## 修复方案

### 1. 修改 `run_wecom_mcp()` 函数
**文件位置**: `~/.openclaw/skills/wecom-task-manager/scripts/task_manager.py`

**修改内容**:
- 将 `wecom_mcp call doc` 命令改为使用 `mcporter call wecom-doc.<command>`
- 使用临时文件方式避免 subprocess 输出缓冲区限制
- 正确处理 URL 参数中的特殊字符

**关键代码变更**:
```python
def run_wecom_mcp(command: str, args_dict: dict) -> Optional[dict]:
    """
    使用 mcporter 调用 wecom-doc MCP 服务（绕过 mcporter 分页限制）
    """
    import tempfile
    
    # 构建 mcporter 调用命令
    args_parts = []
    for key, value in args_dict.items():
        # URL 需要特殊处理（包含特殊字符）
        if key == "url" and isinstance(value, str):
            args_parts.append(f'{key}="{value}"')
        else:
            args_parts.append(f"{key}={value}")
    
    args_str = " ".join(args_parts)
    
    # 使用临时文件避免 subprocess 输出缓冲区限制
    # capture_output 有约 64KB 限制，而完整数据约 120KB
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmpfile:
        tmpfile_path = tmpfile.name
    
    try:
        cmd = f'{MCPORTER_PATH} call wecom-doc.{command} {args_str} --output json > "{tmpfile_path}" 2>&1'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            # 读取错误输出
            try:
                with open(tmpfile_path, 'r', encoding='utf-8') as f:
                    error_output = f.read()
                print(f"Error running mcporter (wecom-doc): {error_output[:500]}")
            except:
                print(f"Error running mcporter (wecom-doc): {result.stderr}")
            return None
        
        # 从文件读取完整 JSON
        with open(tmpfile_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return json.loads(content)
    
    except Exception as e:
        print(f"Failed to parse wecom-doc response: {e}")
        return None
    
    finally:
        # 清理临时文件
        try:
            os.unlink(tmpfile_path)
        except:
            pass
```

### 2. 修改工作目录切换逻辑
**修改内容**:
- 优先切换到 `general_coordinator` workspace（包含 mcporter 配置文件）
- 确保 mcporter 能找到 wecom-doc 服务器配置

```python
# 切换到 workspace 目录（确保 mcporter 能找到 MCP 配置）
GENERAL_COORDINATOR_WS = str(Path.home() / ".openclaw" / "workspace-general_coordinator")

# 优先使用 general_coordinator workspace（包含 mcporter 配置）
if Path(GENERAL_COORDINATOR_WS).exists():
    os.chdir(GENERAL_COORDINATOR_WS)
elif Path(WORKSPACE).exists():
    os.chdir(WORKSPACE)
else:
    print(f"⚠️ 工作区不存在：{WORKSPACE}，使用当前目录")
```

## 测试验证

### 测试命令 1: 列出所有任务
```bash
cd /Users/zhengxiaoyu/.openclaw/skills/wecom-task-manager
python3 scripts/task_manager.py list
```

**结果**: ✅ 成功返回 57 个任务（之前只能获取 30 个）

### 测试命令 2: 生成状态报告
```bash
python3 scripts/task_manager.py report
```

**结果**: ✅ 正确统计所有状态的任务
- 总任务数：57
- 已完成：20
- 进行中：1
- 待办：26
- 已取消：8
- 已暂停：2

### 测试命令 3: 统计数据
```bash
python3 scripts/task_manager.py stats
```

**结果**: ✅ 正确统计各维度数据
- 按优先级：P0(3), P1(46), P2(6)
- 按负责人：da-yan(27), techlead(13), general_coordinator(9) 等
- 按类型：运维 (30), 开发 (12), 文档 (10) 等

### 测试命令 4: 过滤功能
```bash
python3 scripts/task_manager.py filter status=待办
python3 scripts/task_manager.py filter status=已完成
python3 scripts/task_manager.py filter status=进行中
python3 scripts/task_manager.py filter status=已暂停
```

**结果**: ✅ 所有过滤功能正常工作
- 待办：26 个
- 已完成：20 个
- 进行中：1 个
- 已暂停：2 个

## 修复效果

| 指标 | 修复前 | 修复后 |
|------|--------|--------|
| 获取任务数 | 30 个（分页限制） | 57 个（全部） |
| JSON 解析 | 失败（截断） | 成功 |
| 所有状态查询 | ❌ 部分缺失 | ✅ 完整 |
| 过滤功能 | ⚠️ 不完整 | ✅ 正常 |

## 技术要点

1. **MCP 调用方式**：使用 `mcporter call wecom-doc.<command>` 而非 `wecom_mcp call doc`
2. **输出缓冲区问题**：使用临时文件绕过 subprocess 的 64KB 限制
3. **配置路径**：确保切换到包含 mcporter 配置的 workspace 目录
4. **URL 参数处理**：特殊字符需要用引号包裹

## 后续建议

1. 考虑将临时文件方式封装为通用工具函数
2. 为 mcporter 配置添加环境变量支持，避免硬编码路径
3. 添加更完善的错误处理和日志记录

## 修复人员
墨攻（技术领航）

## 审核状态
✅ 已完成测试验证
