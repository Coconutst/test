#!/usr/bin/env python3
"""
代理配置测试工具
"""

import os
import sys
import requests
from config import Config

def test_basic_connectivity():
    """测试基本网络连接"""
    print("=== 基本网络连接测试 ===")
    test_urls = [
        "https://www.google.com",
        "https://generativelanguage.googleapis.com",
        "https://httpbin.org/ip"
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=10)
            print(f"✅ {url}: {response.status_code}")
        except Exception as e:
            print(f"❌ {url}: {str(e)[:100]}...")

def test_proxy_settings():
    """测试代理设置"""
    print("\n=== 代理设置检查 ===")
    
    # 检查环境变量
    http_proxy = os.getenv('HTTP_PROXY') or os.getenv('http_proxy')
    https_proxy = os.getenv('HTTPS_PROXY') or os.getenv('https_proxy')
    no_proxy = os.getenv('NO_PROXY') or os.getenv('no_proxy')
    
    print(f"HTTP_PROXY: {http_proxy or '未设置'}")
    print(f"HTTPS_PROXY: {https_proxy or '未设置'}")
    print(f"NO_PROXY: {no_proxy or '未设置'}")
    
    # 检查Config类设置
    print(f"\nConfig.HTTP_PROXY: {Config.HTTP_PROXY or '未设置'}")
    print(f"Config.HTTPS_PROXY: {Config.HTTPS_PROXY or '未设置'}")
    
    return http_proxy or https_proxy

def test_proxy_connectivity():
    """测试通过代理的连接"""
    print("\n=== 代理连接测试 ===")
    
    proxies = {}
    if Config.HTTP_PROXY:
        proxies['http'] = Config.HTTP_PROXY
    if Config.HTTPS_PROXY:
        proxies['https'] = Config.HTTPS_PROXY
    
    if not proxies:
        print("⚠️ 未配置代理，跳过代理测试")
        return False
    
    print(f"使用代理: {proxies}")
    
    test_urls = [
        "https://httpbin.org/ip",
        "https://www.google.com"
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, proxies=proxies, timeout=15)
            print(f"✅ 通过代理访问 {url}: {response.status_code}")
            if 'httpbin.org/ip' in url:
                print(f"   IP信息: {response.json()}")
        except Exception as e:
            print(f"❌ 代理访问 {url} 失败: {str(e)[:100]}...")
            return False
    
    return True

def test_gemini_with_proxy():
    """测试Gemini API通过代理的连接"""
    print("\n=== Gemini API代理测试 ===")
    
    try:
        import google.generativeai as genai
        
        # 设置代理
        Config.setup_proxy()
        
        # 配置API
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        # 尝试简单请求
        response = genai.generate_text(
            model="models/text-bison-001",
            prompt="Hello",
            max_output_tokens=10,
            temperature=0.1
        )
        
        if response and response.result:
            print("✅ Gemini API通过代理连接成功!")
            print(f"响应: {response.result}")
            return True
        else:
            print("❌ Gemini API无响应")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API测试失败: {str(e)[:200]}...")
        return False

def get_system_proxy_windows():
    """获取Windows系统代理设置"""
    try:
        import winreg
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
        
        proxy_enable = winreg.QueryValueEx(key, "ProxyEnable")[0]
        if proxy_enable:
            proxy_server = winreg.QueryValueEx(key, "ProxyServer")[0]
            return f"http://{proxy_server}"
    except:
        pass
    return None

def suggest_proxy_config():
    """建议代理配置"""
    print("\n=== 代理配置建议 ===")
    
    # 检查Windows系统代理
    if sys.platform == "win32":
        system_proxy = get_system_proxy_windows()
        if system_proxy:
            print(f"检测到系统代理: {system_proxy}")
            print("建议在.env文件中添加:")
            print(f"HTTP_PROXY={system_proxy}")
            print(f"HTTPS_PROXY={system_proxy}")
    
    print("\n常见代理配置示例:")
    print("# 公司代理")
    print("HTTP_PROXY=http://proxy.company.com:8080")
    print("HTTPS_PROXY=http://proxy.company.com:8080")
    print()
    print("# 带认证的代理")
    print("HTTP_PROXY=http://username:password@proxy.company.com:8080")
    print("HTTPS_PROXY=http://username:password@proxy.company.com:8080")
    print()
    print("# SOCKS代理")
    print("HTTP_PROXY=socks5://127.0.0.1:1080")
    print("HTTPS_PROXY=socks5://127.0.0.1:1080")

def main():
    """主测试函数"""
    print("🌐 代理配置测试工具")
    print("=" * 50)
    
    # 基本连接测试
    test_basic_connectivity()
    
    # 代理设置检查
    has_proxy = test_proxy_settings()
    
    if has_proxy:
        # 代理连接测试
        proxy_works = test_proxy_connectivity()
        
        if proxy_works:
            # Gemini API测试
            test_gemini_with_proxy()
        else:
            print("\n❌ 代理连接失败，请检查代理配置")
    else:
        print("\n⚠️ 未检测到代理配置")
        suggest_proxy_config()

if __name__ == "__main__":
    main()
