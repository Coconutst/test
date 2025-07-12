#!/usr/bin/env python3
"""
EXA-AI搜索功能测试脚本
"""

def test_exa_search():
    """测试EXA-AI搜索功能"""
    try:
        from agent import DeepSeekAgent

        print("=== EXA-AI智能搜索功能测试 ===")
        agent = DeepSeekAgent()

        # 测试1: 技术查询
        print("\n📍 测试1: 搜索最新AI技术发展")
        response = agent.chat("请搜索2024年人工智能领域的最新突破和发展趋势")
        print(f"智能体回复: {response}")

        # 测试2: 学术研究
        print("\n📍 测试2: 搜索机器学习论文")
        response = agent.chat("搜索关于Transformer架构优化的最新研究论文")
        print(f"智能体回复: {response}")

        # 测试3: 行业信息
        print("\n📍 测试3: 搜索科技公司信息")
        response = agent.chat("搜索OpenAI公司的最新产品和发展动态")
        print(f"智能体回复: {response}")

        # 测试4: 实时新闻
        print("\n📍 测试4: 搜索实时科技新闻")
        response = agent.chat("搜索最近一周关于ChatGPT和大语言模型的新闻")
        print(f"智能体回复: {response}")

        # 测试5: 专业知识
        print("\n📍 测试5: 搜索专业技术资料")
        response = agent.chat("搜索Python深度学习框架PyTorch的最新功能和教程")
        print(f"智能体回复: {response}")

        print("\n✅ EXA-AI搜索功能测试完成！")

    except Exception as e:
        print(f"❌ EXA-AI搜索测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_search_tool_directly():
    """直接测试搜索工具"""
    try:
        from tools import WebSearch

        print("\n=== 直接测试WebSearch工具 ===")
        search_tool = WebSearch()

        test_queries = [
            "人工智能最新发展",
            "Python编程教程",
            "DeepSeek AI公司",
            "机器学习算法"
        ]

        for query in test_queries:
            print(f"\n🔍 搜索: {query}")
            result = search_tool._run(query, num_results=3)
            print(f"结果: {result[:300]}...")

        print("\n✅ 搜索工具直接测试完成！")

    except Exception as e:
        print(f"❌ 搜索工具测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 开始测试升级后的EXA-AI搜索功能")
    print("=" * 60)

    # 先测试搜索工具本身
    test_search_tool_directly()

    # 再测试智能体集成
    test_exa_search()

    print("\n" + "=" * 60)
    print("🎉 所有测试完成！")
