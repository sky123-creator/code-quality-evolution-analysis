from typing import Dict, List, Any
from .file_walker import get_python_files, get_project_versions

# 导入同学A的指标计算函数
from analyzers.loc import get_line_count
from analyzers.comment import get_comment_rate
from analyzers.complexity import get_average_cyclomatic_complexity
from analyzers.inheritance import get_average_inheritance_depth

def process_single_version(version_dir: str) -> Dict[str, Any]:
    """处理单个版本，调用A的工具计算指标"""
    py_files = get_python_files(version_dir)
    if not py_files:
        return {"loc": 0, "comment_rate": 0.0, "avg_complexity": 0.0, "avg_inheritance_depth": 0.0}
    
    try:
        loc = get_line_count(py_files)
        comment_rate = round(get_comment_rate(py_files), 4)
        avg_complexity = round(get_average_cyclomatic_complexity(py_files), 4)
        avg_inheritance_depth = round(get_average_inheritance_depth(py_files), 4)
    except Exception as e:
        print(f"处理版本 {version_dir} 出错：{str(e)}")
        return {"loc": 0, "comment_rate": 0.0, "avg_complexity": 0.0, "avg_inheritance_depth": 0.0}
    
    return {
        "loc": loc,
        "comment_rate": comment_rate,
        "avg_complexity": avg_complexity,
        "avg_inheritance_depth": avg_inheritance_depth
    }

def process_all_projects(project_root: str) -> List[Dict[str, Any]]:
    """批量处理3个项目的15个版本"""
    projects = get_project_versions(project_root)
    all_results = []
    
    for project_name, versions in projects.items():
        print(f"处理项目：{project_name}")
        for version_name, version_dir in versions.items():
            print(f"  版本：{version_name}")
            metrics = process_single_version(version_dir)
            row = {
                "project_name": project_name,
                "version": version_name,
                "file_count": len(get_python_files(version_dir)),
                **metrics
            }
            all_results.append(row)
    
    return all_results