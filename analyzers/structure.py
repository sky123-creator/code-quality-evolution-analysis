"""
类结构分析器
分析Python代码中的类、方法、继承关系
"""

import ast

def analyze_structure(code):
    """
    分析代码的类结构
    
    参数:
        code: Python代码字符串
        
    返回:
        dict: 包含类结构信息的字典
    """
    if not code or code.strip() == "":
        return {
            'class_count': 0,
            'method_count': 0,
            'max_inheritance_depth': 0,
            'avg_methods_per_class': 0,
            'classes': [],
            'error': None
        }
    
    try:
        tree = ast.parse(code)
        
        # 存储所有类信息
        classes = []
        total_methods = 0
        
        # 遍历AST找类定义
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = analyze_class(node)
                classes.append(class_info)
                total_methods += class_info['method_count']
        
        # 计算统计数据
        class_count = len(classes)
        
        # 最大继承深度
        max_depth = 0
        for cls in classes:
            if cls['inheritance_depth'] > max_depth:
                max_depth = cls['inheritance_depth']
        
        # 平均方法数
        avg_methods = total_methods / class_count if class_count > 0 else 0
        
        return {
            'class_count': class_count,
            'method_count': total_methods,
            'max_inheritance_depth': max_depth,
            'avg_methods_per_class': round(avg_methods, 2),
            'classes': classes,
            'error': None
        }
        
    except SyntaxError as e:
        return {
            'class_count': 0,
            'method_count': 0,
            'max_inheritance_depth': 0,
            'avg_methods_per_class': 0,
            'classes': [],
            'error': f'语法错误：第{e.lineno}行 {e.msg}'
        }


def analyze_class(class_node):
    """
    分析单个类的结构
    """
    # 类名
    class_name = class_node.name
    
    # 继承深度：统计基类数量
    inheritance_depth = len(class_node.bases) if class_node.bases else 0
    
    # 基类列表
    base_classes = []
    for base in class_node.bases:
        if isinstance(base, ast.Name):
            base_classes.append(base.id)
        elif isinstance(base, ast.Attribute):
            base_classes.append(ast.unparse(base))
    
    # 统计方法
    method_count = 0
    method_types = {
        'instance_methods': 0,
        'class_methods': 0,
        'static_methods': 0
    }
    
    for item in class_node.body:
        if isinstance(item, ast.FunctionDef):
            method_count += 1
            method_name = item.name
            
            # 判断方法类型
            if method_name == '__init__':
                method_types['instance_methods'] += 1
            elif has_decorator(item, 'classmethod'):
                method_types['class_methods'] += 1
            elif has_decorator(item, 'staticmethod'):
                method_types['static_methods'] += 1
            else:
                method_types['instance_methods'] += 1
    
    return {
        'name': class_name,
        'inheritance_depth': inheritance_depth,
        'base_classes': base_classes,
        'method_count': method_count,
        'method_types': method_types,
        'line_number': class_node.lineno
    }


def has_decorator(func_node, decorator_name):
    """
    检查函数是否有特定装饰器
    """
    for decorator in func_node.decorator_list:
        if isinstance(decorator, ast.Name):
            if decorator.id == decorator_name:
                return True
        elif isinstance(decorator, ast.Attribute):
            if decorator.attr == decorator_name:
                return True
    return False


# 测试代码
if __name__ == "__main__":
    print("=== structure.py 类结构分析器测试 ===\n")
    
    # 测试用例1：简单类
    test1 = '''class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return "..."'''
    
    print("1. 简单类（无继承）:")
    result1 = analyze_structure(test1)
    print(f"   类数量: {result1['class_count']}")
    print(f"   方法数量: {result1['method_count']}")
    print(f"   继承深度: {result1['max_inheritance_depth']}")
    
    # 测试用例2：继承结构
    test2 = '''class Animal:
    pass

class Mammal(Animal):
    pass

class Dog(Mammal):
    def bark(self):
        return "Woof!"
    
    @classmethod
    def create_puppy(cls):
        return Dog()
    
    @staticmethod
    def is_pet():
        return True'''
    
    print("\n2. 多层继承结构:")
    result2 = analyze_structure(test2)
    print(f"   类数量: {result2['class_count']}")
    print(f"   最大继承深度: {result2['max_inheritance_depth']}")
    print(f"   平均方法数: {result2['avg_methods_per_class']}")
    
    if result2['classes']:
        print("   类详情:")
        for cls in result2['classes']:
            print(f"     - {cls['name']}: {cls['method_count']}个方法")
    
    # 测试用例3：没有类的代码
    test3 = '''def standalone_function():
    return 42
    
x = 10'''
    
    print("\n3. 无类代码:")
    result3 = analyze_structure(test3)
    print(f"   类数量: {result3['class_count']}")
    print(f"   方法数量: {result3['method_count']}")
    
    # 测试用例4：语法错误
    test4 = '''class BadClass
    def missing_colon'''
    
    print("\n4. 语法错误测试:")
    result4 = analyze_structure(test4)
    if result4['error']:
        print(f"   ✅ 正确捕获: {result4['error']}")
    
    print("\n" + "="*50)
    print("✅ structure.py 测试完成！")
    print("="*50)