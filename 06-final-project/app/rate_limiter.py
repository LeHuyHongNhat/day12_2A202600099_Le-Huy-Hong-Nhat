import time
import redis
from fastapi import HTTPException
from .config import settings

r = redis.from_url(settings.REDIS_URL, decode_responses=True)

def check_rate_limit(user_id: str):
    now = time.time()
    key = f"rate_limit:{user_id}"
    window = 60
    
    try:
        # Sliding window using Redis Sorted Set
        r.zremrangebyscore(key, 0, now - window)
        request_count = r.zcard(key)
        
        if request_count >= settings.RATE_LIMIT_PER_MINUTE:
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again in a minute.")
        
        r.zadd(key, {str(now): now})
        r.expire(key, window)
    except redis.ConnectionError:
        # Fallback if Redis is down (optional)
        pass
