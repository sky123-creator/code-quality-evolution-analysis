import sys
import os
# 添加项目根目录到Python模块搜索路径，解决analyzers导入问题
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import Dict, List, Any
# 导入本地模块
from file_walker import get_python_files, get_project_versions
from csv_exporter import export_to_csv  # 导入CSV导出工具
# 导入各分析器指标计算函数
from analyzers.loc import calculate_loc                  # LOC + 注释率
from analyzers.complexity import calculate_complexity    # 圈复杂度
from analyzers.dependency import analyze_dependencies    # 依赖分析

# ===================== 全局配置（无需修改，已适配你的项目）=====================
PROJECT_ROOT = "pipeline/target"  # 待分析项目根目录（指向Flask的project目录）
OUTPUT_DIR = "pipeline/output"    # 分析结果输出目录
OUTPUT_CSV = "flask_quality_metrics.csv"  # 输出的CSV文件名
# ==============================================================================

def process_single_version(version_dir: str) -> Dict[str, Any]:
    """处理单个版本：整合所有指标，生成版本级汇总数据"""
    py_files = get_python_files(version_dir)
    if not py_files:
        print(f"  警告：该版本无有效Python文件 → {version_dir}")
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

            # 2. 调用所有分析器函数，获取字典结果
            loc_dict = calculate_loc(file_content)
            complexity_dict = calculate_complexity(file_content)
            dep_dict = analyze_dependencies(file_content)

            # 3. 从字典提取数值（兼容键名缺失的情况，默认0）
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
            print(f"  跳过异常文件：{os.path.basename(file_path)} → 错误：{str(e)[:50]}")
            continue

    # 5. 计算版本级平均值（避免除以 0，防止运行报错）
    avg_comment = round(total_comment_rate / valid_file_count, 4) if valid_file_count > 0 else 0.0
    avg_complex = round(total_complexity / valid_file_count, 4) if valid_file_count > 0 else 0.0
    avg_import = round(total_import_count / valid_file_count, 4) if valid_file_count > 0 else 0.0

    # 6. 返回版本级最终指标（与 CSV 列名对应）
    return {
        "loc": total_code_lines,          # 版本总代码行数
        "comment_rate": avg_comment,     # 版本平均注释率（%）
        "avg_complexity": avg_complex,   # 版本平均圈复杂度
        "total_imports": total_imports,  # 版本总导入模块数
        "avg_import_count": avg_import   # 版本文件平均import语句数
    }

def process_all_projects(project_root: str) -> List[Dict[str, Any]]:
    """批量处理所有项目+版本，生成最终数据列表（修复了原代码的拼写错误）"""
    # 获取项目和版本字典（适配你的flask项目+5个版本）
    projects = get_project_versions(project_root)
    all_results = []

    if not projects:
        print("错误：未在指定目录找到任何项目 →", project_root)
        return all_results

    # 遍历所有项目和版本
    for project_name, versions in projects.items():
        print(f"\n===================== 开始处理项目：{project_name} =====================")
        if not versions:
            print(f"  警告：项目{project_name}无有效版本目录")
            continue
        # 遍历当前项目的所有版本
        for version_name, version_dir in versions.items():
            print(f"  ├─ 正在分析版本：{version_name}")
            # 计算当前版本的所有质量指标
            metrics = process_single_version(version_dir)
            # 拼接行数据：项目名+版本名+文件数+所有指标
            row = {
                "project_name": project_name,
                "version": version_name,
                "file_count": len(get_python_files(version_dir)),  # 该版本的有效Python文件数
                **metrics  # 解包指标字典（loc/comment_rate等）
            }
            all_results.append(row)
            # 打印当前版本的核心指标（直观展示进度）
            print(f"  └─ 版本{version_name}分析完成 → 文件数：{row['file_count']} | 总代码行数：{row['loc']}")

    print(f"\n===================== 所有项目分析完成 =====================")
    return all_results

def main():
    """程序主入口：执行全流程（分析+导出）"""
    print("===== 启动代码质量分析流水线 =====")
    print(f"分析根目录：{os.path.abspath(PROJECT_ROOT)}")
    print(f"结果输出目录：{os.path.abspath(OUTPUT_DIR)}")

    # 1. 自动创建输出目录（如果不存在）
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"已自动创建输出目录 → {OUTPUT_DIR}")

    # 2. 执行全量分析（核心步骤）
    analysis_results = process_all_projects(PROJECT_ROOT)

    if not analysis_results:
        print("===== 流水线执行结束：无分析结果可导出 =====")
        return

    # 3. 导出分析结果到CSV文件
    output_csv_path = os.path.join(OUTPUT_DIR, OUTPUT_CSV)
    export_to_csv(analysis_results, output_csv_path)
    print(f"\n===== 流水线执行成功！=====")
    print(f"分析结果已导出为CSV → {os.path.abspath(output_csv_path)}")
    print(f"共分析 {len(analysis_results)} 个版本的代码质量")

# 仅在直接运行该脚本时执行主函数（Python规范写法）
if __name__ == "__main__":
    main()