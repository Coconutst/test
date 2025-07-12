#!/usr/bin/env python3
"""
简化的EXA-AI API测试脚本
"""

import os
import requests

def test_exa_api_directly():
    """直接测试EXA-AI API"""
    print("=== 直接测试EXA-AI API修复 ===")

    # 检查环境变量
    exa_api_key = os.getenv('EXA_API_KEY')
    if not exa_api_key:
        print("❌ 未找到EXA_API_KEY环境变量")
        print("请设置环境变量: set EXA_API_KEY=你的API密钥")
        return False

    print(f"✅ 找到EXA API密钥: {exa_api_key[:10]}...")

    # EXA-AI API配置
    exa_api_url = "https://api.exa.ai/search"

    headers = {
        'Authorization': f'Bearer {exa_api_key}',
        'Content-Type': 'application/json'
    }

    # 修复后的正确参数格式
    payload = {
        'query': 'Python编程',
        'num_results': 3,
        'include_text': ['text']
    }

    print(f"\n🔍 测试API请求...")
    print(f"URL: {exa_api_url}")
    print(f"Payload: {payload}")

    try:
        response = requests.post(exa_api_url,
                               headers=headers,
                               json=payload,
                               timeout=15)

        print(f"\n📊 响应状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            print(f"✅ API调用成功！")
            print(f"📄 返回结果数量: {len(results)}")

            for i, result in enumerate(results[:2], 1):
                title = result.get('title', '无标题')
                url = result.get('url', '')
                print(f"{i}. {title}")
                print(f"   {url}")

            return True

        elif response.status_code == 400:
            print("❌ 仍然出现400错误")
            print(f"响应内容: {response.text}")
            return False

        elif response.status_code == 401:
            print("❌ API认证失败，请检查API密钥")
            return False

        else:
            print(f"❌ API调用失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {e}")
        return False

def show_fix_summary():
    """显示修复总结"""
    print("\n" + "="*50)
    print("🔧 EXA-AI API修复总结")
    print("="*50)
    print("修复的问题:")
    print("1. 参数名称错误:")
    print("   - 'numResults' → 'num_results' ✅")
    print("   - 'includeText' → 'include_text' ✅")
    print("2. 删除了不支持的参数:")
    print("   - 移除了 'type': 'neural' ✅")
    print("3. 添加了调试信息输出 ✅")
    print("\n如果仍有问题，请检查:")
    print("- EXA_API_KEY环境变量是否正确设置")
    print("- API密钥是否有效且有足够额度")
    print("- 网络连接是否正常")

if __name__ == "__main__":
    success = test_exa_api_directly()
    show_fix_summary()

    if success:
        print("\n🎉 EXA-AI API修复成功！")
    else:
        print("\n⚠️ 请检查上述问题并重试")
