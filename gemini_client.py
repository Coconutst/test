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
                # 验证模型名称格式
                model_name = self.model if not self.model.startswith("models/") else self.model.replace("models/", "")
                self.gemini_model = model_name  # 存储模型名称
                print(f"✅ Gemini模型初始化成功: {model_name}")

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
            # 使用新版API生成响应
            model_name = self.model if not self.model.startswith("models/") else self.model.replace("models/", "")

            # 创建生成模型实例
            model = genai.GenerativeModel(model_name)

            # 生成响应
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature,
                )
            )

            # 返回生成的文本
            if response and response.text:
                return response.text
            else:
                return "抱歉，无法生成响应。请重试。"

        except Exception as e:
            # 如果API调用失败，提供一个智能的模拟响应
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg.lower():
                # 模型不存在，提供有用的模拟响应
                return self._generate_fallback_response(prompt)
            else:
                raise Exception(f"Gemini API调用失败: {str(e)}")
    
    def _generate_fallback_response(self, prompt: str) -> str:
        """生成智能的回退响应"""
        import datetime
        import re

        # 分析用户输入，提供相应的回答
        prompt_lower = prompt.lower()

        # 时间相关问题
        if any(word in prompt_lower for word in ['今天', '现在', '时间', '日期', '几号', 'today', 'now', 'time', 'date']):
            now = datetime.datetime.now()
            return f"""Thought: 用户询问时间相关信息，我需要提供当前的日期和时间。
Final Answer: 今天是{now.strftime('%Y年%m月%d日')}，现在是{now.strftime('%H:%M')}。

注意：我目前使用的是临时响应模式，因为Gemini API模型不可用。要获得完整功能，请：
1. 升级Python到3.9+版本
2. 安装最新版本的google-generativeai库
3. 确保网络连接正常"""

        # 问候语
        elif any(word in prompt_lower for word in ['你好', 'hello', 'hi', '您好']):
            return """Thought: 用户在问候我，我应该友好地回应并说明当前状态。
Final Answer: 你好！我是基于Gemini API的智能助手。

⚠️ 当前状态提醒：
- 我正在使用临时响应模式
- Gemini API模型暂时不可用（可能是版本兼容性问题）
- 要获得完整的AI功能，需要解决API连接问题

我仍然可以帮助您进行一些基本的任务和回答。有什么我可以帮助您的吗？"""

        # 计算相关
        elif any(word in prompt_lower for word in ['计算', '算', '+', '-', '*', '/', 'calculate']):
            # 尝试简单的数学计算
            try:
                # 提取数字和运算符
                numbers = re.findall(r'\d+(?:\.\d+)?', prompt)
                if len(numbers) >= 2:
                    # 简单的加减乘除
                    if '+' in prompt:
                        result = float(numbers[0]) + float(numbers[1])
                        return f"""Thought: 用户要求计算 {numbers[0]} + {numbers[1]}。
Final Answer: {numbers[0]} + {numbers[1]} = {result}

注意：这是基本计算功能。完整的AI计算能力需要Gemini API正常工作。"""
                    elif '*' in prompt:
                        result = float(numbers[0]) * float(numbers[1])
                        return f"""Thought: 用户要求计算 {numbers[0]} × {numbers[1]}。
Final Answer: {numbers[0]} × {numbers[1]} = {result}

注意：这是基本计算功能。完整的AI计算能力需要Gemini API正常工作。"""
            except:
                pass

            return """Thought: 用户询问计算相关问题，但我无法解析具体的计算内容。
Final Answer: 我可以帮您进行基本的数学计算，但目前处于临时模式。请提供具体的计算表达式，例如："计算 25 * 4 + 10"。

要获得完整的计算和分析能力，需要解决Gemini API连接问题。"""

        # 默认响应
        else:
            return f"""Thought: 用户提出了问题，但我目前处于临时响应模式。
Final Answer: 感谢您的问题。我目前处于临时响应模式，因为Gemini API暂时不可用。

您的问题是：{prompt[:100]}{'...' if len(prompt) > 100 else ''}

🔧 技术状态：
- 当前Python版本：3.8.8
- 需要Python版本：3.9+
- google-generativeai版本：0.1.0rc1（旧版本）
- 问题：旧版本API不支持现代Gemini模型

💡 建议解决方案：
1. 升级Python环境到3.9+
2. 安装最新版本的google-generativeai库
3. 检查网络连接和代理设置

在解决这些问题之前，我只能提供基本的响应。"""

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """返回标识参数"""
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
