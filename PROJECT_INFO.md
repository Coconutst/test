# DeepSeek智能体项目信息

## 项目概述
基于LangChain和DeepSeek API构建的智能体，具备工具调用和对话记忆功能。

## Git仓库信息

### 初始化Git仓库
```bash
git init
git add .
git commit -m "Initial commit: DeepSeek Agent with LangChain"
```

### 推荐的Git工作流
```bash
# 添加远程仓库
git remote add origin <your-repository-url>

# 推送到远程仓库
git push -u origin main
```

## 项目结构
```
deepseek-agent/
├── agent.py           # 智能体核心实现
├── config.py          # 配置管理
├── deepseek_client.py # DeepSeek API客户端
├── tools.py           # 工具函数集合
├── main.py            # 主程序入口
├── requirements.txt   # 依赖管理
├── README.md          # 项目说明
├── .env.example       # 环境变量模板
├── .gitignore         # Git忽略文件
└── deepseek_agent_env/ # 虚拟环境（被Git忽略）
```

## 核心功能
- 🤖 DeepSeek API集成
- 🔧 多工具支持（计算器、搜索、文本分析）
- 💭 对话记忆功能
- 🎯 ReAct推理模式
- 📝 可扩展架构

## 技术栈
- **语言**: Python 3.8+
- **框架**: LangChain
- **LLM**: DeepSeek API
- **工具**: Pydantic, Requests, Python-dotenv

## 部署说明
1. 克隆仓库
2. 创建虚拟环境：`python -m venv deepseek_agent_env`
3. 激活环境：`deepseek_agent_env\Scripts\activate`
4. 安装依赖：`pip install -r requirements.txt`
5. 配置API密钥：复制`.env.example`为`.env`并填入密钥
6. 运行：`python main.py`

## 开发者信息
- 创建时间：2025-07-11
- 开发工具：Augment Agent + Claude Sonnet 4
- 许可证：MIT

## 版本历史
- v1.0.0 - 初始版本，包含基础智能体功能
