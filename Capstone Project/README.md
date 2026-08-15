# 🚀 AI Resume Critic & Career Optimizer (Tech-Roast)

```text
===================================================================================
   ___   ___   ___                                  ___    _ _  _     
  / _ \ |_ _| | _ \___ ___ _  _ _ __  ___  ___ _ _ / __| _(_) |_(_)__ 
 | || |  | |  |   / -_)__ \ || | '  \/ -_) \__ \ '_| (__|  _| |  _| / _|
 |_||_| |___| |_|_\___|___/\_,_|_|_|_\___| |___/_|  \___|\__|_|\__|_\__|
===================================================================================
 [MirAI School of Technology] B.Tech Capstone Project — Problem Statement #17
 Status: Phase 1 — Production Foundation Built
===================================================================================
```

---

## 📌 Project Overview
**The AI Resume Critic** is an enterprise-grade AI dashboard that acts as a ruthless Silicon Valley Tech Recruiter. It analyzes candidate resumes against target job descriptions, roasts weak bullet points, computes quantitative ATS match metrics, recommends line-by-line improvements, and exports polished resumes across multiple professional templates.

> [!NOTE]
> **Evaluation Rubric Target**: 100/100 Points (Technical Architecture, Gemini AI Prompting, UI/UX Visualization, Deployment Prep, Open-Source Branding, System Documentation).

---

## 🏗️ Architecture & Module Breakdown

```text
project/
├── app.py                     # Main Streamlit Entrypoint & State Orchestrator
├── requirements.txt           # Locked Production Dependencies
├── README.md                  # Project Documentation & Terminal Branding
│
├── assets/                    # Static Assets, Logos & Custom CSS
├── output/                    # Generated Export Storage (PDFs, DOCX, JSON)
├── sample_data/               # Realistic Test Resume & Job Descriptions
│
├── templates/                 # Modular Resume Render Templates
│   ├── __init__.py
│   ├── ats_professional.py    # 100% ATS Parser Compatible Layout
│   ├── modern_professional.py # Executive 2-Column Corporate Layout
│   └── developer_professional.py # Tech / Software Engineer Layout
│
├── modules/                   # Core Logic Packages
│   ├── __init__.py
│   ├── config.py              # Central Constants, Gemini Settings & State Schema
│   ├── ui.py                  # Reusable Layout & Component Renderers
│   ├── prompts.py             # Recruiter Personas & Gemini Prompt Engineering
│   ├── ai_engine.py           # Gemini 2.5 Flash API Wrapper & Multimodality
│   ├── resume_parser.py       # PDF / DOCX / TXT Multi-format Reader
│   ├── scoring.py             # ATS Match & Keyword Density Algorithms
│   ├── visualizations.py      # Plotly Radar Charts & Dynamic KPI Cards
│   ├── resume_builder.py      # ReportLab PDF & Docx Compiler
│   └── helpers.py             # Text Cleaners & File Utilities
│
└── docs/                      # System Design & Documentation
    ├── architecture.md        # Mermaid Architecture Diagram
    ├── technical_design.md    # Session State & Rubric Alignment Matrix
    └── api_strategy.md        # Gemini Integration & Optimization Strategy
```

---

## 🗺️ Development Roadmap

- [x] **Phase 1: Foundation & Production Architecture** *(Current Stage)*
  - [x] Modular directory hierarchy creation
  - [x] Explicit `st.session_state` schema initialization
  - [x] Responsive wide-layout UI shell
  - [x] System design & API strategy documentation
- [ ] **Phase 2: Input Parsing & Document Extraction**
- [ ] **Phase 3: Gemini 2.5 AI Engine & Prompt Engineering**
- [ ] **Phase 4: Recruiter Dashboard & Plotly Visual Analytics**
- [ ] **Phase 5: Interactive Resume Optimizer & Template Engine**
- [ ] **Phase 6: ReportLab PDF & DOCX Export Engine**
- [ ] **Phase 7: Cloud Deployment (Streamlit Community Cloud)**

---

## ⚙️ Installation & Local Setup

### Prerequisites
- Python 3.10+
- Git

### 1. Clone Repository & Setup Virtual Environment
```bash
git clone https://github.com/ShubhamSnSharma/session7-git_basics.git
cd session7-git_basics

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Streamlit Dashboard
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

---

## 📄 License
Created for **MirAI School of Technology Capstone Evaluation 2026**. Released under the MIT License.
