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
from datetime import datetime, timezone
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

    # 4. Initialize Gemini SDK Client & Execute with Fallback Cascade
    from modules.config import FALLBACK_GEMINI_MODELS

    client = genai.Client(api_key=key)
    config = types.GenerateContentConfig(
        temperature=DEFAULT_TEMPERATURE,
        max_output_tokens=MAX_OUTPUT_TOKENS,
        response_mime_type="application/json",
    )

    models_to_try = [DEFAULT_GEMINI_MODEL] + [m for m in FALLBACK_GEMINI_MODELS if m != DEFAULT_GEMINI_MODEL]
    raw_output = None
    last_error = None
    used_model = DEFAULT_GEMINI_MODEL

    for model_name in models_to_try:
        try:
            logger.info("Executing single-call Gemini API request with model: %s...", model_name)
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config,
            )
            raw_output = response.text if hasattr(response, "text") and response.text else str(response)
            if raw_output and raw_output.strip():
                used_model = model_name
                logger.info("Successfully received API response from %s (%d bytes).", model_name, len(raw_output))
                break
        except Exception as e:
            last_error = e
            logger.warning("Model %s failed with error: %s. Trying fallback model...", model_name, str(e))
            time.sleep(0.8)

    if not raw_output or not raw_output.strip():
        logger.exception("All Gemini model attempts failed. Last error: %s", str(last_error))
        err_msg = str(last_error) if last_error else "Empty response from Gemini API"
        if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
            raise ValueError("Google Gemini API rate limit / quota exceeded (HTTP 429). Please wait 10 seconds before retrying.")
        raise ValueError(f"Gemini API request failed: {err_msg}")

    # 5. Clean & Extract JSON with Self-Healing Normalization
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

    # Inject dynamic runtime timestamp and processing time metadata
    if "metadata" not in analysis_dict or not isinstance(analysis_dict["metadata"], dict):
        analysis_dict["metadata"] = {}
    
    analysis_dict["metadata"]["analysis_timestamp"] = datetime.now(timezone.utc).isoformat()
    analysis_dict["metadata"]["processing_time_seconds"] = elapsed_time
    analysis_dict["metadata"]["model"] = used_model

    return analysis_dict
