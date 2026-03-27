#!/usr/bin/env python3
"""
添加缺失的工时字段
"""

import json
import subprocess
import time

DOCID = "dcTCczAuKRidTOQ9ZlUOpXgW9JSuq7slNrR6Z6O-N80yqOaGNTJpcTyqYXgOF7aXURG1adBiAxIYCi5KQg7KAXvA"
SHEET_ID = "q979lj"
MCPORTER_PATH = "/usr/local/Cellar/node/25.6.0/bin/mcporter"

def run_mcporter(command: str, args: dict):
    args_json = json.dumps(args, ensure_ascii=False)
    cmd = f'{MCPORTER_PATH} call wecom-doc.{command} --args \'{args_json}\''
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        return {"errcode": -1, "errmsg": result.stderr}
    try:
        return json.loads(result.stdout)
    except:
        return {"errcode": -1, "errmsg": result.stdout}

def add_field(field_name: str, field_type: str, retry: int = 3):
    """添加单个字段"""
    print(f"\n➕ 添加字段：{field_name} ({field_type})")
    
    field_def = {
        "field_name": field_name,
        "field_type": field_type
    }
    
    for attempt in range(retry):
        result = run_mcporter("smartsheet_add_fields", {
            "sheet_id": SHEET_ID,
            "docid": DOCID,
            "fields": [field_def]
        })
        
        if result.get("errcode") == 0:
            print(f"   ✅ 添加成功")
            return True
        else:
            err = result.get('errmsg', 'Unknown error')
            print(f"   ⚠️ 尝试 {attempt+1}/{retry} 失败：{err}")
            if attempt < retry - 1:
                time.sleep(2)
    
    print(f"   ❌ 添加失败（重试{retry}次）")
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 添加工时字段")
    print("=" * 60)
    
    fields_to_add = [
        ("预计工时", "FIELD_TYPE_NUMBER"),
        ("实际工时", "FIELD_TYPE_NUMBER"),
    ]
    
    success_count = 0
    for field_name, field_type in fields_to_add:
        if add_field(field_name, field_type):
            success_count += 1
        time.sleep(1.5)
    
    print(f"\n{'='*60}")
    print(f"✅ 完成：{success_count}/{len(fields_to_add)} 个字段添加成功")
    print(f"{'='*60}")
