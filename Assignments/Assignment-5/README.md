# 📖 AI Multi-Modal Visual Novel

An interactive AI-powered **Visual Novel** built with **Streamlit**, **Google Gemini**, **Pollinations AI**, and **Microsoft Edge TTS**.

Users choose a story genre and art style, then experience a dynamically generated adventure featuring AI-written narration, AI-generated illustrations, and branching choices that shape the story.

---

## ✨ Features

- 🎭 Multiple story genres and artistic styles
- 🤖 AI-generated interactive storytelling with Google Gemini
- 🖼️ Scene-specific AI illustrations using Pollinations AI
- 🔊 AI narration powered by Microsoft Edge TTS
- 🎮 Branching choices that influence the story
- 📦 Structured JSON responses for reliable story generation
- 💾 Persistent conversations using Streamlit Session State
- ⚡ Cached Gemini client for improved performance
- 🛡️ Graceful error handling for API, image, and audio generation

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini API
- Pollinations AI
- Microsoft Edge TTS
- JSON
- Requests
- Asyncio
- python-dotenv

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone <repository-url>
cd Assignment-5
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```env
GEMINI_API_KEY=your_api_key_here
```

### Run the application

```bash
streamlit run assignment5.py
```

---

## 🎥 Demo

A demonstration video is available in the **demo/** folder.

---

## 📂 Project Structure

```text
Assignment-5/
│
├── assignment5.py      # Main Streamlit application
├── README.md
├── requirements.txt
└── demo/
    └── demo.mp4
```

---

## 🧠 AI Workflow

1. The user selects a story genre and art style.
2. Google Gemini generates the story, image prompt, and branching choices in structured JSON format.
3. Pollinations AI creates an illustration for the current scene.
4. Microsoft Edge TTS converts the narration into speech.
5. The user's choice is sent back to Gemini to continue the story while maintaining context.

---

## 📚 About the Project

This project was developed as **Assignment 5** for the **MirAI School of Technology – Virtual Summer Internship 2026**.

The project demonstrates:

- Prompt engineering for structured AI outputs
- JSON-based response parsing
- Multi-modal AI integration (Text + Image + Audio)
- Stateful application development with Streamlit
- Dynamic UI generation
- Robust exception handling
