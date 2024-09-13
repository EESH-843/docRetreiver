import threading
import requests

def scrape_news():
    # Example scraping logic
    url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=your_api_key"
    response = requests.get(url)
    articles = response.json()['articles']

    for article in articles:
        # Process and store article text and embeddings in the database
        doc_text = article['content']
        embedding = model.encode([doc_text])[0]
        cursor.execute("INSERT INTO documents (document_text, embedding) VALUES (?, ?)", (doc_text, embedding))
    conn.commit()

# Run the scraper in a separate thread
scraper_thread = threading.Thread(target=scrape_news)
scraper_thread.start()
