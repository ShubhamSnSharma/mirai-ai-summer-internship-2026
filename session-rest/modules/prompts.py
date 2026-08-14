"""
Gemini Prompt Engineering Module.

Purpose:
    Contains tailored system prompts, dynamic f-string templates, and structured JSON
    schema specifications for the Gemini 2.5 API.

Architecture Role:
    Decouples raw prompt engineering from AI API execution code. Ensures strict,
    predictable recruiter persona roasts and structured output formatting.

TODO:
    - [ ] Define SYSTEM_PROMPT_RECRUITER_ROAST persona instructions.
    - [ ] Define JSON schema for structured resume breakdown response.
    - [ ] Build f-string template builders for dynamic context injection.
"""

from typing import Dict, Any

# TODO: Add dynamic prompt builder functions
def build_analysis_prompt(resume_text: str, job_description: str) -> str:
    """Builds the dynamic evaluation prompt combining resume and target job description.

    Args:
        resume_text: Cleaned text extracted from candidate's resume.
        job_description: Target job description text.

    Returns:
        Formatted prompt string.
    """
    # TODO: Implement prompt template logic
    raise NotImplementedError("Prompts module is in placeholder state.")
