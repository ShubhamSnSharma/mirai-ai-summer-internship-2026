"""
AI Engine Module (Google Gemini 2.5 API Integration).

Purpose:
    Handles authentication, prompt formatting, single-call LLM generation, response cleaning,
    deep JSON schema validation, and terminal logging for Gemini 2.5 Flash.

Architecture Role:
    Acts as the primary AI inference pipeline for candidate resume evaluation.
"""

import logging
import os
import time
from typing import Dict, Any, Optional
import streamlit as st

from google import genai
from google.genai import types

from modules.config import DEFAULT_GEMINI_MODEL, DEFAULT_TEMPERATURE, MAX_OUTPUT_TOKENS
from modules.prompts import build_analysis_prompt
from modules.helpers import clean_response, extract_json, validate_analysis_schema

# Initialize module logger for terminal diagnostics
logger = logging.getLogger("ai_engine")
logging.basicConfig(level=logging.INFO)


def resolve_api_key(passed_key: Optional[str] = None) -> Optional[str]:
    """Resolves Gemini API Key from explicit parameter, Streamlit secrets, or environment.

    Args:
        passed_key: Optional explicit API key string.

    Returns:
        API key string or None if unconfigured.
    """
    if passed_key:
        return passed_key.strip()
    
    # Check Streamlit Secrets
    try:
        if "GEMINI_API_KEY" in st.secrets:
            key = st.secrets["GEMINI_API_KEY"]
            if key and str(key).strip():
                return str(key).strip()
    except Exception:
        pass

    # Check Environment Variables
    env_key = os.environ.get("GEMINI_API_KEY", "")
    if env_key and env_key.strip():
        return env_key.strip()

    return None


def analyze_resume_with_gemini(
    resume_text: str,
    job_description: str,
    api_key: Optional[str] = None,
    persona_tone: str = "Ruthless Tech Recruiter (Roast Mode)",
    seniority_level: str = "Mid-Level Software Engineer (2-5 YOE)",
) -> Dict[str, Any]:
    """Executes single-call Gemini API evaluation and validates structured JSON output.

    Args:
        resume_text: Clean candidate resume text.
        job_description: Target job description requirements text.
        api_key: Optional explicit API key string.
        persona_tone: Selected recruiter personality mode.
        seniority_level: Target seniority expectation.

    Returns:
        Validated candidate analysis dictionary.

    Raises:
        ValueError: If input validation, API execution, or JSON schema validation fails.
    """
    start_time = time.time()

    # 1. Validate non-empty inputs
    if not resume_text or not resume_text.strip():
        logger.error("Input validation failed: Candidate resume text is empty.")
        raise ValueError("Candidate resume text cannot be empty.")
        
    if not job_description or not job_description.strip():
        logger.error("Input validation failed: Job description text is empty.")
        raise ValueError("Job description text cannot be empty.")

    # 2. Resolve API Key
    key = resolve_api_key(api_key)
    if not key:
        logger.error("API Key resolution failed: GEMINI_API_KEY not found in secrets or environment.")
        raise ValueError("Gemini API key is not configured. Please add GEMINI_API_KEY to st.secrets or environment variables.")

    # 3. Construct Prompt Payload
    logger.info("Constructing evaluation prompt for model: %s (Persona: %s)", DEFAULT_GEMINI_MODEL, persona_tone)
    prompt = build_analysis_prompt(
        resume_text=resume_text,
        job_description=job_description,
        persona_tone=persona_tone,
        seniority_level=seniority_level,
    )

    # 4. Initialize Gemini SDK Client
    try:
        client = genai.Client(api_key=key)
        config = types.GenerateContentConfig(
            temperature=DEFAULT_TEMPERATURE,
            max_output_tokens=MAX_OUTPUT_TOKENS,
            response_mime_type="application/json",
        )

        logger.info("Executing single-call Gemini 2.5 API request...")
        response = client.models.generate_content(
            model=DEFAULT_GEMINI_MODEL,
            contents=prompt,
            config=config,
        )

        raw_output = response.text if hasattr(response, "text") and response.text else str(response)
        logger.info("Received API response (%d bytes). Cleaning output...", len(raw_output))

    except Exception as e:
        logger.exception("Gemini API execution failed with error: %s", str(e))
        raise ValueError(f"Gemini API request failed: {str(e)}")

    # 5. Clean & Extract JSON
    cleaned_json_text = clean_response(raw_output)
    
    try:
        analysis_dict = extract_json(cleaned_json_text)
    except Exception as e:
        logger.error("JSON parsing error on cleaned response. Raw snippet: %s", raw_output[:300])
        raise ValueError(f"Failed to parse structured JSON from Gemini response: {str(e)}")

    # 6. Deep Schema Validation
    is_valid, err_msg = validate_analysis_schema(analysis_dict)
    if not is_valid:
        logger.error("JSON Schema validation failure: %s", err_msg)
        raise ValueError(f"Gemini JSON response failed schema contract validation: {err_msg}")

    elapsed_time = round(time.time() - start_time, 2)
    logger.info("Analysis completed and validated successfully in %.2f seconds.", elapsed_time)

    # Inject runtime processing time metadata
    if "metadata" in analysis_dict and isinstance(analysis_dict["metadata"], dict):
        analysis_dict["metadata"]["processing_time_seconds"] = elapsed_time

    return analysis_dict
