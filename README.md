# Mental Health Chatbot - CBT Therapy Assistant

Dự án này phát triển một chatbot hỗ trợ sức khỏe tinh thần dựa trên nguyên tắc của Liệu pháp Nhận thức Hành vi (Cognitive Behavioral Therapy - CBT). Chatbot được thiết kế để cung cấp hỗ trợ, hướng dẫn và tài nguyên cho người dùng đang đối mặt với các thách thức về sức khỏe tinh thần.

## Tính năng chính

- **Các bước trị liệu CBT**: Chatbot hướng dẫn người dùng thông qua các bước của liệu pháp CBT:
  - Nhận diện cảm xúc
  - Khám phá tình huống
  - Xác định suy nghĩ tiêu cực tự động (NATs)
  - Thử thách suy nghĩ
  - Tái cấu trúc nhận thức
  - Lập kế hoạch hành động
- **Hướng dẫn chánh niệm**: Cung cấp bài tập chánh niệm và kỹ thuật thư giãn
- **Giao diện thân thiện**: Xây dựng trên nền tảng Gradio với giao diện trò chuyện trực quan
- **Tích hợp AI**: Sử dụng Google Gemini để đảm bảo phản hồi tự nhiên và đồng cảm

## Cấu trúc dự án

```
mental_health_chatbots/
├── src/                       # Mã nguồn chính của dự án
│   ├── app.py                 # Điểm khởi chạy chính, thiết lập giao diện người dùng Gradio
│   ├── core/                  # Module core của chatbot
│   │   ├── __init__.py        # Export CBTChatbotAgent
│   │   ├── main.py            # Định nghĩa lớp CBTChatbotAgent chính
│   │   ├── prompt_template.py # Các mẫu prompt cho mô hình ngôn ngữ
│   │   └── helper.py          # Các hàm tiện ích
├── docs/                      # Tài liệu
├── venv/                      # Môi trường ảo (không được theo dõi trong git)
├── .gitignore                 # Cấu hình Git ignore
├── README.md                  # Tài liệu dự án
└── requirements.txt           # Các phụ thuộc của dự án
```

## Công nghệ sử dụng

- **Python** - Ngôn ngữ lập trình chính
- **Gradio** - Framework để xây dựng giao diện người dùng
- **LangChain** - Framework cho các ứng dụng dựa trên mô hình ngôn ngữ lớn (LLM)
- **Google Generative AI** - API mô hình ngôn ngữ (Gemini)
- **Prompt Engineering** - Kỹ thuật thiết kế prompt cho mô hình ngôn ngữ

## Thiết lập môi trường

### Yêu cầu

- Python 3.8 hoặc cao hơn
- Google API Key (cho Gemini)

### Bắt đầu

1. **Clone repository:**
```bash
git clone <repository_url>
cd mental_health_chatbots
```

2. **Thiết lập môi trường ảo:**

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Cài đặt các phụ thuộc:**
```bash
pip install -r requirements.txt
```

4. **Thiết lập biến môi trường:**

Tạo file `.env` trong thư mục gốc và thêm API Key của bạn:
```
GOOGLE_API_KEY=your_google_api_key_here
```

5. **Chạy ứng dụng:**
```bash
python src/app.py
```

Sau khi chạy, giao diện web sẽ được mở tại địa chỉ: `http://127.0.0.1:7860`

## Kiến trúc hệ thống

Dự án sử dụng kiến trúc dựa trên agent, trong đó `CBTChatbotAgent` là thành phần chính điều phối luồng trò chuyện và quy trình CBT:

1. **Agent chính**: Quản lý luồng trò chuyện tổng thể và quyết định công cụ nào cần sử dụng
2. **Các công cụ chuyên biệt**: Mỗi bước trong quy trình CBT được thực hiện bởi một công cụ riêng biệt:
   - EmotionIdentifierAndGreeter
   - SituationExplorer
   - NATIdentifier
   - ThoughtChallenger
   - CognitiveRestructurer
   - ActionPlanner
   - MindfulnessGuide
3. **Bộ nhớ**: Lưu trữ lịch sử trò chuyện để duy trì ngữ cảnh

## Tùy chỉnh và mở rộng

Để tùy chỉnh chatbot:

1. **Chỉnh sửa prompt**: Điều chỉnh các mẫu prompt trong `src/core/prompt_template.py`
2. **Thêm công cụ mới**: Mở rộng `CBTChatbotAgent._initialize_tools()` trong `src/core/main.py`
3. **Điều chỉnh giao diện**: Sửa đổi phần giao diện Gradio trong `src/app.py`

## Đóng góp

Đóng góp luôn được chào đón! Nếu bạn có ý tưởng, đề xuất hoặc báo cáo lỗi, vui lòng mở một issue hoặc gửi pull request.

## License

Dự án này được cấp phép theo [MIT License](LICENSE).

## Tuyên bố miễn trừ trách nhiệm

Chatbot phát triển trong dự án này chỉ nhằm mục đích cung cấp thông tin và hỗ trợ. Nó không thay thế cho lời khuyên, chẩn đoán hoặc điều trị y tế chuyên nghiệp. Nếu bạn đang trải qua khủng hoảng sức khỏe tinh thần, vui lòng tìm kiếm sự giúp đỡ từ chuyên gia sức khỏe tâm thần có trình độ.
