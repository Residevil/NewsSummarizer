import feedparser
from datetime import datetime

RSS_FEEDS = {
    "NYTimes World": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "BBC World": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "Reuters World": "https://feeds.reuters.com/Reuters/worldNews",
    "AP News": "https://apnews.com/hub/apf-intlnews?format=xml",
    "TechCrunch": "https://techcrunch.com/feed/",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml"
}

def parse_date(entry):
    try:
        return datetime(*entry.published_parsed[:6])
    except:
        return None

def fetch_news():
    articles = []

    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)

        for entry in feed.entries:
            published = parse_date(entry)
            if isinstance(published, datetime):
                published = published.isoformat()

            articles.append({
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "content": entry.get("content", [{}])[0].get("value", None),
                "link": entry.get("link", ""),
                "source": source,
                "published": published
            })

    return articles
