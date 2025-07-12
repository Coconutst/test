import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置类"""
    
    # DeepSeek API配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
    
    # EXA-AI API配置
    EXA_API_KEY = os.getenv("EXA_API_KEY", "")
    EXA_BASE_URL = "https://api.exa.ai"

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

        # EXA API密钥是可选的，如果没有会使用备用搜索
        if not cls.EXA_API_KEY:
            print("⚠️ 注意: EXA_API_KEY 未设置，将使用备用搜索功能")

        return True
