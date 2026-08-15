"""
Authoritative Schema Specification Module.

Purpose:
    Contains the single authoritative JSON schema definition for candidate resume analysis.

Architecture Role:
    Single source of truth imported by prompts.py (for LLM instructions) and helpers.py (for deep validation).
"""

from typing import Dict, Any

# Top-level required keys
REQUIRED_ROOT_KEYS = [
    "metadata",
    "builder",
    "candidate",
    "job",
    "scores",
    "ats_analysis",
    "skills_analysis",
    "experience_analysis",
    "projects_analysis",
    "bullet_analysis",
    "summary_analysis",
    "keyword_analysis",
    "strengths",
    "weaknesses",
    "recommendations",
    "optimized_resume",
    "recruiter_feedback",
]

# JSON schema string used directly inside Gemini system prompts
ANALYSIS_JSON_SCHEMA: str = """
{
  "metadata": {
    "analysis_timestamp": "string (ISO-8601)",
    "model": "string",
    "analysis_version": "string",
    "processing_time_seconds": "number",
    "supported_templates": ["string"]
  },
  "builder": {
    "recommended_template": "string",
    "ats_safe": "boolean",
    "estimated_pages": "number",
    "export_ready": "boolean"
  },
  "candidate": {
    "name": "string",
    "email": "string",
    "phone": "string",
    "location": "string",
    "linkedin": "string",
    "github": "string",
    "portfolio": "string"
  },
  "job": {
    "company": "string",
    "role": "string",
    "industry": "string",
    "experience_required": "string",
    "education_required": "string",
    "primary_skills": ["string"],
    "secondary_skills": ["string"]
  },
  "scores": {
    "overall_resume_score": "number (0-100)",
    "ats_score": "number (0-100)",
    "job_match_score": "number (0-100)",
    "interview_probability": "number (0-100)",
    "skills_score": "number (0-100)",
    "experience_score": "number (0-100)",
    "projects_score": "number (0-100)",
    "education_score": "number (0-100)",
    "score_breakdown": {
      "content": "number (0-100)",
      "format": "number (0-100)",
      "impact": "number (0-100)",
      "readability": "number (0-100)",
      "keyword_match": "number (0-100)"
    }
  },
  "ats_analysis": {
    "format_score": "number",
    "readability_score": "number",
    "keyword_density": "number",
    "parsing_risk": "string (Low|Medium|High)",
    "missing_sections": ["string"],
    "ats_issues": ["string"]
  },
  "skills_analysis": {
    "matched_skills": [{"skill": "string", "confidence": "number (0-100)"}],
    "missing_skills": [{"skill": "string", "confidence": "number (0-100)"}],
    "recommended_skills": ["string"],
    "soft_skills_found": ["string"],
    "soft_skills_missing": ["string"]
  },
  "experience_analysis": [
    {
      "company": "string",
      "role": "string",
      "strengths": ["string"],
      "issues": ["string"],
      "improved_description": "string"
    }
  ],
  "projects_analysis": [
    {
      "project_name": "string",
      "strengths": ["string"],
      "missing_metrics": ["string"],
      "missing_technologies": ["string"],
      "improved_description": "string"
    }
  ],
  "bullet_analysis": [
    {
      "section": "string",
      "original": "string",
      "issue": "string",
      "improved": "string",
      "reason": "string"
    }
  ],
  "summary_analysis": {
    "original_summary": "string",
    "issues": "string",
    "improved_summary": "string"
  },
  "keyword_analysis": {
    "matched_keywords": ["string"],
    "missing_keywords": ["string"],
    "high_priority_keywords": ["string"],
    "low_priority_keywords": ["string"]
  },
  "strengths": ["string"],
  "weaknesses": ["string"],
  "recommendations": [
    {
      "severity": "string (Critical|High|Medium|Low)",
      "priority": "number",
      "category": "string",
      "title": "string",
      "description": "string"
    }
  ],
  "optimized_resume": {
    "personal_information": {
      "name": "string",
      "email": "string",
      "phone": "string",
      "location": "string",
      "linkedin": "string",
      "github": "string",
      "portfolio": "string"
    },
    "headline": "string",
    "professional_summary": "string",
    "experience": [
      {
        "company": "string",
        "location": "string",
        "role": "string",
        "start_date": "string",
        "end_date": "string",
        "bullets": ["string"]
      }
    ],
    "projects": [
      {
        "project_name": "string",
        "tech_stack": ["string"],
        "description": "string"
      }
    ],
    "education": [
      {
        "degree": "string",
        "institution": "string",
        "location": "string",
        "graduation_date": "string",
        "gpa": "string"
      }
    ],
    "skills": {
      "languages": ["string"],
      "frameworks": ["string"],
      "databases": ["string"],
      "tools": ["string"],
      "cloud": ["string"],
      "other": ["string"]
    },
    "certifications": ["string"],
    "achievements": ["string"],
    "languages_spoken": ["string"],
    "interests": ["string"]
  },
  "recruiter_feedback": {
    "overall_verdict": "string",
    "hire_decision": "string",
    "top_concerns": ["string"],
    "final_comments": "string"
  }
}
"""
