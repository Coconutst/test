#!/usr/bin/env python3
"""
自动代理设置工具
"""

import os
import sys
import subprocess

def detect_system_proxy():
    """检测系统代理设置"""
    print("🔍 检测系统代理设置...")
    
    if sys.platform == "win32":
        return detect_windows_proxy()
    elif sys.platform == "darwin":
        return detect_mac_proxy()
    else:
        return detect_linux_proxy()

def detect_windows_proxy():
    """检测Windows代理"""
    try:
        import winreg
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
        
        proxy_enable = winreg.QueryValueEx(key, "ProxyEnable")[0]
        if proxy_enable:
            proxy_server = winreg.QueryValueEx(key, "ProxyServer")[0]
            print(f"✅ 检测到Windows系统代理: {proxy_server}")
            return f"http://{proxy_server}"
    except Exception as e:
        print(f"⚠️ 无法读取Windows代理设置: {e}")
    return None

def detect_mac_proxy():
    """检测Mac代理"""
    try:
        result = subprocess.run(['scutil', '--proxy'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if 'HTTPProxy' in line and ':' in line:
                    proxy = line.split(':')[1].strip()
                    print(f"✅ 检测到Mac系统代理: {proxy}")
                    return f"http://{proxy}"
    except Exception as e:
        print(f"⚠️ 无法读取Mac代理设置: {e}")
    return None

def detect_linux_proxy():
    """检测Linux代理"""
    proxy_vars = ['HTTP_PROXY', 'http_proxy', 'HTTPS_PROXY', 'https_proxy']
    for var in proxy_vars:
        proxy = os.getenv(var)
        if proxy:
            print(f"✅ 检测到Linux环境代理: {proxy}")
            return proxy
    return None

def create_env_file(proxy_url=None):
    """创建或更新.env文件"""
    print("\n📝 配置.env文件...")
    
    env_content = []
    
    # 读取现有.env文件
    if os.path.exists('.env'):
        with open('.env', 'r', encoding='utf-8') as f:
            env_content = f.readlines()
    
    # 检查是否已有代理配置
    has_http_proxy = any('HTTP_PROXY=' in line for line in env_content)
    has_https_proxy = any('HTTPS_PROXY=' in line for line in env_content)
    
    # 添加代理配置
    if proxy_url and not has_http_proxy:
        env_content.append(f'\n# 网络代理配置\n')
        env_content.append(f'HTTP_PROXY={proxy_url}\n')
    
    if proxy_url and not has_https_proxy:
        env_content.append(f'HTTPS_PROXY={proxy_url}\n')
    
    # 写入.env文件
    with open('.env', 'w', encoding='utf-8') as f:
        f.writelines(env_content)
    
    print("✅ .env文件已更新")

def manual_proxy_setup():
    """手动代理设置"""
    print("\n🔧 手动代理设置")
    print("请输入代理信息（直接回车跳过）:")
    
    proxy_host = input("代理服务器地址: ").strip()
    if not proxy_host:
        return None
    
    proxy_port = input("代理端口 (默认8080): ").strip() or "8080"
    
    username = input("用户名 (如果需要认证): ").strip()
    password = input("密码 (如果需要认证): ").strip()
    
    if username and password:
        proxy_url = f"http://{username}:{password}@{proxy_host}:{proxy_port}"
    else:
        proxy_url = f"http://{proxy_host}:{proxy_port}"
    
    return proxy_url

def test_proxy_connection(proxy_url):
    """测试代理连接"""
    print(f"\n🧪 测试代理连接: {proxy_url}")
    
    try:
        import requests
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        
        response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
        if response.status_code == 200:
            print("✅ 代理连接测试成功!")
            print(f"IP信息: {response.json()}")
            return True
        else:
            print(f"❌ 代理连接测试失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 代理连接测试失败: {e}")
        return False

def setup_environment_variables(proxy_url):
    """设置环境变量"""
    print(f"\n🌐 设置环境变量...")
    
    os.environ['HTTP_PROXY'] = proxy_url
    os.environ['HTTPS_PROXY'] = proxy_url
    
    print("✅ 环境变量已设置")
    print("注意: 这些设置只在当前会话中有效")

def main():
    """主函数"""
    print("🚀 代理自动配置工具")
    print("=" * 50)
    
    # 检测系统代理
    system_proxy = detect_system_proxy()
    
    proxy_url = None
    
    if system_proxy:
        use_system = input(f"\n是否使用检测到的系统代理? ({system_proxy}) [Y/n]: ").strip().lower()
        if use_system != 'n':
            proxy_url = system_proxy
    
    if not proxy_url:
        proxy_url = manual_proxy_setup()
    
    if proxy_url:
        # 测试代理连接
        if test_proxy_connection(proxy_url):
            # 更新.env文件
            create_env_file(proxy_url)
            
            # 设置环境变量
            setup_environment_variables(proxy_url)
            
            print("\n🎉 代理配置完成!")
            print("现在可以运行以下命令测试:")
            print("python test_proxy.py")
            print("python test_gemini_connection.py")
        else:
            print("\n❌ 代理配置失败，请检查代理设置")
    else:
        print("\n⚠️ 未配置代理")

if __name__ == "__main__":
    main()
