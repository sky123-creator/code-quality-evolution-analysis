import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 尝试导入自定义可视化函数，失败则直接启用内置绘图
try:
    from visualization.trend_plotter import plot_project_trend
    from visualization.comparison_plotter import plot_project_comparison
    from visualization.correlation_plotter import plot_metric_correlation
    from visualization.heatmap_plotter import plot_metric_heatmap
    CUSTOM_FUNC_AVAILABLE = True
    print("✅ Custom visualization functions imported successfully, will try to call")
except ImportError as e:
    CUSTOM_FUNC_AVAILABLE = False
    print(f"ℹ️  Custom visualization functions import failed ({e}), use built-in plotting logic directly")

# ==================== Core Configuration: 100% Compatibility ====================
PIPELINE_CSV_PATH = r"D:\code-quality-evolution-analysis-workspace\pipeline\output\flask_quality_metrics.csv"
OUTPUT_DIR = "output"
PLOT_DPI = 300
# 三框架配色 + 对应matplotlib内置色板（全版本兼容，无自定义颜色拼接）
FRAMEWORK_CONFIG = {
    "django": {"color": "#E63946", "cmap": "Reds"},    # 红色系内置色板
    "fastapi": {"color": "#06D6A0", "cmap": "Greens"},  # 绿色系内置色板
    "flask": {"color": "#2E86AB", "cmap": "Blues"}      # 蓝色系内置色板
}
# ================================================================================

# Auto create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Check if CSV file exists
if not os.path.exists(PIPELINE_CSV_PATH):
    print(f"\n❌ Error: Three frameworks CSV file not found!")
    print(f"Please run first: git checkout integrate-all-modules && py pipeline/batch_processor.py && git checkout main")
    sys.exit(1)

# Read and preprocess data: sort by framework + version
df = pd.read_csv(PIPELINE_CSV_PATH, encoding="utf-8-sig")
df = df.sort_values(["project_name", "version"]).reset_index(drop=True)

# Data preview in console
print(f"\n✅ Successfully read pipeline analysis data: {len(df)} version records in total")
print(f"✅ Frameworks included: {df['project_name'].unique().tolist()} (Total {df['project_name'].nunique()})")
for frame in df['project_name'].unique():
    print(f"   └─ {frame.upper()}: {len(df[df['project_name'] == frame])} versions")
print(f"✅ Core data columns: {list(df.columns)}")

# Detailed data preview
preview_cols = ["project_name", "version", "file_count", "loc", "comment_rate", "avg_complexity"]
print(f"\n📊 Three Frameworks Data Preview:")
print(df[preview_cols].to_string(index=False))

# ==================== Built-in Plotting Logic: No Error / No Warning ====================
def plot_builtin_trend():
    """Three Frameworks: LOC + Avg Complexity Dual-Y Trend Chart (Core)"""
    plt.figure(figsize=(14, 7))
    ax1 = plt.gca()
    # Primary Y: Lines of Code (LOC)
    sns.lineplot(
        x="version", y="loc", hue="project_name", data=df,
        marker="o", linewidth=2.5, markersize=9, 
        palette=[FRAMEWORK_CONFIG[f]["color"] for f in df['project_name'].unique()],
        ax=ax1
    )
    ax1.set_ylabel("Lines of Effective Code", fontsize=14, fontweight="500")
    ax1.tick_params(axis='y', labelsize=12)

    # Secondary Y: Average Cyclomatic Complexity (dark color scheme)
    ax2 = ax1.twinx()
    dark_colors = [c["color"].replace("6", "3").replace("A", "7").replace("0", "7") for c in FRAMEWORK_CONFIG.values()]
    sns.lineplot(
        x="version", y="avg_complexity", hue="project_name", data=df,
        marker="s", linewidth=2.5, markersize=9, palette=dark_colors,
        ax=ax2, legend=False  # Close secondary Y legend to avoid duplication
    )
    ax2.set_ylabel("Average Cyclomatic Complexity", fontsize=14, fontweight="500")
    ax2.tick_params(axis='y', labelsize=12)

    # Chart style
    plt.title("Flask & Django & FastAPI Version Evolution - LOC + Avg Complexity Trend", 
              fontsize=16, fontweight="bold", pad=25)
    plt.xlabel("Framework Version", fontsize=14, fontweight="500")
    plt.xticks(rotation=45, fontsize=12)
    plt.grid(alpha=0.3, linestyle="--")
    plt.tight_layout()
    # Save chart
    save_path = os.path.join(OUTPUT_DIR, "3frame_loc_complexity_trend.png")
    plt.savefig(save_path, dpi=PLOT_DPI, bbox_inches="tight", facecolor="white")
    print(f"\n✅ [3-Frame Trend Chart] Saved: {save_path}")
    plt.close()

def plot_builtin_comment_rate():
    """Three Frameworks: Average Comment Rate Bar Chart"""
    plt.figure(figsize=(14, 7))
    sns.barplot(
        x="version", y="comment_rate", hue="project_name", data=df,
        palette=[FRAMEWORK_CONFIG[f]["color"] for f in df['project_name'].unique()],
        edgecolor="white", linewidth=1.2
    )
    plt.title("Flask & Django & FastAPI Average Comment Rate by Version", 
              fontsize=16, fontweight="bold", pad=25)
    plt.xlabel("Framework Version", fontsize=14, fontweight="500")
    plt.ylabel("Average Comment Rate", fontsize=14, fontweight="500")
    plt.xticks(rotation=45, fontsize=12)
    plt.legend(title="Framework", title_fontsize=12, fontsize=10)
    plt.grid(alpha=0.3, linestyle="--", axis="y")
    plt.tight_layout()
    save_path = os.path.join(OUTPUT_DIR, "3frame_comment_rate_comparison.png")
    plt.savefig(save_path, dpi=PLOT_DPI, bbox_inches="tight", facecolor="white")
    print(f"✅ [3-Frame Comment Rate Chart] Saved: {save_path}")
    plt.close()

def plot_builtin_correlation():
    """Three Frameworks: LOC vs Avg Complexity Scatter Correlation Chart"""
    plt.figure(figsize=(12, 6))
    sns.scatterplot(
        x="loc", y="avg_complexity", hue="project_name", data=df,
        s=200, marker="o", 
        palette=[FRAMEWORK_CONFIG[f]["color"] for f in df['project_name'].unique()],
        edgecolor="white", linewidth=2.5
    )
    # Chart style
    plt.title("LOC vs Average Cyclomatic Complexity Correlation (Flask+Django+FastAPI)", 
              fontsize=16, fontweight="bold", pad=25)
    plt.xlabel("Lines of Effective Code", fontsize=14, fontweight="500")
    plt.ylabel("Average Cyclomatic Complexity", fontsize=14, fontweight="500")
    plt.legend(title="Framework", title_fontsize=12, fontsize=10)
    plt.grid(alpha=0.3, linestyle="--")
    plt.tight_layout()
    save_path = os.path.join(OUTPUT_DIR, "3frame_loc_vs_complexity_correlation.png")
    plt.savefig(save_path, dpi=PLOT_DPI, bbox_inches="tight", facecolor="white")
    print(f"✅ [3-Frame Correlation Chart] Saved: {save_path}")
    plt.close()

def plot_builtin_single_heatmap():
    """Single Framework: Normalized Core Metrics Heatmap (1 per framework, 内置色板兼容)"""
    core_metrics = ["loc", "avg_complexity", "comment_rate", "file_count"]
    for frame in df['project_name'].unique():
        df_single = df[df['project_name'] == frame].set_index("version")
        # Metrics normalization (0-1)
        df_heat = df_single[core_metrics].apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=0)
        # Plot heatmap - 核心修复：使用matplotlib内置色板，无自定义颜色拼接
        plt.figure(figsize=(10, 6))
        sns.heatmap(
            df_heat, annot=True, 
            cmap=FRAMEWORK_CONFIG[frame]["cmap"],  # 全版本兼容的内置色板
            fmt=".2f", linewidths=0.6, annot_kws={"fontsize": 11}
        )
        # Chart style (匹配框架主色)
        plt.title(f"{frame.upper()} Normalized Core Quality Metrics by Version", 
                  fontsize=16, fontweight="bold", pad=25, color=FRAMEWORK_CONFIG[frame]["color"])
        plt.xlabel("Quality Metrics", fontsize=14, fontweight="500")
        plt.ylabel(f"{frame.upper()} Version", fontsize=14, fontweight="500")
        plt.tight_layout()
        save_path = os.path.join(OUTPUT_DIR, f"{frame}_metrics_heatmap.png")
        plt.savefig(save_path, dpi=PLOT_DPI, bbox_inches="tight", facecolor="white")
        print(f"✅ [{frame.upper()} Heatmap] Saved: {save_path}")
        plt.close()

def plot_builtin_file_count():
    """Three Frameworks: Source File Count Line Chart"""
    plt.figure(figsize=(14, 7))
    sns.lineplot(
        x="version", y="file_count", hue="project_name", data=df,
        marker="D", linewidth=2.5, markersize=9,
        palette=[FRAMEWORK_CONFIG[f]["color"] for f in df['project_name'].unique()]
    )
    plt.title("Flask & Django & FastAPI Source File Count by Version", 
              fontsize=16, fontweight="bold", pad=25)
    plt.xlabel("Framework Version", fontsize=14, fontweight="500")
    plt.ylabel("Number of Source Files", fontsize=14, fontweight="500")
    plt.xticks(rotation=45, fontsize=12)
    plt.legend(title="Framework", title_fontsize=12, fontsize=10)
    plt.grid(alpha=0.3, linestyle="--")
    plt.tight_layout()
    save_path = os.path.join(OUTPUT_DIR, "3frame_file_count_trend.png")
    plt.savefig(save_path, dpi=PLOT_DPI, bbox_inches="tight", facecolor="white")
    print(f"✅ [3-Frame File Count Chart] Saved: {save_path}")
    plt.close()

# ==================== Main Execution Logic: Clean & Stable ====================
if __name__ == "__main__":
    print(f"\n===== Start Generating Three Frameworks Visualization Charts ======")
    # Skip custom functions directly (column mismatch permanent)
    if CUSTOM_FUNC_AVAILABLE:
        print(f"\n⚠️  Custom functions skipped: CSV columns do not match required ['项目', '版本', '指标值']")
    print(f"⚠️  Running built-in plotting logic (100% compatible with all matplotlib/seaborn versions)!")
    # Execute all built-in plotting functions
    plot_builtin_trend()
    plot_builtin_comment_rate()
    plot_builtin_correlation()
    plot_builtin_single_heatmap()
    plot_builtin_file_count()

    # Final result summary
    all_charts = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".png")]
    print(f"\n===== 🎉 FINAL SUCCESS! ALL CHARTS GENERATED! 🎉 =====")
    print(f"📁 High-Res Charts Save Path: {os.path.abspath(OUTPUT_DIR)}")
    print(f"📊 Total Charts (300DPI / No Watermark / No Error): {len(all_charts)}")
    for idx, chart in enumerate(all_charts, 1):
        print(f"   {idx}. {chart}")
    print(f"\n💡 All charts are ready for reports/PPT! Raw data: {PIPELINE_CSV_PATH}")
    print(f"💡 Add new frameworks → update FRAMEWORK_CONFIG and add source code in pipeline/target/!")