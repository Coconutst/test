#!/usr/bin/env python3
"""
Gemini智能体主程序
"""

import sys
from agent import GeminiAgent
from config import Config


def main():
    """主函数"""
    print("=== Gemini智能体 ===")
    print("输入 'quit' 或 'exit' 退出程序")
    print("输入 'reset' 重置对话历史")
    print("输入 'memory' 查看对话历史")
    print("-" * 50)

    try:
        # 创建智能体
        agent = GeminiAgent()
        print("智能体初始化成功！")
        
        # 交互循环
        while True:
            try:
                user_input = input("\n用户: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("再见！")
                    break
                
                if user_input.lower() in ['reset', '重置']:
                    agent.reset_memory()
                    print("对话历史已重置")
                    continue
                
                if user_input.lower() in ['memory', '历史']:
                    memory = agent.get_memory()
                    print(f"对话历史:\n{memory}")
                    continue
                
                # 获取智能体响应
                print("智能体: ", end="", flush=True)
                response = agent.chat(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n程序被用户中断")
                break
            except Exception as e:
                print(f"发生错误: {str(e)}")
                continue
    
    except Exception as e:
        print(f"初始化失败: {str(e)}")
        print("请检查配置和API密钥设置")
        sys.exit(1)


def demo():
    """演示函数"""
    print("=== Gemini智能体演示 ===")

    try:
        agent = GeminiAgent()
        
        # 演示对话
        demo_questions = [
            "你好，请介绍一下你自己",
            "计算 25 * 4 + 10",
            "分析这段文本的情感：'今天天气真好，我很开心！'",
            "搜索关于人工智能的信息"
        ]
        
        for question in demo_questions:
            print(f"\n用户: {question}")
            response = agent.chat(question)
            print(f"智能体: {response}")
            print("-" * 50)
    
    except Exception as e:
        print(f"演示失败: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        main()
