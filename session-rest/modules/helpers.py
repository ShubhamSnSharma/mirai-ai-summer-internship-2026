"""
Helper Utilities Module.

Purpose:
    Provides general utility functions for string cleaning, word/character counting,
    file I/O operations, mock data loading, and JSON schema validation.

Architecture Role:
    Contains stateless helper functions used across UI, state management, and data contract validation.
"""

import json
import os
from typing import Any, Dict, Optional

# Expected top-level keys for schema validation
REQUIRED_SCHEMA_KEYS = [
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


def load_sample_file(file_path: str) -> str:
    """Loads text content from a local sample data file safely.

    Args:
        file_path: Relative or absolute path to sample text file.

    Returns:
        Extracted text content or empty string if error occurs.
    """
    if not os.path.exists(file_path):
        return ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""


def load_mock_analysis(file_path: str = "data/mock_analysis.json") -> Dict[str, Any]:
    """Loads the official mock analysis JSON payload from the data directory.

    Args:
        file_path: Path to mock JSON analysis file.

    Returns:
        Parsed JSON dictionary.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Mock analysis file not found at path: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_analysis_schema(data: Dict[str, Any]) -> bool:
    """Validates that a dictionary conforms to the required top-level analysis JSON contract.

    Args:
        data: Candidate analysis JSON dictionary.

    Returns:
        True if all required top-level keys exist, False otherwise.
    """
    if not isinstance(data, dict):
        return False
    return all(key in data for key in REQUIRED_SCHEMA_KEYS)


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
