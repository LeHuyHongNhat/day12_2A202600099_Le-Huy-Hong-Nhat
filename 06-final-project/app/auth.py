from fastapi import Header, HTTPException
from .config import settings

def verify_api_key(x_api_key: str = Header(..., description="API Key for authentication")):
    if x_api_key != settings.AGENT_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    # Trả về một user_id giả lập
    return "user_123"
