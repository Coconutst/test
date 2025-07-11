import math
import os
import json
import hashlib
import datetime
import platform
import subprocess
import urllib.parse
import urllib.request
import re
import socket
from typing import Any, Optional

import requests
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


# 计算器工具
class CalculatorInput(BaseModel):
    expression: str = Field(description="数学表达式")


class Calculator(BaseTool):
    """真实的计算器工具"""
    name = "calculator"
    description = "执行真实的数学计算，支持复杂数学函数"
    args_schema = CalculatorInput
    
    def _run(self, expression: str) -> str:
        try:
            # 安全的数学计算环境
            safe_dict = {
                "__builtins__": {},
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow, "divmod": divmod,
                "math": math, "pi": math.pi, "e": math.e,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
                "exp": math.exp, "floor": math.floor, "ceil": math.ceil
            }
            
            result = eval(expression, safe_dict)
            return f"计算结果: {result}"
        except Exception as e:
            return f"计算错误: {str(e)}"


# 真实的网络搜索工具
class SearchInput(BaseModel):
    query: str = Field(description="搜索关键词")


class WebSearch(BaseTool):
    """真实的网络搜索工具"""
    name = "web_search"
    description = "搜索互联网信息并返回真实结果"
    args_schema = SearchInput
    
    def _run(self, query: str) -> str:
        try:
            # 使用真实的搜索API
            encoded_query = urllib.parse.quote(query)
            
            # 尝试多个搜索源
            search_engines = [
                f"https://api.duckduckgo.com/?q={encoded_query}&format=json&no_html=1",
                f"https://www.bing.com/search?q={encoded_query}&format=rss"
            ]
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            for search_url in search_engines:
                try:
                    response = requests.get(search_url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        if 'duckduckgo' in search_url:
                            data = response.json()
                            if data.get('AbstractText'):
                                return f"搜索 '{query}' 的结果:\n{data['AbstractText']}\n来源: {data.get('AbstractSource', 'DuckDuckGo')}"
                        else:
                            # 简单解析HTML结果
                            content = response.text[:1000]
                            return f"搜索 '{query}' 完成\n找到相关信息，内容长度: {len(content)} 字符"
                except:
                    continue
            
            return f"搜索 '{query}' 完成，但由于网络限制无法获取详细结果"
            
        except Exception as e:
            return f"搜索失败: {str(e)}"


# 真实的文件操作工具
class FileInput(BaseModel):
    operation: str = Field(description="操作类型: read, write, list, delete")
    path: str = Field(description="文件路径")
    content: Optional[str] = Field(default=None, description="写入内容")


class FileOperations(BaseTool):
    """真实的文件操作工具"""
    name = "file_operations"
    description = "执行真实的文件操作：读取、写入、列出、删除文件"
    args_schema = FileInput
    
    def _run(self, operation: str, path: str, content: str = None) -> str:
        try:
            if operation == "read":
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    return f"文件 {path} 内容:\n{file_content[:500]}{'...' if len(file_content) > 500 else ''}"
                else:
                    return f"文件 {path} 不存在"
            
            elif operation == "write":
                if content is None:
                    return "写入操作需要提供内容"
                
                # 确保目录存在
                dir_path = os.path.dirname(path)
                if dir_path:  # 只有当路径包含目录时才创建
                    os.makedirs(dir_path, exist_ok=True)
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"成功写入文件 {path}，内容长度: {len(content)} 字符"
            
            elif operation == "list":
                if os.path.isdir(path):
                    files = os.listdir(path)
                    return f"目录 {path} 包含 {len(files)} 个项目:\n" + "\n".join(files[:20])
                else:
                    return f"{path} 不是有效目录"
            
            elif operation == "delete":
                if os.path.exists(path):
                    os.remove(path)
                    return f"成功删除文件 {path}"
                else:
                    return f"文件 {path} 不存在"
            
            else:
                return f"不支持的操作: {operation}"
                
        except Exception as e:
            return f"文件操作失败: {str(e)}"


# 真实的系统信息工具
class SystemInfo(BaseTool):
    """真实的系统信息工具"""
    name = "system_info"
    description = "获取真实的系统信息"
    
    def _run(self, info_type: str = "all") -> str:
        try:
            info = []
            
            # 基本系统信息
            info.append(f"操作系统: {platform.system()} {platform.release()}")
            info.append(f"计算机名: {platform.node()}")
            info.append(f"处理器架构: {platform.machine()}")
            info.append(f"处理器: {platform.processor()}")
            info.append(f"Python版本: {platform.python_version()}")
            
            # 网络信息
            try:
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                info.append(f"本机IP: {local_ip}")
            except:
                info.append("本机IP: 获取失败")
            
            # 磁盘信息
            try:
                if platform.system() == "Windows":
                    import shutil
                    total, used, free = shutil.disk_usage("C:")
                    info.append(f"C盘空间: 总计 {total//1024**3}GB, 已用 {used//1024**3}GB, 可用 {free//1024**3}GB")
            except:
                info.append("磁盘信息: 获取失败")
            
            # 环境变量
            info.append(f"用户目录: {os.path.expanduser('~')}")
            info.append(f"当前工作目录: {os.getcwd()}")
            
            return "系统信息:\n" + "\n".join(info)
            
        except Exception as e:
            return f"获取系统信息失败: {str(e)}"


# 真实的网络工具
class NetworkInput(BaseModel):
    url: str = Field(description="网址")
    method: str = Field(default="GET", description="HTTP方法")


class NetworkTool(BaseTool):
    """真实的网络工具"""
    name = "network_tool"
    description = "执行真实的网络请求和测试"
    args_schema = NetworkInput
    
    def _run(self, url: str, method: str = "GET") -> str:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method.upper() == "HEAD":
                response = requests.head(url, headers=headers, timeout=10)
            else:
                return f"不支持的HTTP方法: {method}"
            
            result = []
            result.append(f"URL: {url}")
            result.append(f"状态码: {response.status_code}")
            result.append(f"响应时间: {response.elapsed.total_seconds():.2f}秒")
            result.append(f"内容长度: {len(response.content)} 字节")
            result.append(f"内容类型: {response.headers.get('content-type', '未知')}")
            
            # 如果是HTML，提取标题
            if 'text/html' in response.headers.get('content-type', ''):
                title_match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
                if title_match:
                    result.append(f"页面标题: {title_match.group(1).strip()}")
            
            return "\n".join(result)
            
        except Exception as e:
            return f"网络请求失败: {str(e)}"


def get_tools():
    """获取所有真实工具"""
    return [
        Calculator(),
        WebSearch(),
        FileOperations(),
        SystemInfo(),
        NetworkTool()
    ]
