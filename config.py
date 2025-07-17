import os
from dotenv import load_dotenv

# 加载环境变量
# load_dotenv() 会自动查找并加载项目根目录下的 .env 文件
load_dotenv()


class Config:
    """配置类，集中管理所有配置项"""

    # --- API 配置 ---
    # Gemini API配置
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # EXA-AI API配置 (可选)
    EXA_API_KEY = os.getenv("EXA_API_KEY", "")
    EXA_BASE_URL = "https://api.exa.ai"

    # --- 网络代理配置 (新增部分) ---
    # 优先从环境变量 "HTTP_PROXY" 读取, 其次是 "HTTPS_PROXY"
    # 这允许您的应用通过Clash等本地代理进行网络请求
    # 如果两者都未设置，则为空字符串，表示不使用代理
    PROXY_URL = os.getenv("HTTP_PROXY", os.getenv("HTTPS_PROXY", ""))

    # 模型配置
    DEFAULT_MODEL = "gemini-2.5-flash-preview-04-17"
    ALTERNATIVE_MODELS = ["gemini-2.5-flash", "gemini-2.5-pro","gemini-2.5-flash-preview-04-17"]
    MAX_TOKENS = 20000
    TEMPERATURE = 0.7

    # Agent配置
    MAX_ITERATIONS = 10
    VERBOSE = True

    # --- Agent配置 ---
    MAX_ITERATIONS = 10
    VERBOSE = True

    @classmethod
    def validate(cls):
        """验证并打印关键配置信息"""
        print("--- 正在加载应用配置 ---")

        # 验证 Gemini API 密钥
        if not cls.GEMINI_API_KEY:
            raise ValueError("❌ 错误: GEMINI_API_KEY 环境变量未设置，请在 .env 文件中配置")
        else:
            # 打印部分密钥以供确认，隐藏大部分内容保护安全
            print(f"✅ Gemini API 密钥已加载 (结尾为: ...{cls.GEMINI_API_KEY[-4:]})")

        # 验证 EXA API 密钥 (可选)
        if not cls.EXA_API_KEY:
            print("⚠️ 注意: EXA_API_KEY 未设置，将使用备用搜索功能")
        else:
            print("✅ Exa API 密钥已加载")

        # 验证并打印代理配置 (新增部分)
        if cls.PROXY_URL:
            print(f"✅ 网络代理已配置: {cls.PROXY_URL}")
        else:
            print("ℹ️  提示: 未配置网络代理，将直接进行网络连接")

        print("--------------------------")
        return True