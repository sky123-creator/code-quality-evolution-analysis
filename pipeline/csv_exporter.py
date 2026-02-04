import csv
import os
from typing import List, Dict

def export_to_csv(data: List[Dict], output_path: str) -> None:
    """将结果导出为CSV文件"""
    if not data:
        print("无数据可导出")
        return
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fixed_fieldnames = [
        "project_name", "version", "file_count",
        "loc", "comment_rate", "avg_complexity", "total_imports", "avg_import_count"
    ]
    
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fixed_fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"数据已导出到：{output_path}")