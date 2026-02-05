"""
代码质量分析指标计算器
"""

from .loc import calculate_loc
from .comment import analyze_comments, calculate_comment_rate

__all__ = [
    'calculate_loc',
    'analyze_comments', 
    'calculate_comment_rate'
]

__version__ = '0.1.0'