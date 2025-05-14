import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain # ConversationChain không được sử dụng trực tiếp trong agent này
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import SystemMessage # Đã có SystemMessagePromptTemplate, nhưng SystemMessage trực tiếp cũng OK
from langchain.tools import Tool

from . import prompt_template as prt
from .helper import create_llm_chain
class CBTChatbotAgent:
    def __init__(self,
                model_name: str = "gemini-2.0-flash", 
                emergency_contact: str = "1111111", 
                temperature: float = 1.0,
                verbose_mode: bool = True):
        self.model_name = model_name
        self.emergency_contact = emergency_contact
        self.temperature = temperature
        self.verbose_mode = verbose_mode

        self.llm = self._initialize_llm()
        self.memory = self._initialize_memory()
        
        self.tools = self._initialize_tools()
        
        self.agent_prompt = self._initialize_agent_prompt()
        self.agent = self._create_agent()
        self.agent_executor = self._create_agent_executor()

    def _initialize_llm(self) -> ChatGoogleGenerativeAI:
        """Khởi tạo Large Language Model."""
        try:
            return ChatGoogleGenerativeAI(
                model=self.model_name,
                temperature=self.temperature,
            )
        except Exception as e:
            print(f"Lỗi khi khởi tạo LLM với model '{self.model_name}': {e}")
            print("Hãy đảm bảo model name chính xác và GOOGLE_API_KEY đã được thiết lập.")
            raise

    def _initialize_memory(self) -> ConversationBufferMemory:
        """Khởi tạo bộ nhớ cho cuộc trò chuyện."""
        return ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

    def _explore_situation_func(self, user_input: str) -> str:
        chain = create_llm_chain(
            prompt = prt.PROMPT_SITUATION_EXPLORATION, 
            llm = self.llm, 
            memory= self.memory, 
            verbose = self.verbose_mode
            )
        return chain.invoke({"user_input": user_input})
    def _identify_nats_func(self, user_input: str) -> str:
        chain = create_llm_chain(
            prompt = prt.PROMPT_NAT_IDENTIFICATION, 
            llm = self.llm, 
            memory= self.memory, 
            verbose = self.verbose_mode
            )
        return chain.invoke({"user_input": user_input})

    def _challenge_thought_func(self, user_input: str) -> str:
        chain = create_llm_chain(
            prompt = prt.PROMPT_THROUT_CHALLENGE, 
            llm = self.llm, 
            memory= self.memory, 
            verbose = self.verbose_mode
            )

    def _restructure_cognition_func(self, user_input: str) -> str:
        chain = create_llm_chain(
            prompt = prt.PROMPT_COGNITIVE_RECONSTRUCTION, 
            llm = self.llm, 
            memory= self.memory, 
            verbose = self.verbose_mode
            )
    def _plan_action_func(self, user_input: str) -> str:
        chain = create_llm_chain(
            prompt = prt.PROMPT_ACTION_PLAN, 
            llm = self.llm, 
            memory= self.memory, 
            verbose = self.verbose_mode
            )
    def _guide_mindfulness_func(self, user_input: str) -> str:
        chain = create_llm_chain(
            prompt = prt.PROMPT_MINDFULLNESS_GUIDE, 
            llm = self.llm, 
            memory= self.memory, 
            verbose = self.verbose_mode
            )
    def _initialize_tools(self) -> list[Tool]:
        """Khởi tạo danh sách các công cụ cho agent."""
        greeting_emotion_chain = create_llm_chain(
            prompt = prt.PROMPT_GREET, 
            llm = self.llm, 
            memory= self.memory, 
            verbose = self.verbose_mode
        )

        tools_list = [
            Tool(
                name="EmotionIdentifierAndGreeter", 
                func=greeting_emotion_chain.invoke,
                description="Hữu ích để chào hỏi người dùng khi bắt đầu cuộc trò chuyện và để xác định cảm xúc ban đầu của họ. Đầu vào là lời nói đầu tiên của người dùng hoặc khi cần kiểm tra lại cảm xúc."
            ),
            Tool(
                name="SituationExplorer",
                func=self._explore_situation_func, 
                description="Hữu ích để khám phá tình huống hoặc sự kiện cụ thể gây ra cảm xúc tiêu cực của người dùng. Cần được sử dụng sau khi cảm xúc đã được xác định."
            ),
            Tool(
                name="NATIdentifier",
                func=self._identify_nats_func, 
                description="Hữu ích để giúp người dùng xác định các suy nghĩ tiêu cực tự động (NATs) của họ liên quan đến một tình huống cụ thể."
            ),
            Tool(
                name="ThoughtChallenger",
                func=self._challenge_thought_func, 
                description="Hướng dẫn người dùng phân tích và thử thách một suy nghĩ tiêu cực cụ thể mà họ đã xác định."
            ),
            Tool(
                name="CognitiveRestructurer",
                func=self._restructure_cognition_func,
                description="Giúp người dùng hình thành một suy nghĩ thay thế, cân bằng và thực tế hơn cho một suy nghĩ tiêu cực đã được thử thách."
            ),
            Tool(
                name="ActionPlanner",
                func=self._plan_action_func, 
                description="Giúp người dùng lập kế hoạch các hành động cụ thể, mang tính xây dựng dựa trên những suy nghĩ đã được tái cấu trúc hoặc để cải thiện tâm trạng."
            ),
            Tool(
                name="MindfulnessGuide",
                func=self._guide_mindfulness_func,
                description="Hướng dẫn một bài tập chánh niệm hoặc kỹ thuật thư giãn ngắn khi người dùng yêu cầu hoặc khi agent nhận thấy có thể hữu ích."
            )
        ]
        return tools_list

    def _initialize_agent_prompt(self) -> ChatPromptTemplate:
        """Khởi tạo prompt cho agent."""
        system_prompt = SystemMessagePromptTemplate.from_template(prt.PROMPT_AGENT)
        prompt = ChatPromptTemplate.from_messages([
            system_prompt,
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{user_input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]).partial(emergency_contact = self.emergency_contact)
        return prompt

    def _create_agent(self):
        """Tạo agent."""
        return create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.agent_prompt,
        )

    def _create_agent_executor(self) -> AgentExecutor:
        """Tạo agent executor."""
        return AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=self.verbose_mode,
            handle_parsing_errors=True, 
            # max_iterations=7, 
            # return_intermediate_steps=True, 
        )

    def chat(self, user_input: str) -> str:
        """
        Gửi đầu vào của người dùng đến agent và nhận phản hồi.
        """
        try:
            response = self.agent_executor.invoke({"user_input": user_input})
            return response.get("output", "Xin lỗi, tôi không thể xử lý yêu cầu này ngay bây giờ.")
        except Exception as e:
            print(f"Lỗi trong quá trình xử lý của agent: {e}")
            return "Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau."

#