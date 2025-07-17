from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from gemini_client import GeminiLLM
from tools import get_tools
from config import Config


class GeminiAgent:
    """基于Gemini和LangChain的智能体"""

    def __init__(self):
        """初始化智能体"""
        # 验证配置
        Config.validate()

        # 初始化LLM
        self.llm = GeminiLLM()
        
        # 获取工具
        self.tools = get_tools()
        
        # 创建记忆
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 创建提示模板
        self.prompt = self._create_prompt()
        
        # 创建agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # 创建执行器
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=Config.VERBOSE,
            max_iterations=Config.MAX_ITERATIONS,
            handle_parsing_errors=True
        )
    
    def _create_prompt(self) -> PromptTemplate:
        """创建提示模板"""
        template = """你是一个强大的AI助手，严格按照以下格式进行响应。

**重要提醒：**
- 当用户询问时间、日期相关问题时，必须使用system_info工具获取实时信息
- 不要使用任何缓存或记忆中的日期信息
- 每次都要调用工具获取最新的实时数据

**可用工具:**
{tools}

**响应格式:**
你必须严格遵循以下格式。在你的响应中，只能包含'Thought', 'Action', 'Action Input', 和 'Final Answer'。

Question: 用户提出的原始问题
Thought: 我需要做什么来回答这个问题？
Action: 我应该使用哪个工具？必须是[{tool_names}]中的一个。
Action Input: 这个工具需要什么输入？
Observation: 工具执行后的结果是什么？
... (这个 Thought/Action/Action Input/Observation 的序列可以重复N次) ...
Thought: 我现在已经收集了足够的信息，可以回答用户的问题了。
Final Answer: 对用户原始问题的最终回答。

**## 规则 ##**
- **绝对不要** 在一次响应中同时包含 "Action" 和 "Final Answer"。这是禁止的。
- 如果你需要使用工具，就使用 "Action"。
- 只有当你**绝对**完成了所有必要步骤，并且准备好给出最终答案时，才使用 "Final Answer"。
- 对于时间日期查询，必须使用system_info工具，不要依赖记忆或缓存。

**对话历史:**
{chat_history}

**开始!**

Question: {input}
Thought:{agent_scratchpad}"""
        
        return PromptTemplate.from_template(template)
    
    def chat(self, message: str) -> str:
        """与智能体对话"""
        try:
            response = self.agent_executor.invoke({"input": message})
            return response["output"]
        except Exception as e:
            return f"抱歉，处理您的请求时出现错误：{str(e)}"
    
    def reset_memory(self):
        """重置对话记忆"""
        self.memory.clear()
    
    def get_memory(self) -> str:
        """获取对话历史"""
        return str(self.memory.buffer)
