#!/usr/bin/env python3
"""
测试智能体工具功能
"""

from tools import get_tools


def test_calculator():
    """测试计算器工具"""
    print("=== 测试计算器工具 ===")
    from tools import Calculator
    
    calc = Calculator()
    test_cases = [
        "2 + 3 * 4",
        "sqrt(16)",
        "sin(pi/2)",
        "log(10)",
        "2**8"
    ]
    
    for expression in test_cases:
        result = calc._run(expression)
        print(f"{expression} = {result}")


def test_web_search():
    """测试网络搜索工具"""
    print("\n=== 测试网络搜索工具 ===")
    from tools import WebSearch
    
    search = WebSearch()
    query = "Python编程语言"
    result = search._run(query)
    print(f"搜索 '{query}':")
    print(result[:500] + "..." if len(result) > 500 else result)


def test_system_info():
    """测试系统信息工具"""
    print("\n=== 测试系统信息工具 ===")
    from tools import SystemInfo
    
    sys_info = SystemInfo()
    result = sys_info._run()
    print(result)


def test_datetime_tool():
    """测试时间日期工具"""
    print("\n=== 测试时间日期工具 ===")
    from tools import DateTimeTool
    
    dt_tool = DateTimeTool()
    
    # 测试当前时间
    result = dt_tool._run("now")
    print(f"当前时间: {result}")
    
    # 测试格式化时间
    result = dt_tool._run("now", format_str="%Y年%m月%d日 %H:%M:%S")
    print(f"格式化时间: {result}")


def test_hash_calculator():
    """测试哈希计算工具"""
    print("\n=== 测试哈希计算工具 ===")
    from tools import HashCalculator
    
    hash_calc = HashCalculator()
    text = "Hello, World!"
    
    for algorithm in ["md5", "sha1", "sha256"]:
        result = hash_calc._run(text, algorithm)
        print(f"{algorithm}: {result}")


def test_qr_code():
    """测试二维码生成工具"""
    print("\n=== 测试二维码生成工具 ===")
    from tools import QRCodeGenerator
    
    qr_gen = QRCodeGenerator()
    text = "https://www.python.org"
    result = qr_gen._run(text, "test_qr.png")
    print(result)


def test_file_operations():
    """测试文件操作工具"""
    print("\n=== 测试文件操作工具 ===")
    from tools import FileOperations
    
    file_ops = FileOperations()
    
    # 测试写入文件
    write_result = file_ops._run("write:test_file.txt:这是一个测试文件内容")
    print(f"写入结果: {write_result}")
    
    # 测试读取文件
    read_result = file_ops._run("read:test_file.txt")
    print(f"读取结果: {read_result}")


def test_web_page_fetcher():
    """测试网页内容获取工具"""
    print("\n=== 测试网页内容获取工具 ===")
    from tools import WebPageFetcher
    
    fetcher = WebPageFetcher()
    url = "https://httpbin.org/html"
    result = fetcher._run(url)
    print(f"网页内容: {result[:300]}...")


def main():
    """主测试函数"""
    print("智能体工具功能测试")
    print("=" * 50)
    
    # 显示所有可用工具
    tools = get_tools()
    print(f"可用工具数量: {len(tools)}")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")
    
    print("\n" + "=" * 50)
    
    # 测试各个工具
    try:
        test_calculator()
        test_system_info()
        test_datetime_tool()
        test_hash_calculator()
        test_qr_code()
        test_file_operations()
        
        # 需要网络连接的测试
        print("\n--- 需要网络连接的测试 ---")
        test_web_search()
        test_web_page_fetcher()
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成！")


if __name__ == "__main__":
    main()
