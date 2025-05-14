import gradio as gr
import os
from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from core import CBTChatbotAgent


load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.0-flash",
    temperature=1.0,
    api_key= os.getenv("GOOGLE_API_KEY")
)
INTRODUCTION ="""
# CBT là gì?
**Liệu pháp Nhận thức Hành vi (CBT)** là một loại trị liệu tâm lý thông qua trò chuyện. Nó giúp bạn nhận ra và thay đổi những cách suy nghĩ và hành xử tiêu cực hoặc không hữu ích, từ đó cải thiện cảm xúc và chất lượng cuộc sống.

## Ý tưởng cốt lõi:
CBT dựa trên nguyên tắc rằng suy nghĩ, cảm xúc và hành vi của chúng ta có mối liên hệ chặt chẽ và tác động qua lại. Bằng cách thay đổi những suy nghĩ sai lệch và những hành vi không phù hợp, bạn có thể thay đổi cảm xúc của mình theo hướng tích cực hơn.

## CBT hoạt động như thế nào?
- Nhận diện vấn đề: Cùng với nhà trị liệu, bạn xác định những suy nghĩ và hành vi tiêu cực đang gây khó khăn.
- Thách thức và thay đổi suy nghĩ: Bạn học cách phân tích, đặt câu hỏi và thay thế những suy nghĩ tiêu cực bằng những suy nghĩ thực tế và mang tính xây dựng hơn.
- Thay đổi hành vi: Bạn thực hành những hành vi mới, tích cực hơn để giải quyết vấn đề và cải thiện tâm trạng.
- Học kỹ năng: CBT tập trung vào việc trang bị cho bạn những kỹ năng cụ thể để tự đối phó với các thách thức trong cuộc sống, ngay cả sau khi kết thúc trị liệu.

## CBT giúp ích cho:
CBT rất hiệu quả trong việc điều trị nhiều vấn đề như:
- Lo âu, ám ảnh sợ
- Trầm cảm
- Rối loạn ám ảnh cưỡng chế (OCD)
- Rối loạn căng thẳng sau sang chấn (PTSD)
- Các vấn đề về giấc ngủ, quản lý căng thẳng, tức giận...
"""
def chat_fn (message, history):
    response = llm.invoke(message)
    return {
        "role": "assistant",
        "content": response.content
    }

def create_demo(chat_fn):
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown(INTRODUCTION)
            with gr.Column(scale=4):
                gr.Markdown("# Mental health Chatbot")
                chatbot = gr.ChatInterface(
                    fn = chat_fn,
                    type="messages",
                )
    return demo
if __name__ == "__main__":
    cbt_agent = CBTChatbotAgent(
        model_name="gemini-2.0-flash",
        emergency_contact="12345",
        temperature=1.0,
        verbose_mode=True
    )    
    demo = create_demo(
        chat_fn = lambda message, history: {"role": "assistant", "content": cbt_agent.chat(message)}
    )
    demo.launch()