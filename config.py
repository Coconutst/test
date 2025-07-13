import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置类"""

    # Gemini API配置
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # EXA-AI API配置
    EXA_API_KEY = os.getenv("EXA_API_KEY", "")
    EXA_BASE_URL = "https://api.exa.ai"

    # 代理配置
    HTTP_PROXY = os.getenv("HTTP_PROXY", "")
    HTTPS_PROXY = os.getenv("HTTPS_PROXY", "")
    NO_PROXY = os.getenv("NO_PROXY", "")

    # 模型配置
    DEFAULT_MODEL = "gemini-2.5-pro"
    ALTERNATIVE_MODELS = ["gemini-2.5-flash", "gemini-2.5-flash-preview-04-17"]
    MAX_TOKENS = 2000
    TEMPERATURE = 0.7

    # Agent配置
    MAX_ITERATIONS = 10
    VERBOSE = True

    @classmethod
    def setup_proxy(cls):
        """设置代理环境变量"""
        if cls.HTTP_PROXY:
            os.environ['HTTP_PROXY'] = cls.HTTP_PROXY
            print(f"🌐 设置HTTP代理: {cls.HTTP_PROXY}")
        if cls.HTTPS_PROXY:
            os.environ['HTTPS_PROXY'] = cls.HTTPS_PROXY
            print(f"🌐 设置HTTPS代理: {cls.HTTPS_PROXY}")
        if cls.NO_PROXY:
            os.environ['NO_PROXY'] = cls.NO_PROXY

    @classmethod
    def validate(cls):
        """验证配置"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY 环境变量未设置")

        # 设置代理
        cls.setup_proxy()

        # EXA API密钥是可选的，如果没有会使用备用搜索
        if not cls.EXA_API_KEY:
            print("⚠️ 注意: EXA_API_KEY 未设置，将使用备用搜索功能")

        return True
