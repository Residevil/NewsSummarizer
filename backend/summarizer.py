def summarize_articles(articles):
    # Placeholder — LLM integration later
    summaries = []
    for a in articles:
        summaries.append({
            "title": a["title"],
            "summary": a["summary"][:200] + "...",
            "link": a["link"]
        })
    return summaries
