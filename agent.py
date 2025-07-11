from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from deepseek_client import DeepSeekLLM
from tools import get_tools
from config import Config


class DeepSeekAgent:
    """基于DeepSeek和LangChain的智能体"""
    
    def __init__(self):
        """初始化智能体"""
        # 验证配置
        Config.validate()
        
        # 初始化LLM
        self.llm = DeepSeekLLM()
        
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
        template = """你是一个有用的AI助手，可以使用各种工具来帮助用户解决问题。

你有以下工具可以使用：
{tools}

使用以下格式：

Question: 用户的问题
Thought: 你应该思考要做什么
Action: 要采取的行动，应该是[{tool_names}]中的一个
Action Input: 行动的输入
Observation: 行动的结果
... (这个Thought/Action/Action Input/Observation可以重复N次)
Thought: 我现在知道最终答案了
Final Answer: 对原始问题的最终答案

开始！

Previous conversation history:
{chat_history}

Question: {input}
Thought: {agent_scratchpad}"""
        
        return PromptTemplate(
            template=template,
            input_variables=["input", "chat_history", "agent_scratchpad"],
            partial_variables={
                "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools]),
                "tool_names": ", ".join([tool.name for tool in self.tools])
            }
        )
    
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
