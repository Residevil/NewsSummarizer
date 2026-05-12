import json
import re
import logging
from .utils import BASE_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOPICS_PATH= BASE_DIR / "backend" / "config" / "topics.json"

def load_topics():
    return json.loads(TOPICS_PATH.read_text())["topics"]

def keyword_match(text, topic):
    pattern = r"\b" + re.escape(topic.lower()) + r"\b"
    return re.search(pattern, text.lower()) is not None


def filter_articles(articles):
    topics = load_topics()
    filtered = []
    topic_hits = {topic: 0 for topic in topics}

    logger.info(f"Filtering {len(articles)} articles by {len(topics)} topics")
    for idx, article in enumerate(articles):
        text = " ".join([
            article.get("title", ""),
            article.get("summary", ""),
            article.get("content", "") or ""
        ])

        matched = False
        for topic in topics:
            if keyword_match(text, topic):
                topic_hits[topic] += 1
                matched = True

        if matched:
            filtered.append(article)
            logger.debug(f"[{idx+1}/{len(articles)}] Article matched: '{article.get('title', '')}'")

        if (idx + 1) % 10 == 0 or (idx + 1) == len(articles):
            logger.info(f"Processed {idx + 1} of {len(articles)} articles...")

    logger.info(f"Filter complete: {len(filtered)} articles matched at least one topic.")
    logger.info(f"Topic hits: {topic_hits}")

    return filtered, topic_hits
