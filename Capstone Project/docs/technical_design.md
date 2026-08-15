# Technical Design Document — AI Resume Critic

## 1. Executive Summary
The **AI Resume Critic (Tech-Roast)** addresses MirAI Capstone Problem Statement #17. It evaluates technical resumes against target job descriptions, providing recruiters' candid feedback, actionable line-by-line rewrite suggestions, ATS keyword gap analysis, and automated formatted document generation.

---

## 2. Application Data Flow & Unified JSON Contract

The entire application relies on a **single source of truth** data pipeline. Raw user inputs are sent to Google Gemini 2.5 Flash, which returns a structured JSON payload conforming strictly to `docs/json_contract.md`. Every downstream UI module, visualization engine, resume builder, template renderer, and document exporter consumes this identical JSON schema without duplicate data transformation or secondary AI calls.

```text
  [ User Resume Input ] + [ Target Job Description ]
                         │
                         ▼
        [ Google Gemini 2.5 API (gemini-2.5-flash) ]
                         │
                         ▼
         [ Unified Analysis JSON Data Contract ]
                         │
  ┌──────────────────────┼──────────────────────┬──────────────────────┐
  ▼                      ▼                      ▼                      ▼
[ Recruiter Dashboard ] [ Resume Optimizer ]   [ Template Engine ]  [ PDF/DOCX Export ]
 (Plotly Radar, KPIs,    (Line-by-line diff,    (ATS, Modern & Dev   (ReportLab & Docx
  Recruiter Roasts)       Keyword gap editor)    Layout Builders)     File Compilers)
```

---

## 3. Session State Design & Explicit Schema
To prevent memory leaks and unexpected reruns in Streamlit, all state objects are explicitly initialized at launch:

```python
st.session_state = {
    "resume_text": str,           # Raw extracted text from uploaded/pasted resume
    "job_description": str,       # Raw target job description text
    "analysis_complete": bool,     # Trigger flag for dashboard visibility
    "analysis_json": dict | None,  # Unified JSON object conforming to json_contract.md
    "resume_scores": dict | None, # Quantitative ATS scores & breakdown dict
    "structured_resume": dict,     # Structured JSON representation of candidate resume
    "selected_template": str,     # Template choice ('Modern Professional', etc.)
    "generated_docx": bytes,       # Compiled DOCX file bytes
    "generated_pdf": bytes,        # Compiled PDF file bytes
    "edited_resume": dict | None,  # User-edited resume draft
    "parsed_dataframe": DataFrame, # Pandas DataFrame for keyword gap editor
    "gemini_response": str | None  # Raw string response backup from Gemini API
}
```

---

## 4. Evaluation Rubric Alignment Matrix

| Rubric Category | Max Points | Technical Implementation Strategy |
| :--- | :--- | :--- |
| **1. Technical Implementation & Architecture** | 25 | Modular package layout (`modules/`), strict `st.session_state` management, `st.form` batching to prevent API call waste, zero terminal errors. |
| **2. AI Integration & Prompt Engineering** | 20 | Google Gemini 2.5 Flash API, custom system prompts, dynamic f-string context, structured JSON schema outputs. |
| **3. UI/UX & Data Visualization** | 20 | Custom CSS theme, wide column layouts, dynamic `st.metric` cards with deltas, interactive `st.data_editor`, Plotly radar charts. |
| **4. Deployment & Cloud Engineering** | 15 | Clean `requirements.txt` with locked major versions, `st.secrets` key protection, Streamlit Cloud compatibility. |
| **5. Open-Source Branding** | 10 | Terminal-style `README.md` with setup guide, live deployment link, and architecture specs. |
| **6. System Design & Documentation** | 10 | Dedicated `docs/` folder containing `architecture.md` (Mermaid diagram), `technical_design.md`, `api_strategy.md`, and `json_contract.md`. |
