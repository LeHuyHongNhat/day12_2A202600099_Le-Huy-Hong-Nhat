import redis
from datetime import datetime
from fastapi import HTTPException
from .config import settings

r = redis.from_url(settings.REDIS_URL, decode_responses=True)

def check_budget(user_id: str):
    month_key = datetime.now().strftime("%Y-%m")
    key = f"budget:{user_id}:{month_key}"
    
    try:
        current_spending = float(r.get(key) or 0)
        if current_spending >= settings.MONTHLY_BUDGET_USD:
            raise HTTPException(status_code=402, detail="Monthly budget exceeded. Please upgrade your plan.")
    except redis.ConnectionError:
        pass

def record_usage(user_id: str, cost: float):
    month_key = datetime.now().strftime("%Y-%m")
    key = f"budget:{user_id}:{month_key}"
    try:
        r.incrbyfloat(key, cost)
        r.expire(key, 32 * 24 * 3600)
    except redis.ConnectionError:
        pass
