from typing import Dict, List, Any
from .file_walker import get_python_files, get_project_versions
import os


from analyzers.loc import calculate_loc                  # LOC + 注释率
from analyzers.complexity import calculate_complexity    # 圈复杂度
from analyzers.dependency import analyze_dependencies    # 依赖分析（注意函数名！）

def process_single_version(version_dir: str) -> Dict[str, Any]:
    """处理单个版本：整合所有指标，生成版本级汇总数据"""
    py_files = get_python_files(version_dir)
    if not py_files:
        return {
            "loc": 0,
            "comment_rate": 0.0,
            "avg_complexity": 0.0,
            "total_imports": 0,
            "avg_import_count": 0.0
        }

    # 初始化汇总变量（与返回指标对应）
    total_code_lines = 0
    total_comment_rate = 0.0
    total_complexity = 0.0
    total_imports = 0          
    total_import_count = 0     
    valid_file_count = 0

    for file_path in py_files:
        try:
            # 1. 读取文件内容
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                file_content = f.read()

            # 2. 调用所有函数，获取字典结果
            loc_dict = calculate_loc(file_content)
            complexity_dict = calculate_complexity(file_content)
            dep_dict = analyze_dependencies(file_content)

            # 3. 从字典提取数值
            code_lines = loc_dict.get('code_lines', 0)
            comment_rate = loc_dict.get('comment_rate', 0.0)
            
            complexity = complexity_dict.get('cyclomatic_complexity', 0.0)
           
            imports = dep_dict.get('total_imports', 0)
            import_count = dep_dict.get('import_count', 0)

            # 4. 累加汇总（文件 → 版本）
            total_code_lines += code_lines
            total_comment_rate += comment_rate
            total_complexity += complexity
            total_imports += imports
            total_import_count += import_count
            valid_file_count += 1

        except Exception as e:
            print(f"处理文件 {file_path} 失败: {str(e)}")
            continue

    # 5. 计算版本级平均值（避免除以 0）
    avg_comment = round(total_comment_rate / valid_file_count, 4) if valid_file_count > 0 else 0.0
    avg_complex = round(total_complexity / valid_file_count, 4) if valid_file_count > 0 else 0.0
    avg_import = round(total_import_count / valid_file_count, 4) if valid_file_count > 0 else 0.0

    # 6. 返回版本级最终指标（与 CSV 列名对应）
    return {
        "loc": total_code_lines,          # 版本总代码行数
        "comment_rate": avg_comment,     # 版本平均注释率
        "avg_complexity": avg_complex,   # 版本平均圈复杂度
        "total_imports": total_imports,  # 版本总导入数（A同学指标）
        "avg_import_count": avg_import   # 版本文件平均 import 语句数
    }

def process_all_projects(project_root: str) -> List[Dict[str, Any]]:
    """批量处理 3 项目 × 5 版本，生成最终数据列表"""
    projects = get_project_versions(project_root)
    all_results = []

    for project_name, versions in projects.items():
        print(f"开始处理项目：{project_name}")
        for version_name, version_dir in versions.items():
            print(f"  - 处理版本：{version_name}")
            metrics = process_single_version(version_dir)
            # 拼接项目名、版本名、文件数 + 指标数据
            row = {
                "project_name": project_name,
                "version": version_name,
                "file_count": len(get_python_files(version_dir)),
                **metrics
            }
            all_results.append(row)
    return all_results
