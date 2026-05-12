from datetime import datetime
import re

def split_bullet_points(summary):
    """
    Splits a summary into bullet lines and non-bullet lines.
    Uses a single robust regex to extract bullets at line start and everything else as non-bullet.
    Returns (non_bullet_lines, bullet_lines).
    """
    bullet_regex = re.compile(r'^\s*([*-•])\s+(.*)', flags=re.MULTILINE)
    bullet_lines = []
    bullet_spans = []

    # Gather all bullet points and their spans
    for m in bullet_regex.finditer(summary):
        bullet_lines.append(m.group(2).strip())
        bullet_spans.append((m.start(), m.end()))

    # Now get all non-bullet text not part of any bullet span
    non_bullet_sections = []
    prev_end = 0
    for start, end in bullet_spans:
        if prev_end < start:
            non_bullet = summary[prev_end:start].strip()
            if non_bullet:
                non_bullet_sections.append(non_bullet)
        prev_end = end
    # Check for trailing non-bullet text
    if prev_end < len(summary):
        trailing = summary[prev_end:].strip()
        if trailing:
            non_bullet_sections.append(trailing)

    return non_bullet_sections, bullet_lines

def generate_digest(summaries, last_updated=None):
    timestamp = last_updated or datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"<h1>Daily News Digest</h1>"
    html += f"<p><i>Last updated: {timestamp}</i></p><hr>"

    for s in summaries:
        html += f"<h2>{s['title']}</h2>"

        summary = s['summary'].strip()

        # Detect if there are any bullets in the summary
        has_bullet = bool(re.search(r'^\s*([*-•])\s+', summary, flags=re.MULTILINE))
        if has_bullet:
            non_bullet_lines, bullet_lines = split_bullet_points(summary)

            if non_bullet_lines:
                html += f"<p>{'<br>'.join(non_bullet_lines)}</p>"

            if bullet_lines:
                html += "<ul>"
                for b in bullet_lines:
                    html += f"<li>{b}</li>"
                html += "</ul>"
        else:
            # Otherwise, preserve line breaks, but not bullets
            html += f"<p>{summary.replace(chr(10), '<br>')}</p>"

        html += f"<a href='{s['link']}'>Read more</a><hr>"

    return html
