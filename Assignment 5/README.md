# Assignment 5 — The Multi-Modal Visual Novel

**Track:** MirAI School of Technology — Virtual Summer Internship 2026 (AI Builder)  
**Deadline:** August 25, 2026, 11:59 PM  

---

## Objective

Build a "Choose Your Own Adventure" Visual Novel Engine combining stateful text generation (Gemini), visual asset generation (Pollinations), and audio narration (TTS) in a single Streamlit application.

---

## Architecture

```
User Input
    │
    ▼
Gemini API (Structured JSON Response)
    │
    ├──► story_text  ──► Edge TTS ──► st.audio() narration
    ├──► image_prompt ──► Pollinations API ──► st.image()
    └──► options []  ──► Dynamic st.button() per choice
```

---

## Tasks Completed

### Phase 1 — The Director's Cut (UI & Configuration)
- `@st.cache_resource` caches the Gemini client securely.
- Sidebar with **Story Genre** and **Art Style** dropdowns.
- `st.session_state` stores chat history and the Gemini chat object.

### Phase 2 — Structured JSON Engine
- System prompt instructs Gemini to return strict JSON with three keys:
  - `story_text` — narrative paragraph
  - `image_prompt` — engineered prompt for image generation
  - `options` — list of 2–3 player choices
- `import json` used to parse AI string response into a Python dictionary.

### Phase 3 — Dynamic UI Generation
- `for` loop iterates over the `options` list from parsed JSON.
- Each option dynamically generates an `st.button()`.
- Clicking a button sends that choice back to Gemini as the next move.

### Phase 4 — Multi-Media Rendering & TTS
- **Image:** `image_prompt` sent to Pollinations API; rendered with `st.image()`.
- **Audio:** `story_text` converted to MP3 narration using `edge-tts`; played with `st.audio()`.

### Phase 5 — Graceful Failures
- `try/except` blocks wrap all API calls.
- If image generation fails: `st.toast("Image server is busy, skipping visual...")` — story continues uninterrupted.

---

## Tech Stack
- Python
- Streamlit
- Google Gemini API (`google-genai`)
- Pollinations AI (Image Generation)
- edge-tts (Text-to-Speech)
- json (stdlib)
- python-dotenv

---

## Run Locally

```bash
pip install streamlit google-genai edge-tts requests python-dotenv
# Create a .env file with: GEMINI_API_KEY=your_key_here
streamlit run assignment5.py
```

---

*Built as part of the MirAI School of Technology Virtual Summer Internship 2026.*
