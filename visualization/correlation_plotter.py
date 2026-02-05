import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os

def plot_metric_correlation(csv_path, x_col="代码行数", y_col="圈复杂度", output_dir="output", figsize=(10, 6)):
    """
    绘制两个指标的散点图+趋势线，分析关联关系
    :param csv_path: CSV数据文件路径（包含两个指标列）
    :param x_col: X轴指标列名
    :param y_col: Y轴指标列名
    :param output_dir: 图表输出目录
    :param figsize: 图表尺寸
    :return: 生成的图表文件路径
    """
    # 1. 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 2. 读取CSV数据
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise ValueError(f"读取CSV文件失败：{str(e)}")
    
    # 3. 数据校验
    required_columns = [x_col, y_col]
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"CSV文件缺少必要列，要求：{required_columns}")
    
    # 4. 去除缺失值（避免计算错误）
    df = df.dropna(subset=[x_col, y_col])
    if len(df) == 0:
        raise ValueError("数据中无有效指标值（已去除所有缺失值）")
    
    # 5. 设置matplotlib中文支持
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False
    
    # 6. 计算线性回归（趋势线）
    x = df[x_col].values
    y = df[y_col].values
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    trend_line = slope * x + intercept
    
    # 7. 绘制散点图+趋势线
    fig, ax = plt.subplots(figsize=figsize)
    ax.scatter(x, y, color="#ff7f0e", alpha=0.7, s=60)  # 散点图
    ax.plot(x, trend_line, color="#d62728", linewidth=2, label=f"趋势线（R²={r_value**2:.4f}）")
    
    # 8. 图表美化
    ax.set_title(f"{x_col} 与 {y_col} 关联分析", fontsize=14, pad=20)
    ax.set_xlabel(x_col, fontsize=12)
    ax.set_ylabel(y_col, fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")
    
    # 9. 保存图表
    output_path = os.path.join(output_dir, f"{x_col}_vs_{y_col}_correlation.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    
    print(f"关联分析图已保存至：{output_path}")
    print(f"关联结果：R²={r_value**2:.4f}（越接近1，相关性越强）")
    return output_path