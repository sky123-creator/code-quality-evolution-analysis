import sys
import os
sys.path.append('..')

from analyzers.dependency import analyze_dependencies, detect_circular_imports

def test_basic_imports():
    """测试基础导入"""
    code = "import os\nimport sys"
    result = analyze_dependencies(code)
    assert result['import_count'] == 2
    assert 'os' in result['modules']
    print("✅ test_basic_imports 通过")

def test_from_import():
    """测试from导入"""
    code = "from datetime import datetime"
    result = analyze_dependencies(code)
    assert result['from_import_count'] == 1
    assert 'datetime' in result['modules']
    print("✅ test_from_import 通过")

def test_empty_code():
    """测试空代码"""
    result = analyze_dependencies("")
    assert result['total_imports'] == 0
    assert result['dependency_score'] == 100
    print("✅ test_empty_code 通过")

def test_circular_detection():
    """测试循环导入检测"""
    code = "import mymodule"
    result = detect_circular_imports(code, "mymodule")
    assert result['has_circular'] == True
    print("✅ test_circular_detection 通过")

def test_dependency_score():
    """测试依赖分数"""
    # 无外部依赖应该高分
    code1 = "import os"
    result1 = analyze_dependencies(code1)
    assert result1['dependency_score'] >= 70
    
    # 多个外部依赖应该低分
    code2 = "import requests\nimport numpy\nimport pandas"
    result2 = analyze_dependencies(code2)
    assert result2['dependency_score'] < 70
    print("✅ test_dependency_score 通过")

if __name__ == "__main__":
    test_basic_imports()
    test_from_import()
    test_empty_code()
    test_circular_detection()
    test_dependency_score()
    print("\n🎉 所有依赖测试通过！")