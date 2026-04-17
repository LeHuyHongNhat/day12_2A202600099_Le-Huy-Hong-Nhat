from openai import OpenAI
from app.config import settings

# Khởi tạo client OpenAI
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def ask(question: str) -> str:
    # Nếu chưa có key, thông báo lỗi thay vì crash
    if not settings.OPENAI_API_KEY:
        return "⚠️ OpenAI API Key chưa được cấu hình trong môi trường (.env)!"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}],
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Lỗi khi gọi OpenAI API: {str(e)}"
