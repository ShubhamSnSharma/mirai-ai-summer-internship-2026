# 📖 StoryVerse

> An AI-powered visual novel where every choice shapes the story — with generated artwork and voice narration.

---

## Demo

https://github.com/ShubhamSnSharma/mirai-ai-summer-internship-2026/raw/main/Assignment%205/demo.mov

---

## What It Does

**StoryVerse** is an immersive, interactive storytelling app that combines three AI-powered media types into a single experience — text, visuals, and audio — all driven by your choices.

**Key features:**
- 📖 **AI Story Generation** — Gemini 2.5 Flash writes cinematic, second-person narrative scenes in JSON format
- 🎨 **AI Artwork** — Pollinations.ai generates a scene illustration for every story beat
- 🔊 **Voice Narration** — Microsoft Edge TTS (Andrew Neural) reads each scene aloud
- 🎮 **Branching Choices** — 3 meaningful options per scene that genuinely change the story
- 🧠 **Persistent Chat Session** — Gemini remembers the full story context for consistent continuation
- ⚙️ **Configurable** — choose from 8 genres and 8 art styles before you begin

**Genres:** Dark Fantasy · Cyberpunk Thriller · Post-Apocalyptic Survival · Psychological Horror · Space Opera · Mythological Adventure · Detective Mystery · Time Travel

**Art Styles:** Anime · Cinematic Realism · Studio Ghibli · Comic Book · Pixel Art · Dark Gothic · Fantasy Concept Art · Oil Painting

---

## Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI, session state & media playback |
| [Google Gemini 2.5 Flash](https://ai.google.dev) | Story & image prompt generation (JSON output) |
| [Pollinations.ai](https://pollinations.ai) | Free AI image generation |
| [Edge TTS](https://pypi.org/project/edge-tts/) | Microsoft neural voice narration |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | API key management |
| [Requests](https://pypi.org/project/requests/) | HTTP calls to image API |

---

## Getting Started

**1. Install dependencies:**
```bash
pip install streamlit google-genai python-dotenv edge-tts requests
```

**2. Set up your API key:**

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

**3. Run the app:**
```bash
streamlit run assignment5.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## How It Works

1. Select a **genre** and **art style** from the sidebar
2. Click **🎮 Start New Story** to generate the opening scene
3. Gemini returns a structured JSON response with: story text, image prompt, and 3 choices
4. The app renders the **scene illustration**, **story text**, and **audio narration** simultaneously
5. Click any of the 3 **choice buttons** to continue — Gemini picks up exactly where it left off
6. The story keeps branching until you start a new one

---

*Built as part of the MirAI School of Technology — Virtual Summer Internship 2026.*
