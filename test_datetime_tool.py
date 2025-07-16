#!/usr/bin/env python3
"""
测试新添加的时间工具
"""

from tools import DateTimeTool

def test_datetime_tool():
    """测试时间工具的各种格式"""
    print("=== 测试时间工具 ===")
    
    # 创建时间工具实例
    datetime_tool = DateTimeTool()
    
    # 测试不同的格式
    formats = ["full", "date", "time", "timestamp", "iso"]
    
    for format_type in formats:
        print(f"\n测试格式: {format_type}")
        try:
            result = datetime_tool._run(format_type=format_type)
            print(f"结果: {result}")
        except Exception as e:
            print(f"错误: {str(e)}")
    
    # 测试默认格式
    print(f"\n测试默认格式:")
    try:
        result = datetime_tool._run()
        print(f"结果: {result}")
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    test_datetime_tool()
