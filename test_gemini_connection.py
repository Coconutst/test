#!/usr/bin/env python3
"""
测试Gemini API连接
"""

import os
import sys
from config import Config

def test_api_key():
    """测试API密钥配置"""
    print("=== API密钥测试 ===")
    if Config.GEMINI_API_KEY:
        print(f"✅ API密钥已配置: {Config.GEMINI_API_KEY[:10]}...")
        return True
    else:
        print("❌ API密钥未配置")
        return False

def test_import():
    """测试库导入"""
    print("\n=== 库导入测试 ===")
    try:
        import google.generativeai as genai
        print("✅ google.generativeai 导入成功")
        print(f"可用方法: {[attr for attr in dir(genai) if not attr.startswith('_')]}")
        return True, genai
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False, None

def test_configuration(genai):
    """测试API配置"""
    print("\n=== API配置测试 ===")
    try:
        genai.configure(api_key=Config.GEMINI_API_KEY)
        print("✅ API配置成功")
        return True
    except Exception as e:
        print(f"❌ API配置失败: {e}")
        return False

def test_simple_request(genai):
    """测试简单请求"""
    print("\n=== 简单请求测试 ===")
    try:
        # 尝试不同的模型
        models_to_try = [
            "models/text-bison-001",
            "models/gemini-pro",
            "models/gemini-2.5-flash",
            "models/gemini-2.5-pro",
            "models/gemini-1.5-flash",
            "models/gemini-1.5-pro"
        ]

        for model in models_to_try:
            try:
                print(f"尝试模型: {model}")

                # 使用旧版API方式
                response = genai.generate_text(
                    model=model,
                    prompt="Hello, how are you?",
                    max_output_tokens=50,
                    temperature=0.7
                )

                if response and response.result:
                    print(f"✅ 模型 {model} 响应成功")
                    print(f"响应内容: {response.result[:100]}...")
                    return True, model
                else:
                    print(f"⚠️ 模型 {model} 无响应")

            except Exception as e:
                print(f"❌ 模型 {model} 失败: {str(e)[:100]}...")
                continue

        print("❌ 所有模型都失败了")
        return False, None

    except Exception as e:
        print(f"❌ 请求测试失败: {e}")
        return False, None

def main():
    """主测试函数"""
    print("🧪 Gemini API 连接测试")
    print("=" * 50)
    
    # 测试API密钥
    if not test_api_key():
        print("\n请配置GEMINI_API_KEY环境变量")
        return
    
    # 测试导入
    success, genai = test_import()
    if not success:
        print("\n请安装: pip install google-generativeai")
        return
    
    # 测试配置
    if not test_configuration(genai):
        print("\n请检查API密钥是否正确")
        return
    
    # 测试请求
    success, working_model = test_simple_request(genai)
    if success:
        print(f"\n🎉 测试成功！可用模型: {working_model}")
        print("\n建议更新config.py中的DEFAULT_MODEL为:", working_model)
    else:
        print("\n❌ 网络请求失败，可能的原因:")
        print("1. 网络连接问题")
        print("2. API密钥无效")
        print("3. 模型不可用")
        print("4. 防火墙或代理设置")

if __name__ == "__main__":
    main()
