#!/usr/bin/env python3
"""
检查可用的Gemini模型
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

try:
    import google.generativeai as genai
    
    # 配置API
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    print("🔍 检查可用的Gemini模型...")
    print("=" * 50)
    
    # 列出所有可用模型
    try:
        models = genai.list_models()
        print("✅ 可用模型列表:")
        for model in models:
            print(f"  - {model.name}")
            print(f"    描述: {model.display_name}")
            print(f"    支持的方法: {model.supported_generation_methods}")
            print()
    except Exception as e:
        print(f"❌ 获取模型列表失败: {e}")
        
    # 尝试一些常见的模型名称
    test_models = [
        "models/text-bison-001",
        "models/chat-bison-001", 
        "models/gemini-pro",
        "models/gemini-1.5-pro",
        "models/gemini-1.5-flash"
    ]
    
    print("\n🧪 测试常见模型...")
    print("=" * 50)
    
    for model_name in test_models:
        try:
            print(f"测试模型: {model_name}")
            response = genai.generate_text(
                model=model_name,
                prompt="Hello",
                max_output_tokens=10,
                temperature=0.1
            )
            
            if response and response.result:
                print(f"✅ {model_name} 可用")
                print(f"   响应: {response.result[:50]}...")
            else:
                print(f"⚠️ {model_name} 无响应")
                
        except Exception as e:
            print(f"❌ {model_name} 失败: {str(e)[:100]}...")
        print()
        
except ImportError:
    print("❌ google.generativeai 库未安装")
except Exception as e:
    print(f"❌ 发生错误: {e}")
