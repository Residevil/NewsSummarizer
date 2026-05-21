from fastapi import FastAPI, Request, Body, Response, Path as FastAPIPath
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .news_fetcher import fetch_news
from .topic_filter import filter_articles
from .summarizer import summarize_articles
from .digest_generator import generate_digest
from .storage.cache import is_cache_valid, load_cache, save_cache
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path as FilePath
import json
import logging
import os
import time

# --- Import model management functionality ---
from backend.models.downloader import download_model
from backend.models.manager import (
    list_installed_models,
    delete_model as manager_delete_model,
    set_active_model,
    speed_test,
)

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory or simple file-based digest read flag & settings persistence for demo
_DIGEST_READ_FILE = FilePath("backend/storage/digest_read.json")
_SETTINGS_FILE = FilePath("backend/storage/settings.json")

def _load_digest_read_flags():
    if _DIGEST_READ_FILE.exists():
        with _DIGEST_READ_FILE.open("r") as f:
            return json.load(f)
    return {}

def _save_digest_read_flags(flags):
    _DIGEST_READ_FILE.parent.mkdir(parents=True, exist_ok=True)
    with _DIGEST_READ_FILE.open("w") as f:
        json.dump(flags, f)

def _load_settings():
    if _SETTINGS_FILE.exists():
        with _SETTINGS_FILE.open("r") as f:
            return json.load(f)
    # Defaults
    return {
        "sources": ["all"],
        "refresh_interval_minutes": 60,
        "model_name": "phi3",
        "max_articles": 30,
        "languages": ["en"]
    }

def _save_settings(settings):
    _SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with _SETTINGS_FILE.open("w") as f:
        json.dump(settings, f)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/models")
def list_models():
    """
    List all installed models via manager.
    """
    return list_installed_models()

@app.post("/models/download")
def download_models(
    backend: str = Body(..., embed=True),
    model_name: str = Body(..., embed=True)
):
    """
    Download a model for the specified backend.
    For Ollama, uses download_model logic.
    """
    if backend.lower() == "ollama":
        ok = download_model(model_name)
        if ok:
            return {"status": "ok"}
        return {"status": "error", "detail": "Failed to download model"}
    else:
        # Placeholder for other backends, can be extended...
        return {
            "status": "error",
            "detail": f"Download not implemented for backend '{backend}'."
        }

@app.delete("/models/{name}")
def delete_model(name: str):
    """
    Delete a model and associated files via manager logic.
    """
    result = manager_delete_model(name)
    if result:
        return {"status": "ok", "deleted": name}
    else:
        return {"status": "error", "detail": f"Failed to delete model {name}"}

@app.post("/models/select")
async def select_models(request: Request):
    data = await request.json()
    selected_model = data.get("selected_model") or data.get("active_model")
    if not selected_model:
        return JSONResponse({"error": "No selected_model provided."}, status_code=400)
    set_active_model(selected_model)
    # Persist in settings as well (extra helpful for backend-driven UI sync)
    settings = _load_settings()
    settings["model_name"] = selected_model
    _save_settings(settings)
    return {"status": "ok", "selected_model": selected_model}

@app.post("/models/test")
def speed_test_models(model_name: str = Body(..., embed=True)):
    """
    Speed test a given model using manager's speed_test logic.
    """
    result = speed_test(model_name)
    return result

@app.get("/digests", response_class=JSONResponse)
def list_digests():
    """
    API endpoint: returns an array of digests (JSON, not HTML).
    """
    # Summarize as before
    if is_cache_valid():
        articles = load_cache()
    else:
        articles = fetch_news()
        save_cache(articles)
    filtered, topic_hits = filter_articles(articles)
    summaries = summarize_articles(filtered)

    # Assign generated IDs etc
    read_flags = _load_digest_read_flags()
    digests = []
    for idx, item in enumerate(summaries):
        digest_id = item.get("id") or item.get("guid") or str(idx)
        digest = {
            "id": digest_id,
            "title": item.get("title", ""),
            "source": item.get("source", ""),
            "published_at": item.get("published", ""),
            "summary": item.get("summary", ""),
            "score": item.get("score", 0),
            "read": bool(read_flags.get(str(digest_id), False))
        }
        digests.append(digest)

    return digests

@app.post("/digests/{id}/read")
def mark_digest_as_read(id: str = FastAPIPath(...)):
    """
    Mark a specific digest as read.
    """
    flags = _load_digest_read_flags()
    flags[str(id)] = True
    _save_digest_read_flags(flags)
    return {"status": "ok", "id": id, "read": True}

@app.post("/digests/refresh")
def refresh_digests():
    """
    Force refresh and summarization. Returns new digest list.
    """
    articles = fetch_news()
    save_cache(articles)
    filtered, topic_hits = filter_articles(articles)
    summaries = summarize_articles(filtered)
    # Reset read flags
    _save_digest_read_flags({})
    # Same array format as /digests
    digests = []
    for idx, item in enumerate(summaries):
        digest_id = item.get("id") or item.get("guid") or str(idx)
        digest = {
            "id": digest_id,
            "title": item.get("title", ""),
            "source": item.get("source", ""),
            "published_at": item.get("published", ""),
            "summary": item.get("summary", ""),
            "score": item.get("score", 0),
            "read": False
        }
        digests.append(digest)
    return digests

@app.get("/settings")
def get_settings():
    """
    Get backend settings for summarizer/digest.
    """
    return _load_settings()

@app.post("/settings")
def post_settings(settings: dict = Body(...)):
    """
    Update settings for summarizer/digest.
    """
    current = _load_settings()
    current.update(settings)
    _save_settings(current)
    return {"status": "ok", "settings": current}

@app.get("/digests/html", response_class=HTMLResponse)
def get_digest_html():
    """
    HTML version of digests (old behavior, not for new UI).
    """
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