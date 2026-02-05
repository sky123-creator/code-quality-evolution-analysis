# 第一步：先强制将项目根目录加入Python模块搜索路径，解决导入问题
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 第二步：导入可视化模块的核心函数（双保险：直接从具体文件导入，绕过__init__.py可能的问题）
import pytest
from visualization.trend_plotter import plot_project_trend
from visualization.comparison_plotter import plot_project_comparison
from visualization.correlation_plotter import plot_metric_correlation
from visualization.heatmap_plotter import plot_metric_heatmap

# 测试用例
class TestVisualization:
    """测试可视化模块的图表生成功能"""
    
    @pytest.fixture
    def sample_data_paths(self):
        """返回示例数据文件路径（自动适配项目目录结构，避免路径错误）"""
        # 自动获取当前测试文件的目录，向上回溯到项目根目录
        current_test_dir = os.path.dirname(os.path.abspath(__file__))
        project_root_dir = os.path.dirname(current_test_dir)
        sample_data_dir = os.path.join(project_root_dir, "sample_data")
        
        # 确保示例数据目录存在，避免文件找不到报错
        os.makedirs(sample_data_dir, exist_ok=True)
        
        return {
            "trend": os.path.join(sample_data_dir, "flask_trend.csv"),
            "comparison": os.path.join(sample_data_dir, "framework_comparison.csv"),
            "correlation": os.path.join(sample_data_dir, "code_metrics_correlation.csv"),
            "heatmap": os.path.join(sample_data_dir, "flask_module_heatmap.csv")
        }
    
    @pytest.fixture
    def test_output_dir(self, tmp_path):
        """创建临时输出目录，测试完成后自动清理，不残留文件"""
        output_dir = tmp_path / "test_plots"
        os.makedirs(output_dir, exist_ok=True)
        return str(output_dir)
    
    # 测试趋势图生成（验证文件存在、格式正确、非空）
    def test_trend_plotter(self, sample_data_paths, test_output_dir):
        # 先验证示例数据文件存在，避免因数据缺失报错
        assert os.path.exists(sample_data_paths["trend"]), f"趋势图示例数据不存在：{sample_data_paths['trend']}"
        
        output_path = plot_project_trend(
            csv_path=sample_data_paths["trend"],
            output_dir=test_output_dir
        )
        
        # 核心验证：文件存在、是PNG格式、非空（生成有效图表）
        assert os.path.exists(output_path), "趋势图未成功生成"
        assert output_path.endswith(".png"), "趋势图格式不是PNG"
        assert os.path.getsize(output_path) > 0, "趋势图文件为空，生成失败"
    
    # 测试对比图生成
    def test_comparison_plotter(self, sample_data_paths, test_output_dir):
        assert os.path.exists(sample_data_paths["comparison"]), f"对比图示例数据不存在：{sample_data_paths['comparison']}"
        
        output_path = plot_project_comparison(
            csv_path=sample_data_paths["comparison"],
            metric_col="注释率",
            output_dir=test_output_dir
        )
        
        assert os.path.exists(output_path), "对比图未成功生成"
        assert output_path.endswith(".png"), "对比图格式不是PNG"
        assert os.path.getsize(output_path) > 0, "对比图文件为空，生成失败"
    
    # 测试关联分析图生成
    def test_correlation_plotter(self, sample_data_paths, test_output_dir):
        assert os.path.exists(sample_data_paths["correlation"]), f"关联分析图示例数据不存在：{sample_data_paths['correlation']}"
        
        output_path = plot_metric_correlation(
            csv_path=sample_data_paths["correlation"],
            x_col="代码行数",
            y_col="圈复杂度",
            output_dir=test_output_dir
        )
        
        assert os.path.exists(output_path), "关联分析图未成功生成"
        assert output_path.endswith(".png"), "关联分析图格式不是PNG"
        assert os.path.getsize(output_path) > 0, "关联分析图文件为空，生成失败"
    
    # 测试热力图生成
    def test_heatmap_plotter(self, sample_data_paths, test_output_dir):
        assert os.path.exists(sample_data_paths["heatmap"]), f"热力图示例数据不存在：{sample_data_paths['heatmap']}"
        
        output_path = plot_metric_heatmap(
            csv_path=sample_data_paths["heatmap"],
            output_dir=test_output_dir
        )
        
        assert os.path.exists(output_path), "热力图未成功生成"
        assert output_path.endswith(".png"), "热力图格式不是PNG"
        assert os.path.getsize(output_path) > 0, "热力图文件为空，生成失败"