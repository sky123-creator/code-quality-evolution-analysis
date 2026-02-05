import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_metric_heatmap(csv_path, output_dir="output", figsize=(12, 8)):
    """
    绘制多版本多模块的热力图，展示数据分布
    :param csv_path: CSV数据文件路径（列：版本、模块1、模块2...）
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
    
    # 3. 数据处理（版本作为索引，模块作为列）
    version_col = "版本"
    if version_col not in df.columns:
        raise ValueError("CSV文件必须包含「版本」列作为行索引")
    
    # 4. 设置版本为索引，去除无关列
    heatmap_data = df.set_index(version_col)
    
    # 5. 设置matplotlib中文支持
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False
    
    # 6. 绘制热力图
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        heatmap_data,
        ax=ax,
        cmap="YlOrRd",  # 颜色映射（黄-橙-红）
        annot=True,     # 标注数值
        fmt="d",        # 数值格式（整数）
        cbar_kws={"label": "圈复杂度"},  # 颜色条标签
        linewidths=0.5  # 格子边框宽度
    )
    
    # 7. 图表美化
    ax.set_title("项目各版本各模块圈复杂度分布热力图", fontsize=14, pad=20)
    ax.set_xlabel("模块", fontsize=12)
    ax.set_ylabel("版本", fontsize=12)
    
    # 8. 保存图表
    output_path = os.path.join(output_dir, "module_metric_heatmap.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    
    print(f"热力图已保存至：{output_path}")
    return output_path