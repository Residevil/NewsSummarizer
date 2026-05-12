import os
import sys
import time
import json
import requests
import logging
from .prompts import SUMMARY_PROMPT
from pathlib import Path
from .utils import BASE_DIR
# Optional: OpenAI-compatible clients
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def resource_path(relative_path):
    # When running as a PyInstaller bundle
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    # When running normally
    return os.path.join(os.path.dirname(__file__), relative_path)

CONFIG_PATH = resource_path("backend/config/model_config.json")


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


config = load_config()


def build_openai_client(api_key=None, base_url=None):
    kwargs = {}
    if api_key:
        kwargs["api_key"] = api_key
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


# --- Provider clients ---

openai_client = build_openai_client(
    api_key=os.getenv("OPENAI_API_KEY")
)

deepseek_client = build_openai_client(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=config["deepseek"]["base_url"]
)

groq_client = build_openai_client(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url=config["groq"]["base_url"]
)


# --- Provider-specific summarizers ---

def summarize_with_openai(text):
    logger.debug("Summarizing with OpenAI")
    try:
        model = config["openai"]["model"]
        resp = openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": SUMMARY_PROMPT.format(content=text)}],
            max_tokens=300,
        )
        logger.debug("OpenAI summary generated successfully")
        return resp.choices[0].message.content
    except Exception as e:
        logger.error("OpenAI error: %s", e)
        return None


def summarize_with_deepseek(text):
    logger.debug("Summarizing with DeepSeek")
    try:
        model = config["deepseek"]["model"]
        resp = deepseek_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": SUMMARY_PROMPT.format(content=text)}],
            max_tokens=300,
        )
        logger.debug("DeepSeek summary generated successfully")
        return resp.choices[0].message.content
    except Exception as e:
        logger.error("DeepSeek error: %s", e)
        return None


def summarize_with_groq(text):
    logger.debug("Summarizing with Groq")
    try:
        model = config["groq"]["model"]
        resp = groq_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": SUMMARY_PROMPT.format(content=text)}],
            max_tokens=300,
        )
        logger.debug("Groq summary generated successfully")
        return resp.choices[0].message.content
    except Exception as e:
        logger.error("Groq error: %s", e)
        return None


def summarize_with_local(text):
    logger.debug("Summarizing with Local/Ollama")
    try:
        url = config["local"]["url"]
        model = config["local"]["model"]
        payload = {
            "model": model,
            "prompt": SUMMARY_PROMPT.format(content=text),
            "stream": False
        }
        r = requests.post(url, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        # Ollama: response in "response" or "output"
        logger.debug("Local summary generated successfully")
        return data.get("response") or data.get("output")
    except Exception as e:
        logger.error("Local model error: %s", e)
        return text[:300] + "..."


def summarize_with_rss(article):
    logger.debug("Summarizing with RSS fallback")
    text = article.get("summary") or article.get("title") or ""
    return text[:300] + "..."


# --- Orchestration ---

PROVIDER_FUNCS = {
    "local": summarize_with_local,
    "groq": summarize_with_groq,
    "openai": summarize_with_openai,
    "deepseek": summarize_with_deepseek,
    "rss": summarize_with_rss
}


import asyncio
import hashlib

# --- LLM Summarization Cache ---
SUMMARY_CACHE = {}

def compute_article_hash(article):
    text = (article.get("content") or "") + (article.get("summary") or "") + (article.get("title") or "")
    return hashlib.sha256(text.encode("utf-8")).hexdigest() if text else None

async def summarize_with_timeout(func, arg, timeout=50):
    try:
        return await asyncio.wait_for(
            asyncio.to_thread(func, arg),
            timeout=timeout
        )
    except Exception as e:
        logger.error(f"Timeout or error in provider summarization: {e}")
        return None

def summarize_single(article):
    """
    Summarize a single article, using provider priority order from config.

    Uses event loop from the context, and falls back to spawning a new loop if necessary
    (e.g., in a context where there's no running event loop, such as a thread).
    """
    text = article.get("content") or article.get("summary") or article.get("title") or ""
    article_hash = compute_article_hash(article)

    if article_hash and article_hash in SUMMARY_CACHE:
        logger.info(f"Cache hit for article: '{article.get('title', '')[:50]}'")
        return SUMMARY_CACHE[article_hash]

    order = [
        config.get("primary"),
        config.get("secondary"),
        config.get("tertiary"),
        config.get("fallback"),
    ]

    logger.debug(
        "Attempting summary for article: '%s' using providers order: %s",
        article.get("title", "")[:50], order
    )

    # Try to use the current running or main event loop; fallback to new loop if needed
    try:
        loop = asyncio.get_event_loop()
        # Depending on context, an event loop may or may not be running
        if loop.is_closed():
            raise RuntimeError("Event loop is closed")
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    for provider in order:
        if not provider:
            continue
        func = PROVIDER_FUNCS.get(provider)
        if not func:
            logger.warning("Provider function '%s' not found", provider)
            continue

        logger.info("Summarizing article '%s' using provider: %s", article.get("title", "")[:50], provider)
        coro = summarize_with_timeout(func, article if provider == "rss" else text, timeout=50)
        try:
            result = loop.run_until_complete(coro)
        except Exception as e:
            logger.error("Error during summary with provider '%s': %s", provider, e)
            result = None

        if result:
            logger.info("Article '%s' summarized successfully by provider: %s", article.get("title", "")[:50], provider)
            if article_hash:
                SUMMARY_CACHE[article_hash] = result
            # If we created a new event loop, close it before returning
            try:
                if loop and loop != asyncio.get_event_loop() and not loop.is_closed():
                    loop.close()
            except Exception:
                pass
            return result
        else:
            logger.warning("Provider '%s' failed to summarize article: '%s'", provider, article.get("title", "")[:50])

    logger.error("All providers failed for article: '%s'; using fallback", article.get("title", "")[:50])
    fallback_summary = text[:300] + "..."
    if article_hash:
        SUMMARY_CACHE[article_hash] = fallback_summary
    try:
        if loop and loop != asyncio.get_event_loop() and not loop.is_closed():
            loop.close()
    except Exception:
        pass
    return fallback_summary


def summarize_articles(articles):
    summaries = []

    logger.info("Starting summarization of %d articles", len(articles))
    for idx, a in enumerate(articles):
        logger.info("Summarizing article %d/%d: '%s'", idx + 1, len(articles), a.get("title", "")[:50])
        summary = summarize_single(a)
        summaries.append({
            "title": a["title"],
            "summary": summary,
            "link": a["link"],
            "source": a["source"],
            "published": a["published"]
        })

        time.sleep(0.2)  # basic rate-limit protection

    logger.info("Summarization complete for %d articles.", len(articles))
    return summaries
