# System Architecture — AI Resume Critic & Career Optimizer

## Overview
The **AI Resume Critic** is a production-grade Streamlit application designed for B.Tech Capstone evaluation (Problem Statement #17). It processes candidate resumes alongside target job descriptions, leverages Google Gemini 2.5 API for recruiter-grade evaluation and roasts, visualizes quantitative ATS match metrics using Plotly, and exports optimized resume templates in PDF/DOCX formats.

---

## High-Level Architecture Diagram (Mermaid)

```mermaid
graph TD
    %% User Input Layer
    subgraph UI_Layer ["User Interface Layer (Streamlit App)"]
        A["User / Candidate"] -->|Uploads PDF/DOCX or Pastes Text| B["app.py (Main Entrypoint)"]
        B --> C["modules/ui.py (Layout Renderers)"]
        C --> D1["Resume Input Tab"]
        C --> D2["Recruiter Dashboard Tab"]
        C --> D3["Resume Optimizer Tab"]
        C --> D4["Template Gallery Tab"]
        C --> D5["Export & Download Tab"]
    end

    %% State & Configuration Layer
    subgraph State_Layer ["State & Config Management"]
        B <--> E["st.session_state (Explicit Schema)"]
        B <--> F["modules/config.py (Central Constants & Rubric)"]
    end

    %% Processing & Analysis Pipeline
    subgraph Processing_Layer ["Core Processing Modules"]
        D1 -->|Raw Files / Text| G["modules/resume_parser.py"]
        G -->|Cleaned Text| H["modules/scoring.py"]
        
        D1 -->|Trigger Analysis| I["modules/ai_engine.py"]
        I <-->|Prompt Templates| J["modules/prompts.py"]
        I <-->|Structured JSON Request| K["Google Gemini 2.5 API"]
        
        H & I -->|Scores & Insights| L["modules/visualizations.py"]
        L -->|Plotly Radar & KPI Cards| D2
    end

    %% Export & Generation Layer
    subgraph Export_Layer ["Export & Template Engine"]
        D5 -->|Select Template & Export| M["modules/resume_builder.py"]
        M <--> N1["templates/ats_professional.py"]
        M <--> N2["templates/modern_professional.py"]
        M <--> N3["templates/developer_professional.py"]
        M -->|Compile PDF / DOCX| O["output/ (Generated Documents)"]
    end
```

---

## Module Responsibilities

| Module | Responsibility |
| :--- | :--- |
| `app.py` | Configures Streamlit page, initializes session state, renders main UI container. |
| `modules/config.py` | Central configuration, theme colors, Gemini model parameters, and default state definitions. |
| `modules/ui.py` | Header, sidebar, footer, and tab navigation layout renderers. |
| `modules/resume_parser.py` | Extracts text and splits sections from PDF, DOCX, and TXT files. |
| `modules/prompts.py` | Tailored system prompts, dynamic recruiter personas, and JSON schemas for Gemini. |
| `modules/ai_engine.py` | Gemini API client wrapper, handling requests, retries, and structured JSON parsing. |
| `modules/scoring.py` | TF-IDF keyword frequency matching, ATS score weighting, and delta calculations. |
| `modules/visualizations.py` | Interactive Plotly radar charts, score gauges, and dynamic KPI cards. |
| `modules/resume_builder.py` | Compiles structured resume JSON into styled PDF (ReportLab) and DOCX files. |
| `templates/` | Modular layout templates (`ats_professional`, `modern_professional`, `developer_professional`). |
| `output/` | Temporary file storage directory for generated document exports. |
