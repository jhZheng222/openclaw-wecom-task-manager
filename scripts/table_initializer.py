#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业微信表格自动初始化模块
首次使用时自动创建完整的表格结构
"""

import json
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Optional

# ==================== 配置 ====================

# 切换到 workspace 目录（确保 mcporter 能找到 MCP 配置）
WORKSPACE = Path.home() / ".openclaw" / "workspace"
import os
os.chdir(WORKSPACE)

MCPORTER_PATH = "/usr/local/Cellar/node/25.6.0/bin/mcporter"

# 从配置文件加载
CONFIG_PATH = Path(__file__).parent.parent / "config.json"
if CONFIG_PATH.exists():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
    DOCID = config.get("enterpriseWeChat", {}).get("docId")
    SHEET_ID = config.get("enterpriseWeChat", {}).get("sheetId")
else:
    DOCID = "dcTCczAuKRidTOQ9ZlUOpXgW9JSuq7slNrR6Z6O-N80yqOaGNTJpcTyqYXgOF7aXURG1adBiAxIYCi5KQg7KAXvA"
    SHEET_ID = "q979lj"

# ==================== 字段定义 ====================

# 必需字段（21 个，可通过 API 添加）
REQUIRED_FIELDS = [
    # 基础字段（9 个）
    {"field_name": "任务 ID", "field_type": "FIELD_TYPE_TEXT"},
    {"field_name": "任务名称", "field_type": "FIELD_TYPE_TEXT"},
    {"field_name": "任务描述", "field_type": "FIELD_TYPE_TEXT"},
    {"field_name": "任务类型", "field_type": "FIELD_TYPE_SINGLE_SELECT", 
     "options": ["开发", "运维", "投资", "学习", "文档", "市场", "客服"]},
    {"field_name": "优先级", "field_type": "FIELD_TYPE_SINGLE_SELECT",
     "options": ["P0", "P1", "P2", "P3"]},
    {"field_name": "负责人", "field_type": "FIELD_TYPE_TEXT"},
    {"field_name": "状态", "field_type": "FIELD_TYPE_SINGLE_SELECT",
     "options": ["待办", "进行中", "已完成", "已取消"]},
    {"field_name": "截止时间", "field_type": "FIELD_TYPE_DATE_TIME"},
    {"field_name": "进度", "field_type": "FIELD_TYPE_PROGRESS"},
    
    # 时间字段（3 个）
    {"field_name": "创建时间", "field_type": "FIELD_TYPE_DATE_TIME"},
    {"field_name": "实际开始时间", "field_type": "FIELD_TYPE_DATE_TIME"},
    {"field_name": "实际完成时间", "field_type": "FIELD_TYPE_DATE_TIME"},
    
    # 工时字段（1 个）
    {"field_name": "预计工时", "field_type": "FIELD_TYPE_NUMBER"},
    
    # 扩展字段（8 个）
    {"field_name": "前置依赖", "field_type": "FIELD_TYPE_TEXT"},
    {"field_name": "阻塞原因", "field_type": "FIELD_TYPE_TEXT"},
    {"field_name": "风险等级", "field_type": "FIELD_TYPE_SINGLE_SELECT",
     "options": ["高", "中", "低"]},
    {"field_name": "输出物", "field_type": "FIELD_TYPE_URL"},
    {"field_name": "备注", "field_type": "FIELD_TYPE_TEXT"},
    {"field_name": "协作成员", "field_type": "FIELD_TYPE_USER"},
    {"field_name": "关联目标", "field_type": "FIELD_TYPE_TEXT"},
    {"field_name": "验收信息", "field_type": "FIELD_TYPE_TEXT"},
]

# 可选字段（自动计算字段，需要手动配置）
OPTIONAL_FIELDS = [
    {"field_name": "最后更新时间", "field_type": "DATE_TIME", "note": "自动计算字段"},
    {"field_name": "实际工时", "field_type": "NUMBER", "note": "自动计算字段"},
]

# ==================== API 封装 ====================

def run_mcporter(command: str, args: dict) -> dict:
    """执行 mcporter 命令"""
    args_json = json.dumps(args, ensure_ascii=False)
    cmd = f'{MCPORTER_PATH} call wecom-doc.{command} --args \'{args_json}\''
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
    
    if result.returncode != 0:
        return {"errcode": -1, "errmsg": result.stderr}
    
    try:
        return json.loads(result.stdout)
    except:
        return {"errcode": -1, "errmsg": result.stdout}


def get_current_fields() -> List[dict]:
    """获取当前表格的所有字段"""
    result = run_mcporter("smartsheet_get_fields", {
        "sheet_id": SHEET_ID,
        "docid": DOCID
    })
    
    if result.get("errcode") != 0:
        return []
    
    return result.get("fields", [])


def add_field(field_def: dict) -> bool:
    """添加单个字段"""
    result = run_mcporter("smartsheet_add_fields", {
        "sheet_id": SHEET_ID,
        "docid": DOCID,
        "fields": [field_def]
    })
    
    return result.get("errcode") == 0


def update_field(field_id: str, field_title: str) -> bool:
    """更新字段名称"""
    result = run_mcporter("smartsheet_update_fields", {
        "sheet_id": SHEET_ID,
        "docid": DOCID,
        "fields": [{
            "field_id": field_id,
            "field_title": field_title,
            "field_type": "FIELD_TYPE_TEXT"
        }]
    })
    
    return result.get("errcode") == 0


# ==================== 初始化功能 ====================

def check_table_status() -> dict:
    """
    检查表格状态
    
    Returns:
        dict: {
            "exists": bool,  # 表格是否存在
            "field_count": int,  # 字段数量
            "missing_fields": list,  # 缺失的必需字段
            "optional_missing": list,  # 缺失的可选字段
            "is_complete": bool  # 是否完整（必需字段齐全）
        }
    """
    fields = get_current_fields()
    field_names = [f["field_title"] for f in fields]
    
    required_names = [f["field_name"] for f in REQUIRED_FIELDS]
    optional_names = [f["field_name"] for f in OPTIONAL_FIELDS]
    
    missing_fields = [name for name in required_names if name not in field_names]
    optional_missing = [name for name in optional_names if name not in field_names]
    
    return {
        "exists": True,
        "field_count": len(fields),
        "missing_fields": missing_fields,
        "optional_missing": optional_missing,
        "is_complete": len(missing_fields) == 0
    }


def initialize_table(retry: int = 3) -> dict:
    """
    初始化表格（自动创建缺失的字段）
    
    Args:
        retry: 重试次数
    
    Returns:
        dict: {
            "success": bool,
            "added_fields": list,
            "failed_fields": list,
            "message": str
        }
    """
    print("=" * 60)
    print("🚀 企业微信表格初始化")
    print("=" * 60)
    
    # 检查当前状态
    print("\n📋 检查表格状态...")
    status = check_table_status()
    print(f"   当前字段数：{status['field_count']}")
    print(f"   需要字段数：{len(REQUIRED_FIELDS)}")
    print(f"   缺失字段：{len(status['missing_fields'])}")
    
    if status['is_complete']:
        print("\n✅ 表格已完整，无需初始化")
        return {
            "success": True,
            "added_fields": [],
            "failed_fields": [],
            "message": "表格已完整"
        }
    
    # 添加缺失字段
    print("\n📝 开始添加缺失字段...")
    added_fields = []
    failed_fields = []
    
    current_fields = get_current_fields()
    current_names = [f["field_title"] for f in current_fields]
    
    for field_def in REQUIRED_FIELDS:
        field_name = field_def["field_name"]
        
        # 跳过已存在的字段
        if field_name in current_names:
            continue
        
        # 尝试添加
        print(f"\n   ➕ 添加字段：{field_name}")
        success = False
        
        for attempt in range(retry):
            if add_field(field_def):
                print(f"      ✅ 添加成功")
                added_fields.append(field_name)
                success = True
                break
            else:
                print(f"      ⚠️ 尝试 {attempt+1}/{retry} 失败")
                time.sleep(2)
        
        if not success:
            print(f"      ❌ 添加失败")
            failed_fields.append(field_name)
        
        # 避免限流
        time.sleep(1)
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 初始化结果")
    print("=" * 60)
    print(f"   新增字段：{len(added_fields)} 个")
    print(f"   失败字段：{len(failed_fields)} 个")
    
    if added_fields:
        print(f"\n   ✅ 成功：{', '.join(added_fields)}")
    
    if failed_fields:
        print(f"\n   ❌ 失败：{', '.join(failed_fields)}")
    
    success = len(failed_fields) == 0
    
    if success:
        print("\n🎉 表格初始化完成！")
    else:
        print("\n⚠️ 部分字段添加失败，请手动添加")
    
    return {
        "success": success,
        "added_fields": added_fields,
        "failed_fields": failed_fields,
        "message": f"添加 {len(added_fields)} 个字段，失败 {len(failed_fields)} 个"
    }


def ensure_table_initialized() -> bool:
    """
    确保表格已初始化（在创建任务前调用）
    
    Returns:
        bool: 表格是否可用
    """
    status = check_table_status()
    
    if status['is_complete']:
        return True
    
    # 自动初始化
    print("\n⚠️ 表格字段不完整，自动初始化...")
    result = initialize_table()
    
    return result['success']


# ==================== CLI 命令 ====================

def cmd_init_table():
    """CLI 命令：初始化表格"""
    result = initialize_table()
    
    if result['success']:
        print("\n✅ 初始化成功！")
        return 0
    else:
        print("\n❌ 初始化失败或部分失败")
        return 1


def cmd_check_table():
    """CLI 命令：检查表格状态"""
    status = check_table_status()
    
    print("=" * 60)
    print("📊 表格状态检查")
    print("=" * 60)
    print(f"   必需字段：{status['field_count']}/{len(REQUIRED_FIELDS)}")
    print(f"   可选字段：{len(OPTIONAL_FIELDS) - len(status.get('optional_missing', OPTIONAL_FIELDS))}/{len(OPTIONAL_FIELDS)}")
    
    if status['missing_fields']:
        print(f"\n   ❌ 缺失必需字段 ({len(status['missing_fields'])}个):")
        for field in status['missing_fields']:
            print(f"      - {field}")
    
    if status.get('optional_missing'):
        print(f"\n   ⚠️ 缺失可选字段 ({len(status['optional_missing'])}个):")
        for field in status['optional_missing']:
            print(f"      - {field} (自动计算字段)")
    
    if status['is_complete']:
        print("\n✅ 表格配置完整（必需字段齐全）")
        if status.get('optional_missing'):
            print(f"💡 提示：可以手动添加 {len(status['optional_missing'])} 个自动计算字段")
    else:
        print("\n⚠️ 表格配置不完整")
        print("   运行以下命令修复：")
        print("   python3 table_initializer.py init")
    
    return 0 if status['is_complete'] else 1


# ==================== 主程序 ====================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "init":
            sys.exit(cmd_init_table())
        elif command == "check":
            sys.exit(cmd_check_table())
        else:
            print(f"未知命令：{command}")
            print("可用命令：init, check")
            sys.exit(1)
    else:
        # 默认：检查并自动初始化
        ensure_table_initialized()
