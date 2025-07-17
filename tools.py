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


# 使用EXA-AI的网络搜索工具
class SearchInput(BaseModel):
    query: str = Field(description="搜索关键词")
    num_results: Optional[int] = Field(default=5, description="返回结果数量")


class WebSearch(BaseTool):
    """基于EXA-AI的高级网络搜索工具"""
    name = "web_search"
    description = "使用EXA-AI进行高质量的互联网搜索，返回实时准确的结果"
    args_schema = SearchInput
    
    def _run(self, query: str, num_results: int = 5) -> str:
        try:
            # EXA-AI搜索配置
            exa_api_url = "https://api.exa.ai/search"

            # 从环境变量获取EXA API密钥，如果没有则使用内置搜索
            exa_api_key = os.getenv('EXA_API_KEY')

            if exa_api_key:
                # 使用EXA-AI API
                headers = {
                    'Authorization': f'Bearer {exa_api_key}',
                    'Content-Type': 'application/json'
                }

                payload = {
                    'query': query,
                    'num_results': min(num_results, 10),
                    'include_text': ['text']
                }

                try:
                    response = requests.post(exa_api_url,
                                           headers=headers,
                                           json=payload,
                                           timeout=15)

                    if response.status_code == 200:
                        data = response.json()
                        results = []

                        for i, result in enumerate(data.get('results', [])[:num_results], 1):
                            title = result.get('title', '无标题')
                            url = result.get('url', '')
                            text = result.get('text', '')[:200] + '...' if result.get('text') else '无内容摘要'

                            results.append(f"{i}. {title}\n   {url}\n   摘要: {text}\n")

                        if results:
                            return f"🔍 EXA-AI搜索 '{query}' 的结果:\n\n" + "\n".join(results)
                        else:
                            return f"EXA-AI搜索 '{query}' 没有找到相关结果"

                    elif response.status_code == 401:
                        return "EXA-AI API认证失败，请检查API密钥配置"
                    else:
                        print(f"EXA-AI API响应详情: {response.text}")  # 添加调试信息
                        return f"EXA-AI API调用失败，状态码: {response.status_code}"

                except requests.exceptions.RequestException as e:
                    # 如果EXA-AI调用失败，回退到备用搜索方式
                    return self._fallback_search(query)

            else:
                # 如果没有EXA API密钥，使用备用搜索方式
                return self._fallback_search(query)

        except Exception as e:
            return f"搜索过程中发生错误: {str(e)}"

    def _fallback_search(self, query: str) -> str:
        """备用搜索方法"""
        try:
            # 使用模拟的高质量搜索结果
            encoded_query = urllib.parse.quote(query)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # 尝试DuckDuckGo即时答案API
            try:
                search_url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json&no_html=1"
                response = requests.get(search_url, headers=headers, timeout=10)

                if response.status_code == 200:
                    data = response.json()

                    # 构建搜索结果
                    results = []

                    # 添加即时答案
                    if data.get('AbstractText'):
                        results.append(f"📊 即时答案: {data['AbstractText']}")
                        if data.get('AbstractSource'):
                            results.append(f"   来源: {data['AbstractSource']}")

                    # 添加相关话题
                    if data.get('RelatedTopics'):
                        results.append("\n🔗 相关话题:")
                        for i, topic in enumerate(data['RelatedTopics'][:3], 1):
                            if isinstance(topic, dict) and topic.get('Text'):
                                results.append(f"   {i}. {topic['Text'][:100]}...")

                    # 添加定义
                    if data.get('Definition'):
                        results.append(f"\n📖 定义: {data['Definition']}")

                    if results:
                        return f"🔍 搜索 '{query}' 的结果:\n\n" + "\n".join(results)

            except Exception:
                pass

            # 如果所有方法都失败，返回建议性回复
            return f"""🔍 搜索 '{query}' 完成

由于网络限制，无法获取实时搜索结果。建议您：
1. 访问权威搜索引擎（Google、Bing、DuckDuckGo）
2. 查看相关领域的官方网站或文档
3. 咨询专业数据库或学术资源

如需更准确的搜索功能，请配置EXA-AI API密钥。"""

        except Exception as e:
            return f"备用搜索失败: {str(e)}"


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
class SystemInfoInput(BaseModel):
    info_type: str = Field(default="all", description="信息类型: all(全部), date(日期), current_date(当前日期), current_datetime(当前日期时间), system(系统), network(网络), disk(磁盘)")


class SystemInfo(BaseTool):
    """真实的系统信息工具"""
    name = "system_info"
    description = "获取系统信息和当前日期时间。支持参数：date(获取今天日期)、current_date(获取今天日期)、current_datetime(获取当前日期时间)、all(获取所有系统信息)"
    args_schema = SystemInfoInput

    def _run(self, info_type: str = "all", **kwargs) -> str:
        try:
            # 处理可能的参数别名
            if 'query' in kwargs:
                info_type = kwargs['query']

            info = []

            # 当前日期时间信息
            if info_type in ["all", "date", "current_date", "current_datetime"]:
                now = datetime.datetime.now()
                weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]

                # 如果只要日期，直接返回
                if info_type in ["date", "current_date"]:
                    return f"今天是{now.strftime('%Y年%m月%d日')} {weekday}"

                # 如果要日期时间，返回完整信息
                if info_type == "current_datetime":
                    return f"当前日期时间: {now.strftime('%Y年%m月%d日 %H:%M:%S')} {weekday}"

                # 如果是all，添加到info列表
                info.append(f"当前日期: {now.strftime('%Y年%m月%d日')}")
                info.append(f"当前时间: {now.strftime('%H:%M:%S')}")
                info.append(f"星期: {weekday}")

            # 基本系统信息
            if info_type in ["all", "system"]:
                info.append(f"操作系统: {platform.system()} {platform.release()}")
                info.append(f"计算机名: {platform.node()}")
                info.append(f"处理器架构: {platform.machine()}")
                info.append(f"处理器: {platform.processor()}")
                info.append(f"Python版本: {platform.python_version()}")

            # 网络信息
            if info_type in ["all", "network"]:
                try:
                    hostname = socket.gethostname()
                    local_ip = socket.gethostbyname(hostname)
                    info.append(f"本机IP: {local_ip}")
                except:
                    info.append("本机IP: 获取失败")

            # 磁盘信息
            if info_type in ["all", "disk"]:
                try:
                    if platform.system() == "Windows":
                        import shutil
                        total, used, free = shutil.disk_usage("C:")
                        info.append(f"C盘空间: 总计 {total//1024**3}GB, 已用 {used//1024**3}GB, 可用 {free//1024**3}GB")
                except:
                    info.append("磁盘信息: 获取失败")

            # 环境变量
            if info_type in ["all"]:
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


# 获取当前时间工具
class DateTimeInput(BaseModel):
    format_type: Optional[str] = Field(default="full", description="时间格式类型: full(完整), date(仅日期), time(仅时间), timestamp(时间戳)")


class DateTimeTool(BaseTool):
    """获取当前时间和日期的工具"""
    name = "get_current_time"
    description = "获取当前的日期和时间，支持多种格式输出"
    args_schema = DateTimeInput

    def _run(self, format_type: str = "full", **kwargs) -> str:
        try:
            # 处理可能的参数别名
            if 'format' in kwargs:
                format_type = kwargs['format']

            now = datetime.datetime.now()

            if format_type == "full":
                # 完整的日期时间格式
                formatted_time = now.strftime("%Y年%m月%d日 %H:%M:%S")
                weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
                return f"当前时间: {formatted_time} {weekday}"

            elif format_type == "date":
                # 仅日期
                return f"当前日期: {now.strftime('%Y年%m月%d日')}"

            elif format_type == "time":
                # 仅时间
                return f"当前时间: {now.strftime('%H:%M:%S')}"

            elif format_type == "timestamp":
                # Unix时间戳
                timestamp = int(now.timestamp())
                return f"当前时间戳: {timestamp} (对应时间: {now.strftime('%Y-%m-%d %H:%M:%S')})"

            elif format_type == "iso":
                # ISO格式
                return f"当前时间(ISO格式): {now.isoformat()}"

            elif format_type in ["YYYY年MM月DD日", "YYYY-MM-DD"]:
                # 特定日期格式
                return f"{now.strftime('%Y-%m-%d')}"

            else:
                # 默认格式
                return f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}"

        except Exception as e:
            return f"获取时间失败: {str(e)}"


def get_tools():
    """获取所有真实工具"""
    return [
        Calculator(),
        WebSearch(),
        FileOperations(),
        SystemInfo(),
        NetworkTool()
    ]
