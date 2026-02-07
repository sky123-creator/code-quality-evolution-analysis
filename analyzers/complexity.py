"""
基于Python ast模块的圈复杂度计算器
比字符串匹配更准确
"""

import ast

def calculate_complexity(code):
    """
    计算代码的圈复杂度（AST专业版）
    """
    if not code or code.strip() == "":
        return {
            'cyclomatic_complexity': 1,
            'decision_points': 0,
            'if_count': 0,
            'for_count': 0,
            'while_count': 0,
            'try_count': 0,
            'except_count': 0,
            'error': None
        }
    
    try:
        # 用ast解析代码
        tree = ast.parse(code)
        
        # 初始化计数器
        complexity = 1
        if_count = 0
        for_count = 0
        while_count = 0
        try_count = 0
        except_count = 0
        
        # 遍历所有AST节点
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                if_count += 1
                complexity += 1
            elif isinstance(node, ast.For) or isinstance(node, ast.AsyncFor):
                for_count += 1
                complexity += 1
            elif isinstance(node, ast.While):
                while_count += 1
                complexity += 1
            elif isinstance(node, ast.Try):
                try_count += 1
                complexity += 1
                except_count += len(node.handlers)
                complexity += len(node.handlers)
        
        decision_points = if_count + for_count + while_count + try_count + except_count
        
        return {
            'cyclomatic_complexity': complexity,
            'decision_points': decision_points,
            'if_count': if_count,
            'for_count': for_count,
            'while_count': while_count,
            'try_count': try_count,
            'except_count': except_count,
            'error': None
        }
        
    except SyntaxError as e:
        return {
            'cyclomatic_complexity': 1,
            'decision_points': 0,
            'if_count': 0,
            'for_count': 0,
            'while_count': 0,
            'try_count': 0,
            'except_count': 0,
            'error': f'语法错误：第{e.lineno}行 {e.msg}'
        }

# 测试
if __name__ == "__main__":
    print("=== complexity.py 测试 ===\n")
    
    # 测试1
    test1 = '''if x > 0:
    print("正数")
elif x < 0:
    print("负数")
else:
    print("零")'''
    
    print("1. 多层if判断:")
    result1 = calculate_complexity(test1)
    print(f"   复杂度: {result1['cyclomatic_complexity']}")
    print(f"   if数量: {result1['if_count']}")
    
    # 测试2
    test2 = '''for i in range(10):
    if i % 2 == 0:
        try:
            print(10 / i)
        except:
            print("除零错误")'''
    
    print("\n2. 嵌套结构:")
    result2 = calculate_complexity(test2)
    print(f"   复杂度: {result2['cyclomatic_complexity']}")
    print(f"   决策点: {result2['decision_points']}")
    
    # 测试3
    test3 = '''def bad_code(
    print("括号没闭合"'''
    
    print("\n3. 语法错误:")
    result3 = calculate_complexity(test3)
    if result3['error']:
        print(f"   ✅ 捕获到错误: {result3['error']}")
    
    print("\n✅ complexity.py 创建成功！")