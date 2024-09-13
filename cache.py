import redis
import json
from functools import wraps
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = None

def init_cache():
    global redis_client
    redis_client = redis.from_url(REDIS_URL)

def cache_results(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not redis_client:
            return await func(*args, **kwargs)
        
        cache_key = f"search:{json.dumps(args)}:{json.dumps(kwargs)}"
        cached_result = redis_client.get(cache_key)
        
        if cached_result:
            return json.loads(cached_result)
        
        result = await func(*args, **kwargs)
        redis_client.setex(cache_key, 3600, json.dumps(result))  # Cache for 1 hour
        return result
    
    return wrapper