#!/usr/bin/env python3
"""
网络搜索功能专项测试
"""

def test_web_search_detailed():
    """详细测试网络搜索功能"""
    try:
        from agent import DeepSeekAgent

        print("=== DeepSeek智能体网络搜索测试 ===")
        agent = DeepSeekAgent()

        # 测试1: 搜索技术相关信息
        print("\n📍 测试1: 搜索Python编程信息")
        response = agent.chat("请搜索Python编程语言的最新特性和发展趋势")
        print(f"智能体回复: {response}")

        # 测试2: 搜索实时新闻
        print("\n📍 测试2: 搜索AI技术新闻")
        response = agent.chat("搜索最近关于人工智能技术发展的新闻")
        print(f"智能体回复: {response}")

        # 测试3: 搜索特定公司信息
        print("\n📍 测试3: 搜索DeepSeek公司信息")
        response = agent.chat("请搜索DeepSeek公司的背景和主要产品")
        print(f"智能体回复: {response}")

        # 测试4: 搜索学术资料
        print("\n📍 测试4: 搜索机器学习相关资料")
        response = agent.chat("搜索关于大语言模型训练方法的学术资料")
        print(f"智能体回复: {response}")

        print("\n✅ 网络搜索功能测试完成！")

    except Exception as e:
        print(f"❌ 网络搜索测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_web_search_detailed()
