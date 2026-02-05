import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_project_comparison(csv_path, metric_col="注释率", output_dir="output", figsize=(10, 6)):
    """
    绘制多个项目同一指标的分组柱状图
    :param csv_path: CSV数据文件路径（列：项目、版本、指标列）
    :param metric_col: 要对比的指标列名（默认：注释率）
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
    required_columns = ["项目", "版本", metric_col]
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"CSV文件缺少必要列，要求：{required_columns}")
    
    # 4. 设置matplotlib中文支持
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False
    
    # 5. 绘制分组柱状图
    fig, ax = plt.subplots(figsize=figsize)
    x = range(len(df))
    bars = ax.bar(x, df[metric_col], width=0.6, color="#4cae4c")
    
    # 6. 图表美化
    ax.set_title(f"多个项目 {metric_col} 对比（最新版本）", fontsize=14, pad=20)
    ax.set_xlabel("项目", fontsize=12)
    ax.set_ylabel(metric_col, fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(df["项目"], rotation=0)
    ax.grid(True, alpha=0.3, axis="y")
    ax.set_ylim(bottom=0)
    
    # 7. 柱状图上标注数值
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f"{height:.2f}", ha="center", va="bottom", fontsize=10)
    
    # 8. 保存图表
    output_path = os.path.join(output_dir, f"project_comparison_{metric_col}.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    
    print(f"对比图已保存至：{output_path}")
    return output_path