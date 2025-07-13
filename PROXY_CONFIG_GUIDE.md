# 🌐 网络代理配置指南

## 方法1: 环境变量配置（推荐）

### 在.env文件中添加代理配置
编辑`.env`文件，添加以下内容：

```bash
# Gemini API配置
GEMINI_API_KEY=your_gemini_api_key_here

# 代理配置
HTTP_PROXY=http://proxy_server:port
HTTPS_PROXY=http://proxy_server:port
# 如果需要认证
# HTTP_PROXY=http://username:password@proxy_server:port
# HTTPS_PROXY=http://username:password@proxy_server:port

# 不使用代理的地址（可选）
NO_PROXY=localhost,127.0.0.1,.local
```

### 常见代理配置示例
```bash
# 公司代理示例
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=http://proxy.company.com:8080

# 带认证的代理
HTTP_PROXY=http://user:pass@proxy.company.com:8080
HTTPS_PROXY=http://user:pass@proxy.company.com:8080

# Socks代理
HTTP_PROXY=socks5://127.0.0.1:1080
HTTPS_PROXY=socks5://127.0.0.1:1080
```

## 方法2: 系统环境变量

### Windows PowerShell
```powershell
# 设置代理
$env:HTTP_PROXY="http://proxy_server:port"
$env:HTTPS_PROXY="http://proxy_server:port"

# 验证设置
echo $env:HTTP_PROXY
echo $env:HTTPS_PROXY
```

### Windows CMD
```cmd
set HTTP_PROXY=http://proxy_server:port
set HTTPS_PROXY=http://proxy_server:port
```

### Linux/Mac
```bash
export HTTP_PROXY=http://proxy_server:port
export HTTPS_PROXY=http://proxy_server:port
```

## 方法3: 代码中配置

### 修改config.py支持代理
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Gemini API配置
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # 代理配置
    HTTP_PROXY = os.getenv("HTTP_PROXY", "")
    HTTPS_PROXY = os.getenv("HTTPS_PROXY", "")
    
    @classmethod
    def setup_proxy(cls):
        """设置代理"""
        if cls.HTTP_PROXY:
            os.environ['HTTP_PROXY'] = cls.HTTP_PROXY
        if cls.HTTPS_PROXY:
            os.environ['HTTPS_PROXY'] = cls.HTTPS_PROXY
```

## 方法4: 获取系统代理设置

### Windows系统代理检测
```python
import winreg

def get_windows_proxy():
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
        
        proxy_enable = winreg.QueryValueEx(key, "ProxyEnable")[0]
        if proxy_enable:
            proxy_server = winreg.QueryValueEx(key, "ProxyServer")[0]
            return f"http://{proxy_server}"
    except:
        pass
    return None
```

## 测试代理配置

创建测试脚本验证代理是否工作：
```python
import requests
import os

def test_proxy():
    proxies = {
        'http': os.getenv('HTTP_PROXY'),
        'https': os.getenv('HTTPS_PROXY')
    }
    
    try:
        response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
        print("代理测试成功:", response.json())
        return True
    except Exception as e:
        print("代理测试失败:", e)
        return False
```

## 常见问题解决

### 1. 代理认证问题
如果代理需要用户名密码：
```bash
HTTP_PROXY=http://username:password@proxy.server.com:8080
```

### 2. SOCKS代理支持
安装socks支持：
```bash
pip install requests[socks]
```

### 3. SSL证书问题
如果遇到SSL证书问题：
```python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

### 4. 代理自动检测
```python
import urllib.request

def get_system_proxy():
    proxy_handler = urllib.request.ProxyHandler()
    opener = urllib.request.build_opener(proxy_handler)
    return opener
```
