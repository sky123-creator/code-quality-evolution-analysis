def analyze_comments(code):
    """
    深度分析代码注释
    
    参数:
        code: Python代码字符串
        
    返回:
        dict: 包含注释统计信息
    """
    if not code or code.strip() == "":
        return {
            'total_comments': 0,
            'single_line_comments': 0,
            'inline_comments': 0,
            'todo_count': 0,
            'fixme_count': 0,
            'comment_density': 0.0
        }
    
    lines = code.split('\n')
    total_chars = len(code.replace('\n', ''))
    comment_chars = 0
    
    total_comments = 0
    single_line_comments = 0
    inline_comments = 0
    todo_count = 0
    fixme_count = 0
    
    for line in lines:
        stripped = line.strip()
        
        # 纯注释行
        if stripped.startswith("#"):
            total_comments += 1
            single_line_comments += 1
            comment_chars += len(stripped)
            
            # 检查TODO/FIXME
            upper_line = stripped.upper()
            if "TODO" in upper_line:
                todo_count += 1
            if "FIXME" in upper_line:
                fixme_count += 1
                
        # 行内注释（有代码也有#注释）
        elif "#" in line:
            total_comments += 1
            inline_comments += 1
            # 只统计#后面的字符数
            comment_part = line.split("#", 1)[1]
            comment_chars += len(comment_part.strip())
    
    # 计算注释密度
    comment_density = comment_chars / total_chars if total_chars > 0 else 0.0
    
    return {
        'total_comments': total_comments,
        'single_line_comments': single_line_comments,
        'inline_comments': inline_comments,
        'todo_count': todo_count,
        'fixme_count': fixme_count,
        'comment_density': round(comment_density, 4)
    }


def calculate_comment_rate(code):
    """
    计算注释率（基于行数）
    
    参数:
        code: Python代码字符串
        
    返回:
        float: 注释率（0-1）
    """
    from .loc import calculate_loc  # 导入自己的loc模块
    
    loc_info = calculate_loc(code)
    total = loc_info['total_lines']
    comments = loc_info['comment_lines']
    
    return comments / total if total > 0 else 0.0


if __name__ == "__main__":
    print("=== comment.py 测试 ===")
    
    test_code = '''# TODO: 添加错误处理
print("hello world")  # 打印欢迎信息
# 这是普通注释
def func():
    """文档字符串不算注释"""
    pass
# FIXME: 需要优化性能'''
    
    result = analyze_comments(test_code)
    print("注释分析结果:")
    for key, value in result.items():
        print(f"  {key}: {value}")
    
    rate = calculate_comment_rate(test_code)
    print(f"\n注释率: {rate:.2%}")