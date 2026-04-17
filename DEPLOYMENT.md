# Deployment Information

## Public URLs

- **Frontend (Giao diện người dùng):** [https://hospital-chatbot-frontend-n011.onrender.com/](https://hospital-chatbot-frontend-n011.onrender.com/)
- **Backend API (Gốc):** [https://hospital-chatbot-api.onrender.com/](https://hospital-chatbot-api.onrender.com/)
- **AI Agent Endpoint:** [https://hospital-chatbot-api.onrender.com/hospital-rag-agent](https://hospital-chatbot-api.onrender.com/hospital-rag-agent)

## Platform
Render (Blueprint Deployment)

## Test Commands (Production)

### 1. Health Check
```bash
curl https://hospital-chatbot-api.onrender.com/health
# Expected: {"status":"healthy"}
```

### 2. Readiness Check
```bash
curl https://hospital-chatbot-api.onrender.com/ready
# Expected: {"status": "ready"}
```

### 3. API Test (AI Agent)
```bash
curl -X POST https://hospital-chatbot-api.onrender.com/hospital-rag-agent \
  -H "X-API-Key: secret-key-123" \
  -H "Content-Type: application/json" \
  -d '{"text": "Xin chào, bệnh viện có chuyên khoa nội không?", "session_id": "test-session-123"}'
```

## Environment Variables Set (Render)

- `PORT`: 8000
- `REDIS_URL`: (Render Redis Managed Service)
- `AGENT_API_KEY`: secret-key-123
- `OPENAI_API_KEY`: (Đã cấu hình trong Dashboard)
- `NEO4J_URI`: (Đã cấu hình bảo mật)
- `NEO4J_PASSWORD`: (Đã cấu hình bảo mật)

## Screenshots
*(Vui lòng chụp ảnh và lưu vào thư mục screenshots/)*
- `screenshots/frontend.png`: Ảnh giao diện chatbot đang hoạt động.
- `screenshots/render_dashboard.png`: Ảnh các service đang "Live" trên Render.
