#!/usr/bin/env python3
"""
测试智能体工具功能 (简化版)
"""

import sys
from tools import Calculator, WebSearch, FileOperations, SystemInfo, NetworkTool, get_tools

def test_calculator():
    """测试计算器工具"""
    print("\n=== 测试计算器工具 ===")
    calc = Calculator()
    test_cases = [
        "2 + 3 * 4",
        "sqrt(16)",
        "sin(3.14159/2)",
        "log(10)",
        "2**8"
    ]
    for expression in test_cases:
        result = calc._run(expression)
        print(f"'{expression}' = {result}")

def test_web_search():
    """测试网络搜索工具"""
    print("\n=== 测试网络搜索工具 ===")
    search = WebSearch()
    query = "DeepSeek"
    result = search._run(query)
    print(f"搜索 '{query}':\n{result}")

def test_file_operations():
    """测试文件操作工具"""
    print("\n=== 测试文件操作工具 ===")
    file_ops = FileOperations()
    test_filename = "test_file_ops.txt"
    
    # 写入
    write_result = file_ops._run("write", path=test_filename, content="Hello from FileOperations tool!")
    print(f"写入操作: {write_result}")
    
    # 读取
    read_result = file_ops._run("read", path=test_filename)
    print(f"读取操作: {read_result}")

    # 列出
    list_result = file_ops._run("list", path=".")
    print(f"列出 '.' 目录:\n{list_result}")

    # 删除
    delete_result = file_ops._run("delete", path=test_filename)
    print(f"删除操作: {delete_result}")

def test_system_info():
    """测试系统信息工具"""
    print("\n=== 测试系统信息工具 ===")
    sys_info = SystemInfo()
    result = sys_info._run()
    print(result)

def test_network_tool():
    """测试网络工具"""
    print("\n=== 测试网络工具 ===")
    net_tool = NetworkTool()
    url = "https://www.deepseek.com"
    result = net_tool._run(url=url)
    print(f"测试URL '{url}':\n{result}")

def main():
    """主测试函数"""
    print("智能体工具功能测试 (简化版)")
    print("=" * 50)
    
    tools = get_tools()
    print(f"发现 {len(tools)} 个可用工具:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")
    
    print("\n" + "=" * 50)
    
    # 逐个测试工具
    try:
        test_calculator()
        test_file_operations()
        test_system_info()
        
        # 网络测试
        print("\n--- 需要网络连接的测试 ---")
        test_web_search()
        test_network_tool()
        
    except Exception as e:
        print(f"\n!!!!!! 测试过程中出现严重错误: {e} !!!!!!!", file=sys.stderr)
    
    print("\n" + "=" * 50)
    print("所有测试完成！")

if __name__ == "__main__":
    main()
