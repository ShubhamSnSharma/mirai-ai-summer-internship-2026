# 🌌 The AI Multiverse

> Chat with iconic fictional personalities powered by Google Gemini — stay in character, every time.

---

## What It Does

**The AI Multiverse** is an interactive chatbot web app where you can have real conversations with AI-powered versions of famous characters. Pick a personality from the sidebar and start chatting — the AI stays fully in character throughout the conversation.

**Available characters:**
- 🟢 Master Yoda
- 🔴 Deadpool
- 🏴‍☠️ Captain Jack Sparrow
- 🎤 Stand-up Comedian
- 🕵️ Sherlock Holmes

The app remembers your full conversation history within a session, so responses feel natural and contextual. You can also clear the chat and start fresh anytime.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI & session state |
| [Google Gemini 2.5 Flash](https://ai.google.dev) | AI response generation |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | API key management |

---

## Getting Started

**1. Clone the repo and install dependencies:**
```bash
pip install streamlit google-genai python-dotenv
```

**2. Set up your API key:**

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

**3. Run the app:**
```bash
streamlit run assignment3.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## How It Works

1. Select a character from the **sidebar**
2. Type any message in the chat input
3. Gemini generates a response fully in character
4. Conversation history is preserved using `st.session_state`
5. Hit **Clear Conversation** to start fresh

---

*Built as part of the MirAI School of Technology — Virtual Summer Internship 2026.*
