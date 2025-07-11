import requests
import json
from typing import List, Dict, Any, Optional
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from config import Config


class DeepSeekLLM(LLM):
    """DeepSeek API的LangChain LLM包装器"""
    
    api_key: str = Config.DEEPSEEK_API_KEY
    base_url: str = Config.DEEPSEEK_BASE_URL
    model: str = Config.DEFAULT_MODEL
    max_tokens: int = Config.MAX_TOKENS
    temperature: float = Config.TEMPERATURE
    
    @property
    def _llm_type(self) -> str:
        return "deepseek"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """调用DeepSeek API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"DeepSeek API调用失败: {str(e)}")
        except KeyError as e:
            raise Exception(f"DeepSeek API响应格式错误: {str(e)}")
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """返回标识参数"""
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
