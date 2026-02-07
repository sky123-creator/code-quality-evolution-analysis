# code-quality-evolution-analysis
基于 AST/LibCST 的 Python 项目代码质量量化分析与演化追踪
# 项目介绍
## 背景与目标
随着Python项目迭代，代码规模扩大、版本更迭频繁，传统的人工评审难以高效把控代码质量，且无法直观追踪质量演化趋势。本工具基于抽象语法树（AST）和 LibCST（更友好的 Python 语法分析库），深度解析 Python 代码结构，实现多维度质量指标量化、历史版本对比、演化趋势可视化，帮助研发团队：
### 自动化检测代码规范问题、复杂度瓶颈；
### 追溯版本迭代中代码质量的变化规律；
### 定位质量退化的关键提交与模块；
### 建立可量化的代码质量评估体系。
## 核心优势
基于 LibCST+AST 双引擎，兼顾语法分析的精准性与代码修改追踪能力；支持自定义质量指标规则，适配不同团队的编码规范；输出可视化报表（折线图 / 热力图），直观展示质量演化；兼容 Git 版本管理，可分析任意历史提交的代码质量。
# 环境要求
Windows 10+/Linux (Ubuntu 18.04+)/macOS 12+
## 软件要求
Python 3.8 - 3.11（LibCST 暂不兼容 3.12+）；
Git（需分析历史版本时，需本地安装并配置 Git 环境）；
## Python核心依赖
libcst>=1.0.0
astroid>=3.0.0
pandas>=1.5.0
matplotlib>=3.7.0
seaborn>=0.12.0
gitpython>=3.1.0
typing-extensions>=4.5.0
# 安装步骤
1.克隆代码仓库
git clone https://github.com/你的用户名/PythonCodeQualityTracker.git
cd PythonCodeQualityTracker
2.安装依赖
(推荐使用虚拟环境隔离依赖)
/
# 创建虚拟环境
python -m venv venv
# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
/
3.配置工具（可选）
（复制配置模板并自定义质量指标阈值、分析范围：）
/
cp config.example.yaml config.yaml
# 编辑config.yaml，可配置：
# - 忽略分析的目录/文件（如venv、tests）
# - 复杂度阈值、代码规范检查规则
# - 可视化报表的输出路径
# - Git仓库路径（若分析外部项目）
/
# 使用方法

# 核心功能模板
# 质量量化指标说明
# 常见问题
# 贡献指南
# 许可证
