# Steps
1. **Clone repository:**
   ```bash
   git clone https://github.com/minhtruong0208/voice-changer.git
   cd voice-changer

2. **Tạo môi trường ảo**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Đối với Linux/MacOS
   venv\Scripts\activate     # Đối với Windows

3. **Cài đặt dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Cấu hình .env**
- Tạo file .env trong thư mục gốc với nội dung:
   ```bash
   AZURE_SUBSCRIPTION_KEY=your_azure_key
   AZURE_REGION=your_region
   DEFAULT_VOICE=vi-VN-HoaiMyNeural
- Lấy key và region từ Azure Portal (Speech resource).

5. **Chạy ứng dụng**
   ```bash
   python main.py
- API sẽ chạy tại http://localhost:8000
