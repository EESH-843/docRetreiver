from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from database import get_db_connection
from encoder import encode_text
from cache import cache_results
import time

router = APIRouter()

class SearchQuery(BaseModel):
    text: str
    top_k: int = 5
    threshold: float = 0.5

class SearchResult(BaseModel):
    id: int
    content: str
    similarity: float

@router.get("/health")
async def health_check():
    return {"status": "OK", "timestamp": time.time()}

@router.post("/search", response_model=List[SearchResult])
@cache_results
async def search(query: SearchQuery, db = Depends(get_db_connection)):
    start_time = time.time()
    
    embedding = encode_text(query.text)
    
    results = await db.fetch("""
        SELECT id, content, 1 - (embedding <=> $1) AS similarity
        FROM documents
        WHERE 1 - (embedding <=> $1) > $2
        ORDER BY similarity DESC
        LIMIT $3
    """, embedding, query.threshold, query.top_k)
    
    end_time = time.time()
    process_time = end_time - start_time
    
    return [SearchResult(**dict(result)) for result in results]

@router.get("/user_stats/{user_id}")
async def get_user_stats(user_id: str, db = Depends(get_db_connection)):
    user = await db.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user['user_id'], "request_count": user['request_count']}