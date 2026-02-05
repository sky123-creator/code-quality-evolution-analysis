import pytest

# 模拟A同学的指标计算函数（实际项目中替换为A同学的真实代码）
def calculate_loc(code_content: str) -> int:
    """
    计算代码行数（有效代码行，排除空行和注释行（//、#））
    :param code_content: 代码字符串
    :return: 有效代码行数
    """
    if not isinstance(code_content, str):
        raise TypeError("code_content必须是字符串类型")
    
    lines = code_content.split("\n")
    valid_lines = 0
    for line in lines:
        line_stripped = line.strip()
        # 排除空行、Python注释行（#）、Java/JS注释行（//）
        if line_stripped and not line_stripped.startswith(("#", "//")):
            valid_lines += 1
    return valid_lines

def calculate_comment_rate(code_content: str) -> float:
    """
    计算注释率（注释行 / （有效代码行 + 注释行））
    :param code_content: 代码字符串
    :return: 注释率（0~1之间）
    """
    if not isinstance(code_content, str):
        raise TypeError("code_content必须是字符串类型")
    
    lines = code_content.split("\n")
    comment_lines = 0
    valid_code_lines = 0
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        if line_stripped.startswith(("#", "//")):
            comment_lines += 1
        else:
            valid_code_lines += 1
    
    total = valid_code_lines + comment_lines
    return comment_lines / total if total > 0 else 0.0

def calculate_cyclomatic_complexity(control_flow_count: int) -> int:
    """
    计算圈复杂度（简化版：控制流语句数 + 1）
    :param control_flow_count: 控制流语句数（if、for、while等）
    :return: 圈复杂度
    """
    if not isinstance(control_flow_count, int):
        raise TypeError("control_flow_count必须是整数类型")
    if control_flow_count < 0:
        raise ValueError("control_flow_count不能为负数")
    
    return control_flow_count + 1

# 单元测试用例
class TestMetricAnalyzers:
    """测试A同学的指标计算函数"""
    
    # 测试calculate_loc（代码行数计算）
    def test_calculate_loc_basic(self):
        """测试基础有效代码行"""
        code = "print('Hello')\nx = 1 + 2\nif x > 0:\n    print(x)"
        assert calculate_loc(code) == 4
    
    def test_calculate_loc_with_comments(self):
        """测试包含注释的代码行"""
        code = "# 这是注释\nprint('Hello')\n// 另一种注释\nx = 1"
        assert calculate_loc(code) == 2
    
    def test_calculate_loc_with_blank_lines(self):
        """测试包含空行的代码行"""
        code = "print('Hello')\n\nx = 1\n  \ny = 2"
        assert calculate_loc(code) == 3
    
    def test_calculate_loc_invalid_type(self):
        """测试无效输入类型"""
        with pytest.raises(TypeError):
            calculate_loc(12345)
    
    # 测试calculate_comment_rate（注释率计算）
    def test_comment_rate_basic(self):
        """测试基础注释率"""
        code = "# 注释1\nprint('Hello')\n# 注释2\nx = 1"
        assert calculate_comment_rate(code) == 0.5
    
    def test_comment_rate_no_comments(self):
        """测试无注释的情况"""
        code = "print('Hello')\nx = 1"
        assert calculate_comment_rate(code) == 0.0
    
    def test_comment_rate_all_comments(self):
        """测试全是注释的情况"""
        code = "# 注释1\n// 注释2\n# 注释3"
        assert calculate_comment_rate(code) == 1.0
    
    # 测试calculate_cyclomatic_complexity（圈复杂度计算）
    def test_cyclomatic_complexity_basic(self):
        """测试基础圈复杂度"""
        assert calculate_cyclomatic_complexity(3) == 4
    
    def test_cyclomatic_complexity_zero(self):
        """测试控制流语句数为0的情况"""
        assert calculate_cyclomatic_complexity(0) == 1
    
    def test_cyclomatic_complexity_negative(self):
        """测试负数输入（应抛出异常）"""
        with pytest.raises(ValueError):
            calculate_cyclomatic_complexity(-1)