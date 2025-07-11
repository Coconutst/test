import math
import os
import json
import hashlib
import base64
import datetime
import platform
import subprocess
from typing import Any, Optional
from pathlib import Path

import requests
import psutil
import pandas as pd
import qrcode
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    """计算器工具输入"""
    expression: str = Field(description="要计算的数学表达式")


class Calculator(BaseTool):
    """计算器工具"""
    name = "calculator"
    description = "用于执行数学计算。输入应该是一个数学表达式。"
    args_schema = CalculatorInput
    
    def _run(self, expression: str) -> str:
        """执行计算"""
        try:
            # 安全的数学表达式求值
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({"abs": abs, "round": round})
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return str(result)
        except Exception as e:
            return f"计算错误: {str(e)}"


class SearchInput(BaseModel):
    """搜索工具输入"""
    query: str = Field(description="搜索查询")


class WebSearch(BaseTool):
    """真实网络搜索工具"""
    name = "web_search"
    description = "用于搜索网络信息。输入应该是搜索查询。"
    args_schema = SearchInput

    def _run(self, query: str) -> str:
        """执行真实搜索"""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))

            if not results:
                return "未找到相关搜索结果"

            formatted_results = []
            for i, result in enumerate(results, 1):
                formatted_results.append(
                    f"{i}. {result['title']}\n"
                    f"   链接: {result['href']}\n"
                    f"   摘要: {result['body']}\n"
                )

            return "搜索结果:\n" + "\n".join(formatted_results)

        except Exception as e:
            return f"搜索失败: {str(e)}"


class TextAnalysisInput(BaseModel):
    """文本分析工具输入"""
    text: str = Field(description="要分析的文本")


class TextAnalysis(BaseTool):
    """文本分析工具"""
    name = "text_analysis"
    description = "用于分析文本，包括字数统计、情感分析等。"
    args_schema = TextAnalysisInput
    
    def _run(self, text: str) -> str:
        """执行文本分析"""
        word_count = len(text.split())
        char_count = len(text)
        
        # 简单的情感分析（基于关键词）
        positive_words = ["好", "棒", "优秀", "喜欢", "满意", "高兴"]
        negative_words = ["坏", "差", "糟糕", "讨厌", "不满", "难过"]
        
        positive_score = sum(1 for word in positive_words if word in text)
        negative_score = sum(1 for word in negative_words if word in text)
        
        if positive_score > negative_score:
            sentiment = "积极"
        elif negative_score > positive_score:
            sentiment = "消极"
        else:
            sentiment = "中性"
        
        return f"""文本分析结果：
- 字数：{word_count}
- 字符数：{char_count}
- 情感倾向：{sentiment}
- 积极词汇数：{positive_score}
- 消极词汇数：{negative_score}"""


# 网页内容获取工具
class WebPageInput(BaseModel):
    """网页内容获取工具输入"""
    url: str = Field(description="要获取内容的网页URL")


class WebPageFetcher(BaseTool):
    """网页内容获取工具"""
    name = "web_page_fetcher"
    description = "获取指定网页的文本内容。输入应该是一个有效的URL。"
    args_schema = WebPageInput

    def _run(self, url: str) -> str:
        """获取网页内容"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # 移除脚本和样式元素
            for script in soup(["script", "style"]):
                script.decompose()

            # 获取文本内容
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            # 限制长度
            if len(text) > 2000:
                text = text[:2000] + "..."

            return f"网页内容 ({url}):\n{text}"

        except Exception as e:
            return f"获取网页内容失败: {str(e)}"


# 文件操作工具
class FileInput(BaseModel):
    """文件操作工具输入"""
    file_path: str = Field(description="文件路径")
    content: Optional[str] = Field(default=None, description="要写入的内容（仅写入时需要）")


class FileOperations(BaseTool):
    """文件操作工具"""
    name = "file_operations"
    description = "读取或写入文件。格式：'read:文件路径' 或 'write:文件路径:内容'"

    def _run(self, operation: str) -> str:
        """执行文件操作"""
        try:
            parts = operation.split(':', 2)
            if len(parts) < 2:
                return "操作格式错误。使用 'read:文件路径' 或 'write:文件路径:内容'"

            action = parts[0].lower()
            file_path = parts[1]

            if action == "read":
                if not os.path.exists(file_path):
                    return f"文件不存在: {file_path}"

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if len(content) > 1000:
                    content = content[:1000] + "..."

                return f"文件内容 ({file_path}):\n{content}"

            elif action == "write":
                if len(parts) < 3:
                    return "写入操作需要内容。格式：'write:文件路径:内容'"

                content = parts[2]
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                return f"成功写入文件: {file_path}"

            else:
                return f"不支持的操作: {action}。支持的操作：read, write"

        except Exception as e:
            return f"文件操作失败: {str(e)}"


# 系统信息工具
class SystemInfo(BaseTool):
    """系统信息获取工具"""
    name = "system_info"
    description = "获取系统信息，包括CPU、内存、磁盘使用情况等。"

    def _run(self, info_type: str = "all") -> str:
        """获取系统信息"""
        try:
            info = []

            # 基本系统信息
            info.append(f"操作系统: {platform.system()} {platform.release()}")
            info.append(f"处理器: {platform.processor()}")
            info.append(f"Python版本: {platform.python_version()}")

            # CPU信息
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            info.append(f"CPU使用率: {cpu_percent}%")
            info.append(f"CPU核心数: {cpu_count}")

            # 内存信息
            memory = psutil.virtual_memory()
            info.append(f"内存使用率: {memory.percent}%")
            info.append(f"总内存: {memory.total // (1024**3)} GB")
            info.append(f"可用内存: {memory.available // (1024**3)} GB")

            # 磁盘信息
            disk = psutil.disk_usage('/')
            info.append(f"磁盘使用率: {disk.percent}%")
            info.append(f"总磁盘空间: {disk.total // (1024**3)} GB")
            info.append(f"可用磁盘空间: {disk.free // (1024**3)} GB")

            return "系统信息:\n" + "\n".join(info)

        except Exception as e:
            return f"获取系统信息失败: {str(e)}"


# 时间日期工具
class DateTimeInput(BaseModel):
    """时间日期工具输入"""
    operation: str = Field(description="操作类型：now, format, calculate")
    format_str: Optional[str] = Field(default=None, description="时间格式字符串")
    date_str: Optional[str] = Field(default=None, description="日期字符串")


class DateTimeTool(BaseTool):
    """时间日期工具"""
    name = "datetime_tool"
    description = "处理时间日期相关操作。支持：now（当前时间）、format（格式化时间）、calculate（时间计算）"
    args_schema = DateTimeInput

    def _run(self, operation: str, format_str: str = None, date_str: str = None) -> str:
        """执行时间日期操作"""
        try:
            if operation == "now":
                now = datetime.datetime.now()
                if format_str:
                    return now.strftime(format_str)
                else:
                    return f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}"

            elif operation == "format":
                if not date_str or not format_str:
                    return "格式化操作需要日期字符串和格式字符串"

                # 尝试解析日期
                dt = datetime.datetime.fromisoformat(date_str.replace('/', '-'))
                return dt.strftime(format_str)

            elif operation == "calculate":
                return "时间计算功能待实现"

            else:
                return f"不支持的操作: {operation}"

        except Exception as e:
            return f"时间日期操作失败: {str(e)}"


# 二维码生成工具
class QRCodeInput(BaseModel):
    """二维码生成工具输入"""
    text: str = Field(description="要生成二维码的文本")
    file_path: Optional[str] = Field(default="qrcode.png", description="保存路径")


class QRCodeGenerator(BaseTool):
    """二维码生成工具"""
    name = "qr_code_generator"
    description = "生成二维码图片。输入文本内容和可选的保存路径。"
    args_schema = QRCodeInput

    def _run(self, text: str, file_path: str = "qrcode.png") -> str:
        """生成二维码"""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img.save(file_path)

            return f"二维码已生成并保存到: {file_path}"

        except Exception as e:
            return f"二维码生成失败: {str(e)}"


# 哈希计算工具
class HashInput(BaseModel):
    """哈希计算工具输入"""
    text: str = Field(description="要计算哈希的文本")
    algorithm: str = Field(default="md5", description="哈希算法：md5, sha1, sha256")


class HashCalculator(BaseTool):
    """哈希计算工具"""
    name = "hash_calculator"
    description = "计算文本的哈希值。支持MD5、SHA1、SHA256算法。"
    args_schema = HashInput

    def _run(self, text: str, algorithm: str = "md5") -> str:
        """计算哈希值"""
        try:
            text_bytes = text.encode('utf-8')

            if algorithm.lower() == "md5":
                hash_obj = hashlib.md5(text_bytes)
            elif algorithm.lower() == "sha1":
                hash_obj = hashlib.sha1(text_bytes)
            elif algorithm.lower() == "sha256":
                hash_obj = hashlib.sha256(text_bytes)
            else:
                return f"不支持的哈希算法: {algorithm}"

            return f"{algorithm.upper()}哈希值: {hash_obj.hexdigest()}"

        except Exception as e:
            return f"哈希计算失败: {str(e)}"


def get_tools():
    """获取所有可用工具"""
    return [
        Calculator(),
        WebSearch(),
        TextAnalysis(),
        WebPageFetcher(),
        FileOperations(),
        SystemInfo(),
        DateTimeTool(),
        QRCodeGenerator(),
        HashCalculator()
    ]
