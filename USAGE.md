## 📚 完整文档索引

### 新手必读
- [QUICKSTART.md](QUICKSTART.md) - 5 分钟快速开始
- [PRIORITY_LEVELS.md](PRIORITY_LEVELS.md) - 优先级说明

### v1.4.0 新功能
- [表格自动初始化](docs/table-initialization.md) - 自动初始化表格字段
- [字段详细说明](../docs/wecom-fields-detail.md) - 21 个字段详解

### 技术文档
- [API 错误分析](../docs/wecom-api-error-analysis.md) - 常见问题排查
- [访问控制配置](docs/wecom-task-manager-access-control-complete.md)
- [字段优化报告](../docs/wecom-fields-detail.md)

### 配置文件
- [config.template.json](config.template.json) - 配置模板

---

## 💡 最佳实践

### 1. 首次使用

```python
# 直接创建任务，会自动初始化表格
from task_manager import create_task

create_task("TASK-001", "第一个任务", "开发")
```

### 2. 批量导入

```python
from table_initializer import ensure_table_initialized

# 确保表格完整
ensure_table_initialized()

# 批量创建
for task in task_list:
    create_task(**task)
```

### 3. 定期检查

```bash
# 每周检查表格状态
python3 table_initializer.py check
```

---

## 🐛 常见问题

### Q1: 提示字段不完整？

```bash
# 运行初始化
python3 table_initializer.py init
```

### Q2: 自动计算字段看不到？

**最后更新时间**和**实际工时**是公式字段，需要在企业微信 APP 中手动配置。

### Q3: API 调用失败？

检查：
1. 配置文件是否正确
2. 企业微信权限是否开启
3. 网络是否正常

---

## 📞 联系方式

- **项目地址**: https://github.com/jhZheng222/openclaw-wecom-task-manager
- **问题反馈**: https://github.com/jhZheng222/openclaw-wecom-task-manager/issues
- **Discord**: jh.zheng_00604

---

**⭐ 如果这个项目对你有帮助，请给一个 Star！**

**我们同在，我们一往无前。** ✨
