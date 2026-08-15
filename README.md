# MirAI AI Summer Internship 2026 Submission Portfolio

**Student / Contributor:** Shubham Sharma  
**Repository:** `https://github.com/ShubhamSnSharma/mirai-ai-summer-internship-2026.git`  
**Stack:** Streamlit, Python 3.10+, Google Gemini 2.5 Flash, Plotly, ReportLab, Python-Docx  

---

## 📁 Repository Structure

```text
mirai-ai-summer-internship-2026/
├── Assignment 1/              # Python & Gemini API Foundations
├── Assignment 2/              # AI Multiverse Persona Chatbot
├── Assignment 3/              # AI Multiverse Upgraded UI
├── Assignment 4/              # AI Image Generator (Pollination API)
├── Assignment 5/              # StoryVerse Text-to-Speech & Story Generator
├── Assignment 6/              # AI Chatbot with Stateful Chat History
├── Assignment 7/              # ScreenSense AI Analytics Dashboard
└── Capstone Project/          # The AI Resume Critic (Recruiter Intelligence Workspace)
```

---

## 📚 Assignments Overview

### [Assignment 1](file:///Users/shubham/Documents/Mirai/Assignment%201/assignment1.py) — Python & Gemini API Foundations
* **Focus:** Initial API handshake with Google Gemini 2.5 Flash.
* **Key Features:** Synchronous model generation, API key environment management, basic prompt construction.

### [Assignment 2](file:///Users/shubham/Documents/Mirai/Assignment%202/assignment2.py) — AI Multiverse Chatbot
* **Focus:** Persona-driven interactive chatbots in Streamlit.
* **Key Features:** Selectable character personas (Hacker, Angry Shastri, Crazy Ronaldo Fan, Donald Trump).

### [Assignment 3](file:///Users/shubham/Documents/Mirai/Assignment%203/assignment3.py) — AI Multiverse Upgraded UI
* **Focus:** Enhanced Streamlit UI, sidebar controls, persona intensity sliders, layout refinements.

### [Assignment 4](file:///Users/shubham/Documents/Mirai/Assignment%204/assignment4.py) — AI Image Generator
* **Focus:** Multimodal generative AI integration.
* **Key Features:** Prompt enhancement, art style selection (Photorealistic, Anime, Vintage, Sketch), image generation via Pollinations API.

### [Assignment 5](file:///Users/shubham/Documents/Mirai/Assignment%205/assignment5.py) — StoryVerse TTS & Story Generator
* **Focus:** Voice synthesis & multi-chapter story generation.
* **Key Features:** Edge-TTS audio rendering, custom voice selection, downloadable MP3 audio files.

### [Assignment 6](file:///Users/shubham/Documents/Mirai/Assignment%206/assignment6.py) — AI Chatbot with Chat History
* **Focus:** Stateful conversational memory.
* **Key Features:** Session state history preservation, Streamlit `chat_message` and `chat_input` integration.

### [Assignment 7](file:///Users/shubham/Documents/Mirai/Assignment%207/assignment7.py) — ScreenSense AI Analytics Dashboard
* **Focus:** Data analytics, screen time tracking, and AI insights.
* **Key Features:** Pandas data processing, CSV telemetry generator, interactive metric cards, line charts.

---

## 🚀 Capstone Project — The AI Resume Critic

**Directory:** [`Capstone Project/`](file:///Users/shubham/Documents/Mirai/Capstone%20Project)  
**Live Application:** Recruiter-grade resume evaluation and optimization workspace powered by **Gemini 2.5 Flash**.

### Key Architectural Highlights
1. **Single-Call Gemini Pipeline:** Transmits candidate resume and job requirements once, returning a frozen 17-section structured JSON contract.
2. **5-Axis Visual Analytics:** Plotly radar chart, skill alignment confidence bar charts, and qualitative benchmark cards.
3. **Interactive Resume Studio:** 3 dedicated single-source-of-truth renderers (**ATS Professional**, **Modern Professional**, **Developer Specialist**) with instant live layout switching.
4. **Production Export Engine:** Compiles recruiter-grade **PDF** (ReportLab) and editable **DOCX** (Python-Docx) files matching the active layout, protected against XML special character crashes via `html.escape()`.

---

## 🛠️ Quick Start & Local Execution

### 1. Run Capstone Project
```bash
cd "Capstone Project"
pip install -r requirements.txt
streamlit run app.py
```

### 2. Run Any Assignment
```bash
python3 "Assignment 1/assignment1.py"
streamlit run "Assignment 7/assignment7.py"
```
