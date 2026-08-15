# 🎨 AI Image Generator

> Type an idea, pick a style, and watch AI turn it into art — instantly.

---

## Demo

https://github.com/ShubhamSnSharma/mirai-ai-summer-internship-2026/raw/main/Assignment%204/demo.mov

---

## What It Does

**AI Image Generator** is a Streamlit web app that lets you generate images from text prompts using the [Pollinations.ai](https://pollinations.ai) API — no sign-up or API key required.

**Key features:**
- 🖊️ **Custom Prompt** — describe anything and generate an image from it
- 🎲 **Surprise Me!** — pick a random creative prompt and generate instantly
- 🎨 **Art Styles** — choose from Photorealistic, Anime, Vintage Victorian, or Sketch
- ✨ **Magic Enhance** — adds quality-boosting keywords for sharper, more dramatic results
- 📐 **Custom Dimensions** — control image width & height via sliders (256–1024px)
- 💾 **Download** — save the generated image directly to your device

---

## Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI & interactive widgets |
| [Pollinations.ai](https://pollinations.ai) | Free AI image generation API |
| [Requests](https://pypi.org/project/requests/) | HTTP requests to the image API |

---

## Getting Started

**1. Install dependencies:**
```bash
pip install streamlit requests
```

**2. Run the app:**
```bash
streamlit run assignment4.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## How It Works

1. Enter a prompt **or** hit **🎲 Surprise Me!** for a random idea
2. Choose an **art style** from the sidebar
3. Optionally enable **Magic Enhance** for higher quality output
4. Adjust **width & height** using the sliders
5. Click **Generate Image** — the app fetches your image from Pollinations.ai
6. **Download** the result as a `.png` file

---

*Built as part of the MirAI School of Technology — Virtual Summer Internship 2026.*
