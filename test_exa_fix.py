#!/usr/bin/env python3
"""
测试EXA-AI API修复
"""

import os
from tools import WebSearch

def test_exa_api_fix():
    """测试修复后的EXA-AI API"""
    print("=== 测试EXA-AI API修复 ===")

    # 检查环境变量
    exa_key = os.getenv('EXA_API_KEY')
    if not exa_key:
        print("❌ 未找到EXA_API_KEY环境变量")
        print("请在.env文件中设置: EXA_API_KEY=你的API密钥")
        return False

    print(f"✅ 找到EXA API密钥: {exa_key[:10]}...")

    # 测试搜索功能
    search_tool = WebSearch()

    test_queries = [
        "Python编程",
        "人工智能发展",
        "机器学习算法"
    ]

    for query in test_queries:
        print(f"\n🔍 测试搜索: {query}")
        try:
            result = search_tool._run(query, num_results=3)
            if "EXA-AI API调用失败，状态码: 400" in result:
                print("❌ 仍然出现400错误")
                print(f"结果: {result}")
                return False
            elif "EXA-AI搜索" in result:
                print("✅ EXA-AI搜索成功")
                print(f"结果长度: {len(result)} 字符")
            else:
                print("⚠️ 使用了备用搜索方式")
                print(f"结果: {result[:200]}...")
        except Exception as e:
            print(f"❌ 搜索出错: {e}")
            return False

    print("\n✅ EXA-AI API修复测试完成")
    return True

if __name__ == "__main__":
    test_exa_api_fix()
