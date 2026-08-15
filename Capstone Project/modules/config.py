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
APP_NAME: str = "AI Resume Critic"
APP_SUBTITLE: str = "Recruiter-Grade Resume Analysis & Optimization Engine"
APP_DESCRIPTION: str = (
    "An enterprise platform that evaluates software engineering resumes against target job descriptions. "
    "Get recruiter-style feedback, line-by-line rewrite suggestions, ATS keyword gap analysis, and "
    "downloadable templates."
)
APP_VERSION: str = "1.0.0-phase4"
CAPSTONE_PROJECT_NAME: str = "MirAI Capstone Project — Problem Statement #17"

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

# Evaluation Matrix Scoring Weights (100 Points Total)
RUBRIC_SCORES: Dict[str, int] = {
    "technical_architecture": 25,
    "ai_integration_prompting": 20,
    "ui_ux_visualization": 20,
    "deployment_cloud": 15,
    "opensource_branding": 10,
    "system_design_docs": 10,
}

# Default Session State Schema Definitions
INITIAL_SESSION_STATE: Dict[str, Any] = {
    "resume_text": "",
    "job_description": "",
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
