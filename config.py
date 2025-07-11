import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置类"""
    
    # DeepSeek API配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
    
    # 模型配置
    DEFAULT_MODEL = "deepseek-chat"
    MAX_TOKENS = 2000
    TEMPERATURE = 0.7
    
    # Agent配置
    MAX_ITERATIONS = 10
    VERBOSE = True
    
    @classmethod
    def validate(cls):
        """验证配置"""
        if not cls.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY 环境变量未设置")
        return True
