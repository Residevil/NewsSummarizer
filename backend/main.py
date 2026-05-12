# ✅ **3. Initial Python Boilerplate**

### `backend/main.py`

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from .news_fetcher import fetch_news
from .topic_filter import filter_articles
from .summarizer import summarize_articles
from .digest_generator import generate_digest
from .storage.cache import is_cache_valid, load_cache, save_cache
from datetime import datetime
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/digest", response_class=HTMLResponse)
def get_digest():
    # Load or fetch articles
    if is_cache_valid():
        articles = load_cache()
        logger.info("Using cached articles")
    else:
        articles = fetch_news()
        save_cache(articles)
        logger.info("Fetched fresh articles")

    filtered, topic_hits = filter_articles(articles)
    summaries = summarize_articles(filtered)

    logger.info(f"Fetched {len(articles)} articles")
    logger.info(f"Filtered down to {len(filtered)} articles")
    logger.info(f"Topic hits: {topic_hits}")

    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M")
    digest_html = generate_digest(summaries, last_updated)
    # logger.info("Digest generated successfully")

    return digest_html

@app.get("/raw", response_class=JSONResponse)
def get_raw():
    if is_cache_valid():
        articles = load_cache()
    else:
        articles = fetch_news()
        save_cache(articles)

    filtered, topic_hits = filter_articles(articles)

    return {
        "total_articles": len(articles),
        "filtered_articles": len(filtered),
        "topic_hits": topic_hits,
        "articles": filtered
    }