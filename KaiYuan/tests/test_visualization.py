import pytest
import os
from visualization import (
    plot_project_trend,
    plot_project_comparison,
    plot_metric_correlation,
    plot_metric_heatmap
)

# 测试用例
class TestVisualization:
    """测试可视化模块的图表生成功能"""
    
    @pytest.fixture
    def sample_data_paths(self):
        """返回示例数据文件路径（需确保sample_data目录存在）"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return {
            "trend": os.path.join(base_dir, "sample_data", "flask_trend.csv"),
            "comparison": os.path.join(base_dir, "sample_data", "framework_comparison.csv"),
            "correlation": os.path.join(base_dir, "sample_data", "code_metrics_correlation.csv"),
            "heatmap": os.path.join(base_dir, "sample_data", "flask_module_heatmap.csv")
        }
    
    @pytest.fixture
    def test_output_dir(self, tmp_path):
        """创建临时输出目录"""
        output_dir = tmp_path / "test_plots"
        return str(output_dir)
    
    # 测试趋势图生成
    def test_trend_plotter(self, sample_data_paths, test_output_dir):
        output_path = plot_project_trend(
            csv_path=sample_data_paths["trend"],
            output_dir=test_output_dir
        )
        # 验证文件存在且是PNG格式
        assert os.path.exists(output_path)
        assert output_path.endswith(".png")
        # 验证文件大小（非空）
        assert os.path.getsize(output_path) > 0
    
    # 测试对比图生成
    def test_comparison_plotter(self, sample_data_paths, test_output_dir):
        output_path = plot_project_comparison(
            csv_path=sample_data_paths["comparison"],
            metric_col="注释率",
            output_dir=test_output_dir
        )
        assert os.path.exists(output_path)
        assert output_path.endswith(".png")
        assert os.path.getsize(output_path) > 0
    
    # 测试关联分析图生成
    def test_correlation_plotter(self, sample_data_paths, test_output_dir):
        output_path = plot_metric_correlation(
            csv_path=sample_data_paths["correlation"],
            x_col="代码行数",
            y_col="圈复杂度",
            output_dir=test_output_dir
        )
        assert os.path.exists(output_path)
        assert output_path.endswith(".png")
        assert os.path.getsize(output_path) > 0
    
    # 测试热力图生成
    def test_heatmap_plotter(self, sample_data_paths, test_output_dir):
        output_path = plot_metric_heatmap(
            csv_path=sample_data_paths["heatmap"],
            output_dir=test_output_dir
        )
        assert os.path.exists(output_path)
        assert output_path.endswith(".png")
        assert os.path.getsize(output_path) > 0