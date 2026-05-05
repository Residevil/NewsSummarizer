def generate_digest(summaries):
    html = "<h1>Daily News Digest</h1>"
    for s in summaries:
        html += f"<h2>{s['title']}</h2>"
        html += f"<p>{s['summary']}</p>"
        html += f"<a href='{s['link']}'>Read more</a><hr>"
    return html
