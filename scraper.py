import asyncio
import aiohttp
from bs4 import BeautifulSoup
from database import get_db_connection
from encoder import encode_and_store_documents
import logging

logger = logging.getLogger(__name__)

async def scrape_news():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://example-news-site.com') as response:
            html = await response.text()
    
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article')
    
    documents = [article.get_text() for article in articles]
    
    db = await anext(get_db_connection())
    await encode_and_store_documents(db, documents)
    
    logger.info(f"Scraped and stored {len(documents)} articles")

async def periodic_scraper():
    while True:
        try:
            await scrape_news()
        except Exception as e:
            logger.error(f"Error in scraper: {e}")
        await asyncio.sleep(6 * 60 * 60)  # Sleep for 6 hours

def start_background_scraper():
    asyncio.create_task(periodic_scraper())