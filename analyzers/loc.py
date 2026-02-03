def calculate_loc(code):
    """
    统计代码行数信息
    
    参数:
        code: 字符串形式的Python代码
        
    返回:
        字典，包含:
        - total_lines: 总行数
        - code_lines: 代码行数（排除空行和纯注释）
        - comment_lines: 纯注释行数（以#开头的行）
        - blank_lines: 空行数
        - comment_rate: 注释率（comment_lines/total_lines）
    """
    if not code or code.strip() == "":
        return {
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'comment_rate': 0.0
        }
    
    lines = code.split('\n')
    total_lines = len(lines)
    
    code_lines = 0
    comment_lines = 0
    blank_lines = 0
    
    for line in lines:
        stripped_line = line.strip()
        
        if stripped_line == "":
            blank_lines += 1
        elif stripped_line.startswith("#"):
            comment_lines += 1
        else:
            code_lines += 1
    
    comment_rate = comment_lines / total_lines if total_lines > 0 else 0.0
    
    return {
        'total_lines': total_lines,
        'code_lines': code_lines,
        'comment_lines': comment_lines,
        'blank_lines': blank_lines,
        'comment_rate': round(comment_rate, 4)
    }


# 测试代码
if __name__ == "__main__":
    # 测试用例1：简单代码
    test_code1 = '''print("hello")
# 这是一个注释
x = 1 + 2

y = 3  # 行内注释'''
    
    print("=== 测试用例1 ===")
    result1 = calculate_loc(test_code1)
    for key, value in result1.items():
        print(f"{key}: {value}")
    
    # 测试用例2：空代码
    print("\n=== 测试用例2（空代码）===")
    result2 = calculate_loc("")
    for key, value in result2.items():
        print(f"{key}: {value}")
    
    # 测试用例3：只有注释
    print("\n=== 测试用例3（只有注释）===")
    test_code3 = '''# 注释1
# 注释2
# 注释3'''
    result3 = calculate_loc(test_code3)
    for key, value in result3.items():
        print(f"{key}: {value}")
    
    print("\n=== 所有测试完成 ===")