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


def extract_json(cleaned_text: str) -> Dict[str, Any]:
    """Extracts dictionary object from a cleaned JSON string.

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
    try:
        data = json.loads(text)
        if not isinstance(data, dict):
            raise ValueError("Parsed JSON root is not an object/dict.")
        return data
    except Exception as e:
        raise ValueError(f"JSON syntax parsing error: {str(e)}")


def validate_analysis_schema(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Deep validation checking top-level keys, required sub-objects, and data types.

    Args:
        data: Candidate analysis JSON dictionary.

    Returns:
        Tuple of (is_valid: bool, error_message: str).
    """
    if not isinstance(data, dict):
        return False, "Root payload is not a JSON object."

    # 1. Verify required root keys
    missing_roots = [k for k in REQUIRED_ROOT_KEYS if k not in data]
    if missing_roots:
        return False, f"Missing required top-level keys: {', '.join(missing_roots)}"

    # 2. Verify nested object types
    scores = data.get("scores")
    if not isinstance(scores, dict) or "overall_resume_score" not in scores or "score_breakdown" not in scores:
        return False, "Invalid 'scores' structure or missing 'score_breakdown'."

    score_breakdown = scores.get("score_breakdown")
    if not isinstance(score_breakdown, dict):
        return False, "Invalid 'scores.score_breakdown' dict."

    opt_resume = data.get("optimized_resume")
    if not isinstance(opt_resume, dict) or "personal_information" not in opt_resume or "skills" not in opt_resume:
        return False, "Invalid 'optimized_resume' structure or missing 'skills'."

    skills = opt_resume.get("skills")
    if not isinstance(skills, dict):
        return False, "Invalid 'optimized_resume.skills' matrix dictionary."

    builder = data.get("builder")
    if not isinstance(builder, dict):
        return False, "Invalid 'builder' metadata dictionary."

    # 3. Verify key arrays
    if not isinstance(data.get("experience_analysis"), list):
        return False, "'experience_analysis' must be a list."
    if not isinstance(data.get("projects_analysis"), list):
        return False, "'projects_analysis' must be a list."
    if not isinstance(data.get("recommendations"), list):
        return False, "'recommendations' must be a list."

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
