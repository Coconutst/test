# DeepSeek智能体

基于LangChain和DeepSeek API构建的简单智能体，具备工具调用和对话记忆功能。

## 功能特性

- 🤖 基于DeepSeek API的大语言模型
- 🔧 集成多种工具（计算器、搜索、文本分析）
- 💭 对话记忆功能
- 🎯 ReAct推理模式
- 📝 可扩展的工具系统

## 安装依赖

### 方法1：使用用户安装（推荐）
```bash
pip install --user -r requirements.txt
```

### 方法2：使用虚拟环境（最佳实践）
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 方法3：管理员权限安装
```bash
# 以管理员身份运行命令提示符，然后执行：
pip install -r requirements.txt
```

## 配置

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入您的DeepSeek API密钥：
```
DEEPSEEK_API_KEY=your_actual_api_key_here
```

## 使用方法

### 交互式对话

```bash
python main.py
```

### 演示模式

```bash
python main.py demo
```

## 项目结构

```
├── agent.py           # 智能体核心实现
├── config.py          # 配置管理
├── deepseek_client.py # DeepSeek API客户端
├── tools.py           # 工具函数集合
├── main.py            # 主程序入口
├── requirements.txt   # 依赖列表
├── .env.example       # 环境变量模板
└── README.md          # 说明文档
```

## 可用工具

1. **计算器 (calculator)**
   - 执行数学计算
   - 支持基本数学函数

2. **网络搜索 (web_search)**
   - 模拟网络搜索功能
   - 可扩展为真实搜索API

3. **文本分析 (text_analysis)**
   - 字数统计
   - 简单情感分析

## 扩展开发

### 添加新工具

1. 在 `tools.py` 中创建新的工具类：

```python
class YourTool(BaseTool):
    name = "your_tool"
    description = "工具描述"
    
    def _run(self, input_param: str) -> str:
        # 工具逻辑
        return "结果"
```

2. 在 `get_tools()` 函数中添加新工具：

```python
def get_tools():
    return [
        Calculator(),
        WebSearch(),
        TextAnalysis(),
        YourTool()  # 添加新工具
    ]
```

### 自定义配置

修改 `config.py` 中的配置参数：

- `MAX_TOKENS`: 最大生成token数
- `TEMPERATURE`: 生成温度
- `MAX_ITERATIONS`: 最大推理步数

## 注意事项

1. 确保DeepSeek API密钥有效
2. 网络连接正常
3. Python版本 >= 3.8

## 故障排除

### 常见问题

1. **API密钥错误**
   - 检查 `.env` 文件中的API密钥是否正确
   - 确认API密钥有效且有足够额度

2. **网络连接问题**
   - 检查网络连接
   - 确认可以访问DeepSeek API

3. **依赖安装问题**
   - 使用虚拟环境
   - 确保Python版本兼容

## 许可证

MIT License
