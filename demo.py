# 第一步：强制添加项目根目录到Python路径
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# 第二步：导入可视化函数（双保险：直接从具体文件导入）
from visualization.trend_plotter import plot_project_trend
from visualization.comparison_plotter import plot_project_comparison
from visualization.correlation_plotter import plot_metric_correlation
from visualization.heatmap_plotter import plot_metric_heatmap

# 示例数据路径
SAMPLE_DATA_DIR = "sample_data"
OUTPUT_DIR = "output"

if __name__ == "__main__":
    # 1. 生成趋势图
    plot_project_trend(
        csv_path=f"{SAMPLE_DATA_DIR}/flask_trend.csv",
        output_dir=OUTPUT_DIR
    )
    
    # 2. 生成对比图
    plot_project_comparison(
        csv_path=f"{SAMPLE_DATA_DIR}/framework_comparison.csv",
        metric_col="注释率",
        output_dir=OUTPUT_DIR
    )
    
    # 3. 生成关联分析图
    plot_metric_correlation(
        csv_path=f"{SAMPLE_DATA_DIR}/code_metrics_correlation.csv",
        x_col="代码行数",
        y_col="圈复杂度",
        output_dir=OUTPUT_DIR
    )
    
    # 4. 生成热力图
    plot_metric_heatmap(
        csv_path=f"{SAMPLE_DATA_DIR}/flask_module_heatmap.csv",
        output_dir=OUTPUT_DIR
    )
    
    print("所有图表已生成完成，保存在 output/ 目录下！")