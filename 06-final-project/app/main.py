import os
import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

from .config import settings
from .auth import verify_api_key
from .rate_limiter import check_rate_limit, r as redis_client
from .cost_guard import check_budget, record_usage
from utils.mock_llm import ask

# Structured Logging
logging.basicConfig(level=settings.LOG_LEVEL, format='{"time":"%(asctime)s", "level":"%(levelname)s", "msg":"%(message)s"}')
logger = logging.getLogger(__name__)

_is_ready = False
_in_flight_requests = 0

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _is_ready
    logger.info("Agent starting up...")
    try:
        redis_client.ping()
        _is_ready = True
        logger.info("✅ Agent ready and connected to Redis")
    except Exception as e:
        logger.error(f"❌ Failed to connect to Redis: {e}")
    
    yield
    
    # Graceful Shutdown logic
    _is_ready = False
    logger.info("🔄 Shutdown initiated. Waiting for requests to finish...")
    timeout = 10
    start = time.time()
    while _in_flight_requests > 0 and (time.time() - start) < timeout:
        time.sleep(0.5)
    logger.info("✅ Shutdown complete")

app = FastAPI(title="Production AI Agent", lifespan=lifespan)

@app.middleware("http")
async def track_requests(request, call_next):
    global _in_flight_requests
    _in_flight_requests += 1
    try:
        return await call_next(request)
    finally:
        _in_flight_requests -= 1

class ChatRequest(BaseModel):
    question: str
    session_id: str | None = None

@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.ENVIRONMENT}

@app.get("/ready")
def ready():
    if not _is_ready:
        raise HTTPException(status_code=503, detail="Service not ready")
    return {"status": "ready"}

@app.post("/ask")
async def ask_endpoint(
    body: ChatRequest,
    user_id: str = Depends(verify_api_key)
):
    # Dependencies as logic checks
    check_rate_limit(user_id)
    check_budget(user_id)
    
    # LLM Interaction
    answer = ask(body.question)
    
    # Record simulated cost ($0.01)
    record_usage(user_id, 0.01)
    
    return {
        "user_id": user_id,
        "answer": answer,
        "session_id": body.session_id or "new-session"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
