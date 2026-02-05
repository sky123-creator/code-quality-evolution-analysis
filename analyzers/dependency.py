def analyze_dependencies(code):
    """
    分析Python代码的依赖关系（简单版）
    
    参数:
        code: Python代码字符串
        
    返回:
        dict: 包含依赖信息的字典
    """
    if not code or code.strip() == "":
        return {
            'import_count': 0,
            'from_import_count': 0,
            'total_imports': 0,
            'modules': [],
            'standard_lib_count': 0,
            'external_lib_count': 0,
            'has_circular_risk': False
        }
    
    lines = code.split('\n')
    
    import_count = 0
    from_import_count = 0
    modules = []  # 所有导入的模块
    standard_libs = []  # 标准库
    external_libs = []  # 外部库
    
    # 常见Python标准库
    STANDARD_LIBS = [
        'os', 'sys', 'json', 'math', 'datetime', 're', 'collections',
        'itertools', 'functools', 'random', 'typing', 'pathlib', 'logging'
    ]
    
    for line in lines:
        line_stripped = line.strip()
        
        # 跳过空行和注释
        if not line_stripped or line_stripped.startswith('#'):
            continue
        
        # 处理 import 语句
        if line_stripped.startswith('import '):
            import_count += 1
            # 提取 import 后面的部分
            import_part = line_stripped[7:]  # 去掉"import "
            # 处理多个导入：import os, sys, json
            for module in import_part.split(','):
                module = module.strip().split('.')[0]  # 只取顶级模块
                if module and module not in modules:
                    modules.append(module)
                    
                    # 分类
                    if module in STANDARD_LIBS:
                        standard_libs.append(module)
                    else:
                        external_libs.append(module)
        
        # 处理 from ... import 语句
        elif line_stripped.startswith('from '):
            from_import_count += 1
            # 提取 from 后面的模块名
            # 格式: from module import something
            parts = line_stripped[5:].split(' import ')  # 去掉"from "
            if len(parts) >= 1:
                module = parts[0].strip().split('.')[0]  # 只取顶级模块
                if module and module not in modules:
                    modules.append(module)
                    
                    # 分类
                    if module in STANDARD_LIBS:
                        standard_libs.append(module)
                    else:
                        external_libs.append(module)
    
    total_imports = import_count + from_import_count
    
    # 简单检测循环依赖风险（如果导入自己）
    has_circular_risk = any('test' in module.lower() for module in modules)
    
    return {
        'import_count': import_count,
        'from_import_count': from_import_count,
        'total_imports': total_imports,
        'modules': modules,
        'module_count': len(modules),
        'standard_libs': standard_libs,
        'standard_lib_count': len(standard_libs),
        'external_libs': external_libs,
        'external_lib_count': len(external_libs),
        'has_circular_risk': has_circular_risk,
        'dependency_score': calculate_dependency_score(total_imports, len(external_libs))
    }


def calculate_dependency_score(total_imports, external_count):
    """
    计算依赖分数（0-100分）
    规则：外部依赖越少，分数越高
    """
    if total_imports == 0:
        return 100
    
    # 基础分
    score = 80
    
    # 外部依赖扣分
    score -= min(30, external_count * 5)
    
    # 总依赖数扣分
    score -= min(20, total_imports * 2)
    
    return max(0, min(100, score))

def detect_circular_imports(code, module_name="module"):
    """
    检测可能的循环导入（简化版）
    
    参数:
        code: 当前模块的代码
        module_name: 当前模块的名字（用于检测导入自己）
    
    返回:
        dict: 循环导入检测结果
    """
    dependencies = analyze_dependencies(code)
    modules = dependencies['modules']
    
    warnings = []
    
    # 1. 检测导入自己（直接循环）
    if module_name in modules:
        warnings.append(f"⚠️ 模块导入了自己: import {module_name}")
    
    # 2. 检测常见的循环导入模式
    suspicious_pairs = [
        ('a', 'b'), ('b', 'a'),
        ('utils', 'helpers'), ('helpers', 'utils'),
        ('models', 'schemas'), ('schemas', 'models')
    ]
    
    # 这里可以扩展更多检测逻辑
    # 实际项目中需要解析整个项目，这里只是示例
    
    return {
        'has_circular': len(warnings) > 0,
        'warnings': warnings,
        'warning_count': len(warnings)
    }


def get_dependency_tree(code):
    """
    生成简单的依赖树（文本格式）
    
    示例输出:
        os
        sys
        json
        └── datetime
    """
    dependencies = analyze_dependencies(code)
    
    tree_lines = ["依赖关系树:"]
    for i, module in enumerate(dependencies['modules']):
        if i == len(dependencies['modules']) - 1:
            tree_lines.append(f"└── {module}")
        else:
            tree_lines.append(f"├── {module}")
    
    return "\n".join(tree_lines)


# 然后修改测试部分，添加新功能的测试



# 测试代码
if __name__ == "__main__":
    print("=== dependency.py 测试 ===\n")
    
    # 测试用例1：简单导入
    test1 = '''import os
import sys
import json
from datetime import datetime'''
    
    print("测试1 - 简单导入:")
    result1 = analyze_dependencies(test1)
    print(f"  总导入数: {result1['total_imports']}")
    print(f"  模块列表: {result1['modules']}")
    print(f"  标准库: {result1['standard_libs']}")
    print(f"  依赖分数: {result1['dependency_score']}/100")
    
    # 测试用例2：外部依赖
    test2 = '''import requests
import numpy as np
from flask import Flask
import pandas'''
    
    print("\n测试2 - 外部依赖:")
    result2 = analyze_dependencies(test2)
    print(f"  外部库数量: {result2['external_lib_count']}")
    print(f"  外部库: {result2['external_libs']}")
    print(f"  依赖分数: {result2['dependency_score']}/100")
    
    # 测试用例3：空代码
    print("\n测试3 - 空代码:")
    result3 = analyze_dependencies("")
    print(f"  总导入数: {result3['total_imports']}")
    print(f"  依赖分数: {result3['dependency_score']}/100")
    
    # 测试用例4：循环导入检测
    test4 = '''import os
import sys
import module  # 导入自己'''
    
    print("\n测试4 - 循环导入检测:")
    result4 = detect_circular_imports(test4, "module")
    print(f"  有循环导入: {result4['has_circular']}")
    if result4['warnings']:
        for warning in result4['warnings']:
            print(f"  {warning}")
    
    # 测试用例5：依赖树
    print("\n测试5 - 依赖树:")
    tree = get_dependency_tree(test1)
    print(tree)
    
    print("\n✅ 所有测试完成！")