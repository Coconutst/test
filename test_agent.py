#!/usr/bin/env python3
"""
智能体功能测试脚本
"""
import sys
import os

def test_agent_basic():
    """测试智能体基本功能"""
    try:
        from agent import DeepSeekAgent
        print("✅ 智能体模块导入成功")

        # 创建智能体实例
        agent = DeepSeekAgent()
        print("✅ 智能体初始化成功")

        # 测试简单对话
        print("\n=== 测试简单对话 ===")
        response = agent.chat("你好，请简单介绍一下你自己")
        print(f"智能体回复: {response}")

        # 测试工具调用 - 计算
        print("\n=== 测试计算工具 ===")
        response = agent.chat("请帮我计算 25 * 4 + 10")
        print(f"智能体回复: {response}")

        # 测试记忆功能
        print("\n=== 测试记忆功能 ===")
        response = agent.chat("我的名字是张三")
        print(f"智能体回复: {response}")

        response = agent.chat("你还记得我的名字吗？")
        print(f"智能体回复: {response}")

        print("\n✅ 所有测试完成！")
        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("智能体功能测试")
    print("=" * 50)
    success = test_agent_basic()
    if success:
        print("🎉 智能体测试全部通过！")
    else:
        print("⚠️ 智能体测试出现问题")
