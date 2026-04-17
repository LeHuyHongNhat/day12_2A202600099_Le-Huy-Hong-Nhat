# Production-Ready AI Agent (Final Project)

Dự án này là một AI Agent hoàn chỉnh được thiết kế để vận hành trong môi trường Production, hỗ trợ Scaling, Security và Reliability.

## 🚀 Tính năng chính

- **Hiệu năng & Mở rộng:**
  - Docker Multi-stage build (Image < 300MB).
  - Load Balancing với Nginx (mặc định 3 instance agent).
  - Stateless Design: Lưu trữ hội thoại và session trong Redis.
- **Bảo mật:**
  - Xác thực API Key qua HTTP Header.
  - Rate Limiting: Thuật toán Sliding Window (10 req/min).
  - Cost Guard: Kiểm soát ngân sách hàng tháng ($10/user).
- **Độ tin cậy:**
  - Health & Readiness Checks.
  - Graceful Shutdown (xử lý SIGTERM).
  - Structured JSON Logging.

## 🛠 Cấu trúc thư mục

```text
06-final-project/
├── app/
│   ├── main.py          # Entry point & Lifespan management
│   ├── auth.py          # API Key verification
│   ├── rate_limiter.py  # Redis Sliding Window
│   └── cost_guard.py    # Budget tracking
├── utils/
│   └── mock_llm.py      # OpenAI Integration logic
├── nginx.conf           # Load balancer configuration
├── Dockerfile           # Multi-stage production build
├── docker-compose.yml   # Full stack orchestration
└── requirements.txt     # Dependencies
```

## 💻 Hướng dẫn chạy nhanh (Local)

1. **Chuẩn bị môi trường:**
   Tạo file `.env` từ `.env.example`:
   ```bash
   cp .env.example .env
   # Sửa file .env và điền AGENT_API_KEY và OPENAI_API_KEY của bạn
   ```

2. **Khởi động toàn bộ Stack:**
   ```bash
   docker compose up --build -d
   ```

3. **Kiểm tra trạng thái:**
   ```bash
   docker compose ps
   # Bạn sẽ thấy 3 agent, 1 redis và 1 nginx đang chạy.
   ```

4. **Chạy thử request:**
   ```bash
   curl -X POST http://localhost:8080/ask \
     -H "X-API-Key: secret-key-123" \
     -H "Content-Type: application/json" \
     -d '{"question": "Hello AI Agent"}'
   ```

## ☁️ Deployment

Dự án đã được cấu hình sẵn sàng để deploy lên **Render** thông qua file `render.yaml` ở thư mục gốc.
