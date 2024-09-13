import uvicorn
from fastapi import FastAPI, Depends
from api import router as api_router
from database import init_db
from scraper import start_background_scraper
from cache import init_cache
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Document Retrieval API")

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing application...")
    # Initialize database
    await init_db()
    logger.info("Database initialized")

    # Initialize cache
    init_cache()
    logger.info("Cache initialized")

    # Start background scraper
    start_background_scraper()
    logger.info("Background scraper started")

# Include API routes
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Document Retrieval API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)