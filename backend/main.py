# ✅ **3. Initial Python Boilerplate**

### `backend/main.py`

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .news_fetcher import fetch_news
from .topic_filter import filter_articles
from .summarizer import summarize_articles
from .digest_generator import generate_digest

app = FastAPI()

@app.get("/digest", response_class=HTMLResponse)
def get_digest():
    articles = fetch_news()
    filtered = filter_articles(articles)
    summaries = summarize_articles(filtered)
    digest_html = generate_digest(summaries)
    return digest_html
