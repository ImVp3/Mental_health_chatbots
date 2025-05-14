# Hướng Dẫn Kỹ Thuật - Mental Health Chatbot

Tài liệu này cung cấp thông tin chi tiết về kiến trúc, thiết kế và cách triển khai Mental Health Chatbot dựa trên Liệu pháp Nhận thức Hành vi (CBT).

## Mục lục

- [Kiến trúc tổng quan](#kiến-trúc-tổng-quan)
- [Mô-đun chính](#mô-đun-chính)
- [Các mẫu prompt](#các-mẫu-prompt)
- [Luồng xử lý](#luồng-xử-lý)
- [Cách tùy chỉnh](#cách-tùy-chỉnh)
- [Troubleshooting](#troubleshooting)
- [Các API sử dụng](#các-api-sử-dụng)

## Kiến trúc tổng quan

Dự án sử dụng mô hình dựa trên Agent theo framework LangChain, với kiến trúc như sau:

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│                 │      │                 │      │                 │
│   Gradio UI     │─────▶│  CBTChatbot     │─────▶│  Google Gemini  │
│   (app.py)      │      │  Agent          │      │  API            │
│                 │      │  (main.py)      │      │                 │
└─────────────────┘      └────────┬────────┘      └─────────────────┘
                                 │
                                 ▼
                         ┌─────────────────┐
                         │                 │
                         │  Specialized    │
                         │  Tools          │
                         │                 │
                         └─────────────────┘
```

### Luồng dữ liệu:

1. Người dùng nhập vào thông qua giao diện Gradio
2. CBTChatbotAgent xử lý đầu vào
3. Agent quyết định công cụ nào sẽ được sử dụng 
4. Công cụ được chọn sẽ sử dụng Google Gemini API để sinh phản hồi
5. Phản hồi được trả về cho người dùng thông qua giao diện Gradio

## Mô-đun chính

### 1. CBTChatbotAgent (`src/core/main.py`)

Lớp chính điều phối toàn bộ logic của chatbot:

```python
class CBTChatbotAgent:
    def __init__(self,
                model_name: str = "gemini-2.0-flash", 
                emergency_contact: str = "1111111", 
                temperature: float = 1.0,
                verbose_mode: bool = True):
        # Khởi tạo các thành phần
        self.llm = self._initialize_llm()
        self.memory = self._initialize_memory()
        self.tools = self._initialize_tools()
        self.agent_prompt = self._initialize_agent_prompt()
        self.agent = self._create_agent()
        self.agent_executor = self._create_agent_executor()

    def chat(self, user_input: str) -> str:
        # Xử lý đầu vào của người dùng
        response = self.agent_executor.invoke({"user_input": user_input})
        return response.get("output", "Xin lỗi, tôi không thể xử lý yêu cầu này ngay bây giờ.")
```

### 2. Giao diện người dùng (`src/app.py`)

Sử dụng Gradio để tạo giao diện người dùng trực quan:

```python
def create_demo(chat_fn):
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown(INTRODUCTION)  # Giới thiệu về CBT
            with gr.Column(scale=4):
                gr.Markdown("# Mental health Chatbot")
                chatbot = gr.ChatInterface(
                    fn = chat_fn,
                    type="messages",
                )
    return demo
```

### 3. Các công cụ chuyên biệt

Chatbot sử dụng 7 công cụ chính để thực hiện các bước khác nhau trong quá trình CBT:

- **EmotionIdentifierAndGreeter**: Chào hỏi và nhận diện cảm xúc
- **SituationExplorer**: Khám phá tình huống cụ thể
- **NATIdentifier**: Xác định suy nghĩ tiêu cực tự động
- **ThoughtChallenger**: Thử thách những suy nghĩ tiêu cực
- **CognitiveRestructurer**: Tái cấu trúc nhận thức
- **ActionPlanner**: Lên kế hoạch hành động
- **MindfulnessGuide**: Hướng dẫn chánh niệm

### 4. Hàm tiện ích (`src/core/helper.py`)

```python
def create_llm_chain(prompt: str, llm: ChatGoogleGenerativeAI, memory:ConversationBufferMemory|None = None, verbose: bool = False) -> LLMChain:
    # Tạo chain cho LLM với các prompt template
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
```

## Các mẫu prompt

Dự án sử dụng các mẫu prompt được định nghĩa trong `src/core/prompt_template.py`:

| Tên prompt | Mục đích |
|------------|----------|
| PROMPT_AGENT | Định nghĩa vai trò của agent |
| PROMPT_GREET | Chào hỏi và xác định cảm xúc |
| PROMPT_SITUATION_EXPLORATION | Khám phá tình huống cụ thể |
| PROMPT_NAT_IDENTIFICATION | Nhận diện suy nghĩ tiêu cực |
| PROMPT_THROUT_CHALLENGE | Thử thách suy nghĩ tiêu cực |
| PROMPT_COGNITIVE_RECONSTRUCTION | Tái cấu trúc nhận thức |
| PROMPT_ACTION_PLAN | Lập kế hoạch hành động |
| PROMPT_MINDFULLNESS_GUIDE | Hướng dẫn chánh niệm |

## Luồng xử lý

1. **Khởi tạo**: Chatbot được khởi tạo khi chạy `app.py`:
   ```python
   cbt_agent = CBTChatbotAgent(
       model_name="gemini-2.0-flash",
       emergency_contact="12345",
       temperature=1.0,
       verbose_mode=True
   )
   ```

2. **Xử lý đầu vào người dùng**:
   - Đầu vào của người dùng được chuyển đến phương thức `chat()` của `CBTChatbotAgent`
   - Agent chọn công cụ phù hợp dựa trên ngữ cảnh của cuộc trò chuyện
   - Công cụ được chọn xử lý đầu vào và sinh ra phản hồi

3. **Các bước CBT**:
   - Chatbot hướng dẫn người dùng theo trình tự các bước của liệu pháp CBT
   - Sử dụng bộ nhớ để duy trì ngữ cảnh qua các lượt trò chuyện
   - Xử lý các tình huống khẩn cấp với thông tin liên hệ cung cấp

## Cách tùy chỉnh

### 1. Thay đổi mẫu prompt

Chỉnh sửa các mẫu prompt trong `src/core/prompt_template.py` để thay đổi cách chatbot giao tiếp hoặc cách thức thực hiện các bước CBT.

### 2. Thêm công cụ mới

Để thêm một công cụ mới, ví dụ công cụ xác định sai lầm nhận thức:

```python
# 1. Tạo hàm xử lý trong CBTChatbotAgent
def _identify_cognitive_distortions_func(self, user_input: str) -> str:
    chain = create_llm_chain(
        prompt = "Template prompt cho công cụ mới", 
        llm = self.llm, 
        memory= self.memory, 
        verbose = self.verbose_mode
    )
    return chain.invoke({"user_input": user_input})

# 2. Thêm công cụ vào _initialize_tools()
tools_list.append(
    Tool(
        name="CognitiveDistortionIdentifier",
        func=self._identify_cognitive_distortions_func, 
        description="Giúp người dùng xác định các sai lầm nhận thức phổ biến trong suy nghĩ của họ."
    )
)
```

### 3. Chỉnh sửa thông tin liên hệ khẩn cấp

Thay đổi thông tin liên hệ khẩn cấp khi khởi tạo CBTChatbotAgent:

```python
cbt_agent = CBTChatbotAgent(
    model_name="gemini-2.0-flash",
    emergency_contact="YOUR_EMERGENCY_CONTACT",
    temperature=1.0,
    verbose_mode=True
)
```

### 4. Điều chỉnh giao diện người dùng

Chỉnh sửa `src/app.py` để thay đổi giao diện người dùng:

```python
# Ví dụ: Thêm nút hướng dẫn nhanh
with gr.Column(scale=4):
    gr.Markdown("# Mental health Chatbot")
    
    with gr.Row():
        anxiety_btn = gr.Button("Tôi cảm thấy lo âu")
        depression_btn = gr.Button("Tôi cảm thấy buồn")
    
    chatbot = gr.ChatInterface(
        fn = chat_fn,
        type="messages",
    )
    
    anxiety_btn.click(lambda: {"role": "user", "content": "Tôi đang cảm thấy lo âu"}, None, chatbot)
    depression_btn.click(lambda: {"role": "user", "content": "Tôi đang cảm thấy buồn"}, None, chatbot)
```

## Troubleshooting

### Vấn đề phổ biến

1. **Lỗi API Key**:
   ```
   Lỗi khi khởi tạo LLM với model 'gemini-2.0-flash': Google API key not found
   ```
   **Giải pháp**: Đảm bảo file `.env` đã được tạo với GOOGLE_API_KEY hợp lệ.

2. **Lỗi khi chia sẻ bộ nhớ giữa các công cụ**:
   **Giải pháp**: Đảm bảo tất cả các công cụ sử dụng cùng một đối tượng memory của CBTChatbotAgent.

3. **Phản hồi không nhất quán**:
   **Giải pháp**: Điều chỉnh nhiệt độ (temperature) khi khởi tạo LLM để có phản hồi nhất quán hơn (giá trị thấp hơn) hoặc sáng tạo hơn (giá trị cao hơn).

## Các API sử dụng

### Google Generative AI API

Dự án sử dụng API Google Generative AI thông qua LangChain để tương tác với mô hình Gemini:

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=1.0,
    api_key=os.getenv("GOOGLE_API_KEY")
)
```

Để sử dụng API này, bạn cần:
1. Đăng ký tài khoản Google Cloud Platform
2. Kích hoạt API Generative AI
3. Tạo API Key và thêm vào file `.env`

### Gradio API

Giao diện người dùng được xây dựng bằng Gradio:

```python
import gradio as gr

def chat_fn(message, history):
    # Xử lý tin nhắn...
    return response

demo = gr.ChatInterface(chat_fn)
demo.launch()
```

## Ví dụ

### Cuộc trò chuyện mẫu:

```
User: Tôi đang cảm thấy lo lắng về bài thuyết trình ngày mai.

Chatbot: Tôi hiểu cảm giác lo lắng trước một bài thuyết trình. Bạn có thể chia sẻ thêm về tình huống này được không? Có điều gì cụ thể khiến bạn lo lắng?

User: Tôi sợ mọi người sẽ đánh giá tôi nếu tôi mắc lỗi.

Chatbot: Cảm ơn bạn đã chia sẻ. Khi nghĩ về việc mắc lỗi trong bài thuyết trình, những suy nghĩ cụ thể nào xuất hiện trong đầu bạn?

User: Tôi nghĩ mọi người sẽ cho rằng tôi không đủ năng lực và tôi sẽ làm mất mặt bản thân.

Chatbot: Tôi hiểu suy nghĩ đó. Hãy thử thách suy nghĩ này một chút nhé. Có bằng chứng nào cho thấy mọi người sẽ đánh giá bạn nghiêm khắc như vậy không? Bạn có từng thấy ai đó mắc lỗi trong thuyết trình và bị mọi người đánh giá tiêu cực không?
```

---

Tài liệu này cung cấp tổng quan về thiết kế và triển khai Mental Health Chatbot. Để biết thêm thông tin về liệu pháp CBT, xin tham khảo `docs/CBT_methods.md`. 