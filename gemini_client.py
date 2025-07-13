import os
from typing import List, Dict, Any, Optional
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from config import Config

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ 警告: google-generativeai 库未安装，使用模拟模式")
    print("请运行: pip install google-generativeai")


class GeminiLLM(LLM):
    """Gemini API的LangChain LLM包装器"""

    api_key: str = Config.GEMINI_API_KEY
    model: str = Config.DEFAULT_MODEL
    max_tokens: int = Config.MAX_TOKENS
    temperature: float = Config.TEMPERATURE
    gemini_model: Any = None
    generation_config: Any = None

    class Config:
        """允许任意类型的字段"""
        arbitrary_types_allowed = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if GEMINI_AVAILABLE:
            # 配置Gemini API
            genai.configure(api_key=self.api_key)

            # 创建生成配置
            self.generation_config = {
                'max_output_tokens': self.max_tokens,
                'temperature': self.temperature,
            }

            # 简化初始化，避免网络调用
            try:
                self.gemini_model = "initialized"  # 标记已初始化
                print(f"✅ Gemini模型初始化成功: {self.model}")

            except Exception as e:
                raise Exception(f"无法初始化Gemini模型: {str(e)}")
        else:
            # 模拟模式
            self.gemini_model = None
            print(f"🔧 模拟模式: 使用模型 {self.model}")
    
    @property
    def _llm_type(self) -> str:
        return "gemini"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """调用Gemini API"""
        if not GEMINI_AVAILABLE:
            # 模拟模式响应 - 符合ReAct格式
            if "你好" in prompt or "hello" in prompt.lower():
                return """Thought: 用户在问候我，我应该友好地回应。
Final Answer: 你好！我是基于Gemini API的智能体助手。目前正在模拟模式下运行，要使用真实的Gemini API，请安装google-generativeai库并配置API密钥。我可以帮助您进行计算、搜索、文件操作等任务。有什么我可以帮助您的吗？"""
            else:
                return f"""Thought: 我需要回答用户的问题，但目前在模拟模式下运行。
Final Answer: 抱歉，我目前在模拟模式下运行。要使用真实的Gemini API功能，请：
1. 安装依赖: pip install google-generativeai
2. 配置API密钥: GEMINI_API_KEY=your_key
3. 重启程序

您的问题是: {prompt[:100]}{'...' if len(prompt) > 100 else ''}
当前使用模型: {self.model}"""

        try:
            # 使用旧版API生成响应
            response = genai.generate_text(
                model=f"models/{self.model}",
                prompt=prompt,
                temperature=self.temperature,
                max_output_tokens=self.max_tokens
            )

            # 返回生成的文本
            if response.result:
                return response.result
            else:
                return "抱歉，无法生成响应。请重试。"

        except Exception as e:
            raise Exception(f"Gemini API调用失败: {str(e)}")
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """返回标识参数"""
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
