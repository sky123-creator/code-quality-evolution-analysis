import pytest
import os
import pandas as pd
from tests.test_analyzers import calculate_loc, calculate_comment_rate

# 模拟B同学的流水线函数
def data_analysis_pipeline(input_code_path: str, output_csv_path: str, project_name: str, version: str) -> bool:
    """
    完整数据处理流水线：
    1. 读取输入代码文件
    2. 计算指标（行数、注释率）
    3. 输出CSV文件
    :param input_code_path: 输入代码文件路径
    :param output_csv_path: 输出CSV文件路径
    :param project_name: 项目名称
    :param version: 项目版本
    :return: 流水线是否执行成功（bool）
    """
    try:
        # 步骤1：读取代码文件
        if not os.path.exists(input_code_path):
            raise FileNotFoundError(f"代码文件不存在：{input_code_path}")
        
        with open(input_code_path, "r", encoding="utf-8") as f:
            code_content = f.read()
        
        # 步骤2：计算指标
        loc = calculate_loc(code_content)
        comment_rate = calculate_comment_rate(code_content)
        
        # 步骤3：构造输出数据并保存为CSV
        output_data = {
            "项目": [project_name],
            "版本": [version],
            "代码行数": [loc],
            "注释率": [comment_rate]
        }
        df = pd.DataFrame(output_data)
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_csv_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
        
        return True
    except Exception as e:
        print(f"流水线执行失败：{str(e)}")
        return False

# 集成测试用例
class TestDataPipeline:
    """测试B同学的完整数据处理流水线"""
    
    @pytest.fixture
    def test_code_file(self, tmp_path):
        """创建临时测试代码文件（fixture，每个用例自动清理）"""
        code_content = """# 测试项目
print('Hello World')
x = 10
if x > 5:
    print('x is greater than 5')
// 另一个注释
y = x * 2
"""
        code_file = tmp_path / "test_project.py"
        code_file.write_text(code_content, encoding="utf-8")
        return str(code_file)
    
    @pytest.fixture
    def test_output_csv(self, tmp_path):
        """创建临时输出CSV路径"""
        return str(tmp_path / "test_output.csv")
    
    def test_pipeline_success(self, test_code_file, test_output_csv):
        """测试流水线正常执行（成功生成CSV）"""
        # 执行流水线
        result = data_analysis_pipeline(
            input_code_path=test_code_file,
            output_csv_path=test_output_csv,
            project_name="TestProject",
            version="v1.0"
        )
        
        # 验证结果
        assert result is True
        assert os.path.exists(test_output_csv)
        
        # 验证CSV内容是否正确
        df = pd.read_csv(test_output_csv)
        assert df["项目"].iloc[0] == "TestProject"
        assert df["版本"].iloc[0] == "v1.0"
        assert df["代码行数"].iloc[0] == 4  # 有效代码行：print、x=10、if块、y=x*2
        assert 0.3 < df["注释率"].iloc[0] < 0.5  # 注释率：2/6 ≈ 0.333
    
    def test_pipeline_input_file_not_exist(self, test_output_csv):
        """测试输入文件不存在的情况（流水线返回失败）"""
        non_exist_file = "non_exist_file.py"
        result = data_analysis_pipeline(
            input_code_path=non_exist_file,
            output_csv_path=test_output_csv,
            project_name="TestProject",
            version="v1.0"
        )
        assert result is False
    
    def test_pipeline_output_dir_create(self, test_code_file, tmp_path):
        """测试输出目录不存在时，流水线自动创建目录"""
        non_exist_dir = tmp_path / "non_exist_dir"
        output_csv = str(non_exist_dir / "test_output.csv")
        
        # 执行流水线
        result = data_analysis_pipeline(
            input_code_path=test_code_file,
            output_csv_path=output_csv,
            project_name="TestProject",
            version="v1.0"
        )
        
        # 验证目录和文件是否创建成功
        assert result is True
        assert os.path.exists(non_exist_dir)
        assert os.path.exists(output_csv)