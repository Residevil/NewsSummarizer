import json
import re

def load_topics():
    with open("backend/config/topics.json") as f:
        return json.load(f)["topics"]

def keyword_match(text, topic):
    pattern = r"\b" + re.escape(topic.lower()) + r"\b"
    return re.search(pattern, text.lower()) is not None

def filter_articles(articles):
    topics = load_topics()
    filtered = []

    for article in articles:
        text = " ".join([
            article.get("title", ""),
            article.get("summary", ""),
            article.get("content", "") or ""
        ])

        if any(keyword_match(text, topic) for topic in topics):
            filtered.append(article)

    return filtered
