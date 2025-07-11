import math
import requests
from typing import Any
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
    """网络搜索工具（模拟）"""
    name = "web_search"
    description = "用于搜索网络信息。输入应该是搜索查询。"
    args_schema = SearchInput
    
    def _run(self, query: str) -> str:
        """执行搜索（这里是模拟实现）"""
        # 实际项目中可以集成真实的搜索API
        return f"搜索结果：关于'{query}'的信息（这是模拟结果）"


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


def get_tools():
    """获取所有可用工具"""
    return [
        Calculator(),
        WebSearch(),
        TextAnalysis()
    ]
