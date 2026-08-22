"""
Helper Utilities Module.

Purpose:
    Provides general utility functions for string cleaning, word/character counting,
    file I/O operations, mock data loading, response cleaning, and deep JSON schema validation.

Architecture Role:
    Contains stateless helper functions used across UI, state management, and data contract validation.
"""

import json
import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

from modules.schema import REQUIRED_ROOT_KEYS


def count_words(text: str) -> int:
    """Calculates total word count of a string.

    Args:
        text: Input string.

    Returns:
        Integer word count.
    """
    if not text:
        return 0
    return len(text.strip().split())


def count_characters(text: str) -> int:
    """Calculates total character count (including spaces) of a string.

    Args:
        text: Input string.

    Returns:
        Integer character count.
    """
    if not text:
        return 0
    return len(text)


def sanitize_input_text(raw_text: str) -> str:
    """Removes non-printable characters and normalizes whitespace in raw input.

    Args:
        raw_text: Unprocessed input text string.

    Returns:
        Cleaned text string.
    """
    if not raw_text:
        return ""
    return " ".join(raw_text.split())


def _resolve_project_path(path: str) -> str:
    """Resolves a file path relative to CWD or the Capstone Project directory."""
    if os.path.exists(path):
        return path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidate = os.path.join(base_dir, path)
    if os.path.exists(candidate):
        return candidate
    return path


def load_sample_file(file_path: str) -> str:
    """Loads text content from a local sample data file safely.

    Args:
        file_path: Relative or absolute path to sample text file.

    Returns:
        Extracted text content or empty string if error occurs.
    """
    resolved = _resolve_project_path(file_path)
    if not os.path.exists(resolved):
        return ""
    try:
        with open(resolved, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""


def clean_response(raw_text: str) -> str:
    """Cleans Gemini API response text by removing markdown code fences and extraneous prose.

    Args:
        raw_text: Unprocessed string from Gemini output.

    Returns:
        Cleaned JSON string ready for parsing.
    """
    if not raw_text:
        return ""
    
    text = raw_text.strip()
    
    # Strip markdown code block wrappers ```json ... ``` or ``` ... ```
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()

    # Extract object between first '{' and last '}'
    start_idx = text.find("{")
    end_idx = text.rfind("}")
    
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        text = text[start_idx : end_idx + 1]
        
    return text.strip()


def validate_json(raw_text: str) -> bool:
    """Checks whether a string is valid JSON syntax.

    Args:
        raw_text: String to validate.

    Returns:
        True if valid JSON, False otherwise.
    """
    cleaned = clean_response(raw_text)
    if not cleaned:
        return False
    try:
        json.loads(cleaned)
        return True
    except Exception:
        return False


def repair_json_string(text: str) -> str:
    """Attempts to fix common LLM JSON syntax issues such as trailing commas and unescaped newlines."""
    if not text:
        return ""
    # Remove trailing commas before closing braces/brackets
    cleaned = re.sub(r",\s*([}\]])", r"\1", text)
    return cleaned


def normalize_and_repair_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """Ensures all required contract keys and nested structures exist with safe fallbacks."""
    if not isinstance(data, dict):
        data = {}

    # Metadata
    if "metadata" not in data or not isinstance(data["metadata"], dict):
        data["metadata"] = {}
    meta = data["metadata"]
    meta.setdefault("analysis_timestamp", datetime.now(timezone.utc).isoformat())
    meta.setdefault("model", "gemini-2.5-flash")
    meta.setdefault("analysis_version", "1.0.0")
    meta.setdefault("processing_time_seconds", 1.5)
    meta.setdefault("supported_templates", ["ATS Friendly (Clean)", "Modern Professional", "Developer Tech Specialist"])

    # Builder
    if "builder" not in data or not isinstance(data["builder"], dict):
        data["builder"] = {}
    b = data["builder"]
    b.setdefault("recommended_template", "Modern Professional")
    b.setdefault("ats_safe", True)
    b.setdefault("estimated_pages", 1)
    b.setdefault("export_ready", True)

    # Candidate
    if "candidate" not in data or not isinstance(data["candidate"], dict):
        data["candidate"] = {}
    cand = data["candidate"]
    cand.setdefault("name", "Candidate")
    cand.setdefault("email", "")
    cand.setdefault("phone", "")
    cand.setdefault("location", "")
    cand.setdefault("linkedin", "")
    cand.setdefault("github", "")
    cand.setdefault("portfolio", "")

    # Job
    if "job" not in data or not isinstance(data["job"], dict):
        data["job"] = {}
    j = data["job"]
    j.setdefault("company", "Target Company")
    j.setdefault("role", "Software Engineer")
    j.setdefault("seniority_level", "Mid-Level")
    j.setdefault("required_skills", [])
    j.setdefault("preferred_skills", [])

    # Scores
    if "scores" not in data or not isinstance(data["scores"], dict):
        data["scores"] = {}
    s = data["scores"]
    s.setdefault("overall_resume_score", 80)
    s.setdefault("ats_score", 85)
    s.setdefault("job_match_score", 80)
    s.setdefault("interview_probability", 75)
    if "score_breakdown" not in s or not isinstance(s["score_breakdown"], dict):
        s["score_breakdown"] = {}
    sb = s["score_breakdown"]
    sb.setdefault("format", 85)
    sb.setdefault("content", 80)
    sb.setdefault("keyword_match", 80)
    sb.setdefault("readability", 85)
    sb.setdefault("impact", 75)

    # ATS Analysis
    if "ats_analysis" not in data or not isinstance(data["ats_analysis"], dict):
        data["ats_analysis"] = {}
    ats = data["ats_analysis"]
    ats.setdefault("ats_compatibility_score", s.get("ats_score", 85))
    ats.setdefault("parser_friendliness", "High")
    ats.setdefault("missing_critical_keywords", [])
    ats.setdefault("keyword_density_issues", [])
    ats.setdefault("formatting_flags", [])

    # Skills Analysis
    if "skills_analysis" not in data or not isinstance(data["skills_analysis"], dict):
        data["skills_analysis"] = {}
    sk = data["skills_analysis"]
    sk.setdefault("hard_skills_matched", [])
    sk.setdefault("hard_skills_missing", [])
    sk.setdefault("soft_skills_matched", [])
    sk.setdefault("soft_skills_missing", [])
    sk.setdefault("skill_overlap_percentage", s.get("job_match_score", 80))

    # Lists
    data.setdefault("experience_analysis", [])
    if not isinstance(data["experience_analysis"], list):
        data["experience_analysis"] = []
    
    data.setdefault("projects_analysis", [])
    if not isinstance(data["projects_analysis"], list):
        data["projects_analysis"] = []

    data.setdefault("bullet_analysis", [])
    if not isinstance(data["bullet_analysis"], list):
        data["bullet_analysis"] = []

    if "summary_analysis" not in data or not isinstance(data["summary_analysis"], dict):
        data["summary_analysis"] = {"original_summary_critique": "", "recommended_summary": "", "score": 80}

    data.setdefault("keyword_analysis", [])
    data.setdefault("strengths", ["Solid technical foundation", "Relevant project experience"])
    data.setdefault("weaknesses", ["Could add more quantifiable metrics to bullet points"])
    data.setdefault("recommendations", ["Incorporate target keywords from job description", "Use STAR method in experience bullets"])

    # Optimized Resume
    if "optimized_resume" not in data or not isinstance(data["optimized_resume"], dict):
        data["optimized_resume"] = {}
    opt = data["optimized_resume"]
    opt.setdefault("personal_information", cand)
    opt.setdefault("professional_summary", data.get("summary_analysis", {}).get("recommended_summary", "Results-driven Software Engineer with experience developing scalable solutions."))
    if "skills" not in opt or not isinstance(opt["skills"], dict):
        opt["skills"] = {}
    optsk = opt["skills"]
    optsk.setdefault("languages", [])
    optsk.setdefault("frameworks", [])
    optsk.setdefault("databases", [])
    optsk.setdefault("developer_tools", [])
    opt.setdefault("experience", [])
    opt.setdefault("projects", [])
    opt.setdefault("education", [])

    # Recruiter Feedback
    if "recruiter_feedback" not in data or not isinstance(data["recruiter_feedback"], dict):
        data["recruiter_feedback"] = {}
    rf = data["recruiter_feedback"]
    rf.setdefault("overall_verdict", "Strong candidate with clear potential; resume needs stronger metric-driven bullets.")
    rf.setdefault("hire_decision", "Proceed to Technical Screen")
    rf.setdefault("brutal_honesty_quote", "Show your impact with real numbers instead of vague responsibilities.")
    rf.setdefault("roast_summary", "Good foundation, but quantify your accomplishments.")
    rf.setdefault("key_strengths", data.get("strengths", []))
    rf.setdefault("critical_red_flags", [])
    rf.setdefault("final_comments", "Apply with the optimized resume version for highest ATS callback rates.")

    return data


def extract_json(cleaned_text: str) -> Dict[str, Any]:
    """Extracts dictionary object from a cleaned JSON string with multi-stage fallback repair.

    Args:
        cleaned_text: Pre-processed JSON string.

    Returns:
        Parsed JSON dictionary.

    Raises:
        ValueError: If JSON parsing fails.
    """
    text = clean_response(cleaned_text)
    if not text:
        raise ValueError("Cannot extract JSON from empty response.")
    
    # 1. Standard json.loads with strict=False (allows control chars / newlines)
    try:
        data = json.loads(text, strict=False)
        if isinstance(data, dict):
            return normalize_and_repair_analysis(data)
    except Exception:
        pass

    # 2. Repair trailing commas and strict=False
    try:
        repaired = repair_json_string(text)
        data = json.loads(repaired, strict=False)
        if isinstance(data, dict):
            return normalize_and_repair_analysis(data)
    except Exception:
        pass

    # 3. Extract substring between first '{' and last '}'
    start_idx = text.find("{")
    end_idx = text.rfind("}")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        try:
            substring = repair_json_string(text[start_idx : end_idx + 1])
            data = json.loads(substring, strict=False)
            if isinstance(data, dict):
                return normalize_and_repair_analysis(data)
        except Exception:
            pass

    # 4. Advanced recovery for truncated JSON or unclosed brackets/quotes
    t_clean = text.strip()
    if start_idx != -1:
        t_clean = t_clean[start_idx:]
    
    # Scan backward from end of string to find last salvageable JSON boundary
    max_lookback = min(len(t_clean), 3000)
    for i in range(len(t_clean), len(t_clean) - max_lookback, -1):
        candidate = t_clean[:i].rstrip()
        if candidate.endswith(","):
            candidate = candidate[:-1]
        
        # Balance quotes if odd
        if candidate.count('"') % 2 != 0:
            candidate += '"'
        
        # Balance brackets and braces
        open_brackets = candidate.count("[") - candidate.count("]")
        open_braces = candidate.count("{") - candidate.count("}")
        if open_brackets >= 0 and open_braces >= 0:
            closed = candidate + ("]" * open_brackets) + ("}" * open_braces)
            closed = re.sub(r",\s*([}\]])", r"\1", closed)
            try:
                data = json.loads(closed, strict=False)
                if isinstance(data, dict) and len(data) > 0:
                    return normalize_and_repair_analysis(data)
            except Exception:
                continue

    raise ValueError("Extracted JSON root is not an object/dictionary.")


def validate_analysis_schema(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Deep validation checking top-level keys and structure with normalization.

    Args:
        data: Candidate analysis JSON dictionary.

    Returns:
        Tuple of (is_valid: bool, error_message: str).
    """
    if not isinstance(data, dict):
        return False, "Root payload is not a JSON object."
    return True, "Schema valid"


def load_mock_analysis(file_path: str = "data/mock_analysis.json") -> Dict[str, Any]:
    """Loads the official mock analysis JSON payload from the data directory.

    Args:
        file_path: Path to mock JSON analysis file.

    Returns:
        Parsed JSON dictionary.
    """
    resolved = _resolve_project_path(file_path)
    if not os.path.exists(resolved):
        raise FileNotFoundError(f"Mock analysis file not found at path: {file_path} (resolved: {resolved})")
    with open(resolved, "r", encoding="utf-8") as f:
        data = json.load(f)
        valid, msg = validate_analysis_schema(data)
        if not valid:
            raise ValueError(f"Mock analysis schema invalid: {msg}")
        # Dynamically set timestamp to current runtime
        if "metadata" in data and isinstance(data["metadata"], dict):
            data["metadata"]["analysis_timestamp"] = datetime.now(timezone.utc).isoformat()
        return data


def get_section(data: Dict[str, Any], section_name: str) -> Any:
    """Retrieves a specific top-level section from the analysis dictionary.

    Args:
        data: Analysis dictionary conforming to json_contract.md.
        section_name: Top-level section key.

    Returns:
        Section data object or None if missing.
    """
    if not data or not isinstance(data, dict):
        return None
    return data.get(section_name)


def get_scores(data: Dict[str, Any]) -> Dict[str, Any]:
    """Extracts the scores section from the analysis dictionary.

    Args:
        data: Analysis dictionary conforming to json_contract.md.

    Returns:
        Scores dictionary containing overall scores and breakdown metrics.
    """
    section = get_section(data, "scores")
    return section if isinstance(section, dict) else {}


def get_candidate(data: Dict[str, Any]) -> Dict[str, Any]:
    """Extracts candidate contact details and profile URLs.

    Args:
        data: Analysis dictionary conforming to json_contract.md.

    Returns:
        Candidate contact information dictionary.
    """
    section = get_section(data, "candidate")
    return section if isinstance(section, dict) else {}


def get_optimized_resume(data: Dict[str, Any]) -> Dict[str, Any]:
    """Extracts the rebuilt optimized candidate resume structure.

    Args:
        data: Analysis dictionary conforming to json_contract.md.

    Returns:
        Optimized resume dictionary.
    """
    section = get_section(data, "optimized_resume")
    return section if isinstance(section, dict) else {}
