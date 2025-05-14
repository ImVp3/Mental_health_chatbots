from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate, # Giữ lại nếu bạn có kế hoạch sử dụng riêng lẻ
    HumanMessagePromptTemplate,
)
from langchain.memory import ConversationBufferMemory

def create_llm_chain (prompt: str, llm: ChatGoogleGenerativeAI, memory:ConversationBufferMemory|None = None, verbose: bool = False) -> LLMChain:
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{user_input}")
    ])
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory = memory,
        verbose=verbose
    )
    return chain