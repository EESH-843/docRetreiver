# Document Retrieval System

This project implements a document retrieval system for chat applications to use as context.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `REDIS_URL`: Redis connection string

3. Run the application:
   ```
   python main.py
   ```

## API Endpoints

- `/health`: Check if the API is active
- `/search`: Search for documents
  - Parameters:
    - `text`: The search query
    - `top_k`: Number of results to return (default: 5)
    - `threshold`: Similarity threshold (default: 0.5)
- `/user_stats/{user_id}`: Get user statistics

## Docker

To run the application in a Docker container:

1. Build the Docker image:
   ```
   docker build -t document-retrieval .
   ```

2. Run the container:
   ```
   docker run -p 8000:8000 document-retrieval
   ```

## Background Scraper

The application includes a background scraper that periodically fetches and stores news articles. The scraper runs every 6 hours.

## Caching

Search results are cached for 1 hour to improve performance.

## Rate Limiting

Users are limited to 5 requests per session. Additional requests will return a 429 status code.
