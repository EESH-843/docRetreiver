import asyncpg
from asyncpg import Pool
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/document_retrieval")

pool: Pool = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    
    async with pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                embedding vector(384)
            )
        ''')
        
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) UNIQUE NOT NULL,
                request_count INTEGER DEFAULT 0
            )
        ''')

async def get_db_connection():
    async with pool.acquire() as conn:
        yield conn

async def close_db_connection():
    global pool
    if pool:
        await pool.close()