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
## 基础使用
（分析单个Python 文件 / 目录）
#分析单个文件
python main.py --target ./example/project/test.py --output ./reports/single_file_report.html
#分析整个目录
python main.py --target ./example/project/ --output ./reports/dir_report.html
## 分析 Git 项目历史版本（演化追踪）
#分析指定Git仓库，对比最近5次提交的质量变化
python main.py --git-repo ./your_python_project/ --commit-count 5 --output ./reports/evolution_report.html

#分析指定提交区间（哈希/分支/标签）
python main.py --git-repo ./your_python_project/ --start-commit abc123 --end-commit def456 --output ./reports/interval_report.html
## 自定义质量指标规则
#使用自定义配置文件分析
python main.py --target ./example/project/ --config ./custom_config.yaml --output ./reports/custom_report.html
## 输出格式说明
（工具支持多种输出格式，通过--format参数指定：）
#输出JSON（便于二次开发）
python main.py --target ./example/project/ --format json --output ./reports/report.json
#输出Markdown（便于文档集成）
python main.py --target ./example/project/ --format md --output ./reports/report.md
#输出可视化HTML（默认，含图表）
python main.py --target ./example/project/ --format html --output ./reports/report.html
# 核心功能模板
|模块名称 |	作用 |	核心文件
|语法解析模块 |	基于 AST/LibCST 解析 Python 代码，生成语法树，提取代码结构信息 |	core/parser.py
|质量指标计算模块 |	计算圈复杂度、代码行数、注释率、命名规范等量化指标	 | core/metrics_calculator.py
|Git 版本分析模块 |	拉取 Git 仓库历史提交，提取不同版本的代码文件，适配多版本对比 |	core/git_analyzer.py
|演化追踪模块 |	对比不同版本的质量指标，计算变化率，识别质量退化 / 提升的关键节点 | core/evolution_tracker.py
|可视化模块 |	生成折线图（趋势）、热力图（模块质量分布）、表格（指标详情） |	core/visualizer.py
|报告生成模块 |	整合分析结果，输出 HTML/JSON/Markdown 格式的可视化报告 |	core/report_generator.py
# 质量量化指标说明
|指标名称 |	计算方式 |	说明
|圈复杂度  |	基于 AST 计算分支、循环、条件语句数量，公式：1 + 判定节点数 |	反映代码逻辑复杂度，阈值建议≤10（超过则需重构）
|代码行数（LOC） |	统计有效代码行数（排除空行、注释行） |	单函数 LOC≤50 为优，超过则需拆分
|注释率 |	注释行数 / (代码行数 + 注释行数) × 100% |	建议核心模块注释率≥20%，保证可维护性
|命名规范合规率 |	检查变量 / 函数 / 类名是否符合 PEP8（小写下划线 / 大驼峰） |	合规率 100% 为优，避免命名混乱
|函数参数个数 |	统计函数入参数量	| 建议≤5 个，超过则需封装为对象
|重复代码率 |	基于 AST 结构对比，统计重复代码块占比 |	重复率≤5% 为优，超过则需提取公共函数 / 类
|未使用导入率 |	统计 import 但未使用的模块占比 |	建议 0%，减少冗余依赖
# 常见问题
1.问题：运行时提示LibCSTError: Syntax error in file
解决方案：检查目标 Python 文件是否存在语法错误，LibCST 对非法语法解析会报错，需先修复代码语法问题。
2.问题：分析 Git 仓库时提示GitCommandError: Cmd('git') failed
解决方案：确认本地已安装 Git 且配置了环境变量，目标目录是合法的 Git 仓库（含.git 文件夹），且有读取权限。
3.问题：可视化报表无图表显示
解决方案：检查 matplotlib/seaborn 是否安装成功，若为 Linux 环境需安装依赖：sudo apt-get install python3-tk。
4.问题：分析大项目时速度慢
解决方案：在配置文件中增加ignore_dirs，排除 venv、tests、docs 等非核心目录；或使用--workers参数开启多线程：
python main.py --target ./large_project/ --workers 4 --output ./reports/large_report.html
5.问题：自定义指标不生效
解决方案：检查 config.yaml 中指标配置格式是否正确，需严格遵循 YAML 语法，且指标名称与核心模块定义一致。
# 贡献指南

# 许可证
