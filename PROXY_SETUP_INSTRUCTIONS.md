# 🌐 代理配置快速指南

## 🚀 快速开始

### 方法1: 自动配置（推荐）
```bash
# 激活虚拟环境
deepseek_agent_env\Scripts\activate

# 运行自动代理配置工具
python setup_proxy.py
```

### 方法2: 手动配置
编辑 `.env` 文件，添加代理配置：
```bash
# 基本代理配置
HTTP_PROXY=http://proxy_server:port
HTTPS_PROXY=http://proxy_server:port

# 带认证的代理
HTTP_PROXY=http://username:password@proxy_server:port
HTTPS_PROXY=http://username:password@proxy_server:port
```

## 🧪 测试配置

### 1. 测试代理连接
```bash
python test_proxy.py
```

### 2. 测试Gemini API连接
```bash
python test_gemini_connection.py
```

### 3. 运行智能体
```bash
python main.py
```

## 📋 常见代理配置示例

### 公司代理
```bash
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=http://proxy.company.com:8080
```

### 带认证的公司代理
```bash
HTTP_PROXY=http://myuser:mypass@proxy.company.com:8080
HTTPS_PROXY=http://myuser:mypass@proxy.company.com:8080
```

### SOCKS代理（需要安装 requests[socks]）
```bash
HTTP_PROXY=socks5://127.0.0.1:1080
HTTPS_PROXY=socks5://127.0.0.1:1080
```

### 本地代理工具
```bash
# Clash
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890

# V2Ray
HTTP_PROXY=http://127.0.0.1:10809
HTTPS_PROXY=http://127.0.0.1:10809

# Shadowsocks
HTTP_PROXY=http://127.0.0.1:1087
HTTPS_PROXY=http://127.0.0.1:1087
```

## 🔧 故障排除

### 问题1: 代理认证失败
**解决方案**: 确保用户名和密码正确，特殊字符需要URL编码
```bash
# 如果密码包含特殊字符，需要编码
# 例如: password@123 -> password%40123
HTTP_PROXY=http://user:password%40123@proxy:8080
```

### 问题2: SSL证书错误
**解决方案**: 在代码中添加SSL验证跳过
```python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

### 问题3: 连接超时
**解决方案**: 增加超时时间或检查代理服务器状态
```python
import requests
requests.get(url, proxies=proxies, timeout=30)
```

### 问题4: 代理不支持HTTPS
**解决方案**: 使用HTTP代理访问HTTPS
```bash
HTTP_PROXY=http://proxy:8080
HTTPS_PROXY=http://proxy:8080  # 注意这里也是http://
```

## 📱 移动网络/热点配置

如果使用手机热点：
```bash
# 通常不需要代理
# HTTP_PROXY=
# HTTPS_PROXY=
```

## 🏢 企业网络配置

联系IT部门获取：
- 代理服务器地址和端口
- 认证信息（如果需要）
- 是否需要PAC文件配置

## ✅ 验证配置成功

运行测试后，应该看到：
```
✅ 代理连接测试成功
✅ Gemini API通过代理连接成功
✅ 智能体初始化成功
```

## 🆘 获取帮助

如果仍然无法连接：
1. 检查防火墙设置
2. 确认代理服务器可用
3. 尝试不同的代理端口
4. 联系网络管理员
5. 考虑使用VPN
