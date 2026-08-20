"""
Configuration Module for AI Resume Critic & Career Optimizer.

Purpose:
    Centralized repository configuration, app metadata, constants, UI constants,
    model configuration, and initial state default values.

Architecture Role:
    Serves as the single source of truth for app constants across UI, AI Engine,
    Scoring, Visualizations, and Export modules.
"""

from typing import Dict, List, Any

# App Metadata
APP_NAME: str = "ResumeForge AI"
APP_SUBTITLE: str = "AI Resume Critic & Career Optimizer"
APP_DESCRIPTION: str = (
    "An enterprise platform that evaluates software engineering resumes against target job descriptions. "
    "Get recruiter-grade feedback, line-by-line rewrite suggestions, ATS keyword gap analysis, and "
    "downloadable templates."
)
APP_VERSION: str = "1.0.0-phase4"
CAPSTONE_PROJECT_NAME: str = "ResumeForge AI — MirAI Capstone Project (Problem Statement #17)"

# File Paths
SAMPLE_RESUME_PATH: str = "sample_data/sample_resume.txt"
SAMPLE_JOB_DESC_PATH: str = "sample_data/sample_job_description.txt"

# Gemini AI Model Configuration
DEFAULT_GEMINI_MODEL: str = "gemini-2.5-flash"
MAX_INPUT_CHARACTERS: int = 15000
DEFAULT_TEMPERATURE: float = 0.2
MAX_OUTPUT_TOKENS: int = 8192

# Supported Export Formats
SUPPORTED_EXPORTS: List[str] = ["PDF", "DOCX", "JSON"]
DEFAULT_TEMPLATE: str = "modern_professional"

# Evaluator Personas & Seniority Options (Problem Statement #17)
EVALUATOR_PERSONAS: List[str] = [
    "Ruthless Recruiter (Roast Mode)",
    "Hiring Manager (Balanced)",
    "ATS Specialist (Keywords)",
    "Career Coach (Friendly)",
]

SENIORITY_LEVELS: List[str] = [
    "Entry-Level (0-2 years)",
    "Mid-Level (2-5 years)",
    "Senior (5+ years)",
    "Lead / Manager",
]

# Development Checklist
PROGRESS_CHECKLIST: Dict[str, str] = {
    "Foundation": "Completed",
    "Input System": "Completed",
    "AI Engine": "Completed",
    "Dashboard": "Completed",
    "Resume Builder": "Completed",
    "Templates": "Completed",
    "Export": "Completed",
}

# MirAI Capstone Evaluation Matrix (100 Points Total)
RUBRIC_BREAKDOWN: List[Dict[str, Any]] = [
    {
        "category": "1. Technical Architecture",
        "points": 25,
        "desc": "Modular architecture, st.session_state memory persistence, st.form API batching, zero runtime errors.",
    },
    {
        "category": "2. AI Integration & Prompting",
        "points": 20,
        "desc": "Gemini 2.5 Flash API, system persona framing, single-call structured JSON contract, error boundaries.",
    },
    {
        "category": "3. UI/UX & Data Visualization",
        "points": 20,
        "desc": "Wide SaaS layout, dynamic KPI deltas, Plotly radar & skill charts, tabbed deep-dive workspaces.",
    },
    {
        "category": "4. Deployment & Cloud Prep",
        "points": 15,
        "desc": "Zero local dependencies in requirements.txt, Streamlit Cloud ready, environment secrets handling.",
    },
    {
        "category": "5. Open-Source Branding",
        "points": 10,
        "desc": "Terminal-style README.md, comprehensive setup guide, ASCII banner, and public repository structure.",
    },
    {
        "category": "6. System Design & Docs",
        "points": 10,
        "desc": "Mermaid data flow diagrams, technical design specifications, JSON data contract documentation.",
    },
]

# Default Session State Schema Definitions
INITIAL_SESSION_STATE: Dict[str, Any] = {
    "resume_text": "",
    "job_description": "",
    "evaluator_persona": EVALUATOR_PERSONAS[0],
    "target_seniority": SENIORITY_LEVELS[1],
    "analysis_complete": False,
    "analysis_json": None,
    "resume_scores": None,
    "structured_resume": None,
    "selected_template": DEFAULT_TEMPLATE,
    "generated_docx": None,
    "generated_pdf": None,
    "edited_resume": None,
    "parsed_dataframe": None,
    "gemini_response": None,
}
