def calculate_loc(code):
    """统计代码行数信息"""
    if not code:
        return {
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'inline_comment_lines': 0,
            'blank_lines': 0,
            'comment_rate': 0
        }
    
    lines = code.split('\n')
    total_lines = len(lines)
    
    code_lines = 0
    comment_lines = 0
    inline_comment_lines = 0
    blank_lines = 0
    
    for line in lines:
        line_stripped = line.strip()
        
        if line_stripped == '':
            blank_lines += 1
        elif line_stripped.startswith('#'):
            comment_lines += 1
        elif '#' in line:
            inline_comment_lines += 1
            code_lines += 1
        else:
            code_lines += 1
    
    comment_rate = comment_lines / total_lines if total_lines > 0 else 0
    
    return {
        'total_lines': total_lines,
        'code_lines': code_lines,
        'comment_lines': comment_lines,
        'inline_comment_lines': inline_comment_lines,
        'blank_lines': blank_lines,
        'comment_rate': round(comment_rate, 3)
    }

# 测试
if __name__ == "__main__":
    test_code = """print('hello')
# 这是纯注释行
x = 1 + 2  # 这是行内注释

y = 3
z = 4  # 另一个行内注释"""
    
    result = calculate_loc(test_code)
    print("=== 测试结果 ===")
    for key, value in result.items():
        print(f"{key}: {value}")
    
    print("\n=== 验证 ===")
    print(f"总行数 {result['total_lines']} = "
          f"代码{result['code_lines']} + "
          f"纯注释{result['comment_lines']} + "
          f"行内注释{result['inline_comment_lines']} + "
          f"空行{result['blank_lines']}")