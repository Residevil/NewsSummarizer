# Automated News Summarizer (Phase 1 — Text Only)

## Overview
The Automated News Summarizer is a desktop-startup program that fetches global news, filters it by user-selected topics, summarizes the articles using AI, and presents a clean daily digest when the computer starts.

This is **Phase 1 (Text Only)**:
- Fetch news from RSS feeds or APIs
- Filter by user topics
- Summarize using LLMs (multiple providers: OpenAI, DeepSeek, Groq)
- Generate a daily digest (HTML/Markdown)
- Display digest automatically on Windows startup

Future phases:
- Phase 2: Audio summaries
- Phase 3: Video summaries

---

## Architecture

### High-Level Flow
1. Windows boots → Startup script runs  
2. Browser opens `http://localhost:8000/digest`  
3. Backend (running in WSL2 or as a packaged binary)  
   - Fetches news  
   - Filters by topics  
   - Summarizes using multiple LLM providers  
   - Generates digest  
4. Digest displayed to user

### Components
- **Windows**
  - Startup script
  - Browser UI
- **WSL2 (Ubuntu) / PyInstaller Binary**
  - Python backend
  - News ingestion
  - Topic filtering
  - Summarization engine (supports OpenAI, DeepSeek, Groq)
  - Digest generator
  - Local storage
- **Optional: Tauri App**
  - Desktop application UI (future phases)

---

## Architecture Diagram (Optimized Overview)

**System Structure:**

```
┌─────────────────────────────┐
│       Windows OS            │
│ ─ Startup Script            │
│ ─ Browser UI                │
└────────────┬────────────────┘
             │
             ▼
┌───────────────────────────────────┐
│   WSL2 (Ubuntu) / PyInstaller     │
│ ─ Python Backend                  │
│    • News Fetcher                 │
│    • Topic Filter                 │
│    • Summarizer (LLM Providers)   │
│       · OpenAI                    │
│       · DeepSeek                  │
│       · Groq                      │
│    • Digest Generator             │
│    • Local Storage                │
└───────────────────────────────────┘
             │
             ▼
┌─────────────────────────────┐
│      (Optional)             │
│      Tauri App UI           │
└─────────────────────────────┘
```

---

## Architecture Diagram (Mermaid)

```mermaid
flowchart TD
    A[Startup_Script]-->B[Browser_UI]
    B-->C[Python_Backend_WSL2]
    C-->D[News_Fetcher]
    C-->E[Topic_Filter]
    C-->SummarizerSelector{{Summarizer_Selector}}
    SummarizerSelector-->|Local| FL[Local_Summarizer]
    SummarizerSelector-->|OpenAI| F1[OpenAI_Summarizer]
    SummarizerSelector-->|DeepSeek| F2[DeepSeek_Summarizer]
    SummarizerSelector-->|Groq| F3[Groq_Summarizer]
    FL-->G[Digest_Generator]
    F1-->G
    F2-->G
    F3-->G
    G-->H[HTML_or_Markdown_Digest]
    %% Optional frontend
    B-->I[Tauri_App]
```

---

- **Notes:**
  - The backend can be run as a Python script (WSL2) or bundled via PyInstaller for distribution.
  - The summarization engine routes to different providers based on config or API keys.
  - Optional: The Tauri App can replace or supplement the browser UI in later phases for a richer desktop experience.