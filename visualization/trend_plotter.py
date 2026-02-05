import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_project_trend(csv_path, output_dir="output", figsize=(10, 6)):
    """
    绘制单个项目各版本指标变化折线图
    :param csv_path: CSV数据文件路径（列：项目、版本、指标值）
    :param output_dir: 图表输出目录
    :param figsize: 图表尺寸
    :return: 生成的图表文件路径
    """
    # 1. 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)
    
    # 2. 读取CSV数据
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise ValueError(f"读取CSV文件失败：{str(e)}")
    
    # 3. 数据校验（确保列名正确）
    required_columns = ["项目", "版本", "指标值"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"CSV文件缺少必要列，要求：{required_columns}")
    
    # 4. 获取项目名称（单个项目）
    project_name = df["项目"].unique()[0]
    if len(df["项目"].unique()) > 1:
        print(f"警告：CSV中包含多个项目，仅绘制第一个项目「{project_name}」")
    
    # 5. 设置matplotlib中文支持（避免中文乱码）
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 黑体
    plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
    
    # 6. 绘制折线图
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(df["版本"], df["指标值"], marker="o", linewidth=2, color="#2f74c0")
    
    # 7. 图表美化（标题、坐标轴标签）
    ax.set_title(f"{project_name} 各版本指标变化趋势", fontsize=14, pad=20)
    ax.set_xlabel("版本", fontsize=12)
    ax.set_ylabel("指标值", fontsize=12)
    ax.grid(True, alpha=0.3, axis="y")
    ax.set_ylim(bottom=0)  # Y轴从0开始
    
    # 8. 保存图表
    output_path = os.path.join(output_dir, f"{project_name}_trend.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    
    print(f"趋势图已保存至：{output_path}")
    return output_path