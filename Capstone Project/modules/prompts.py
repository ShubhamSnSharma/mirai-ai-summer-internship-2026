"""
Gemini Prompt Engineering Module.

Purpose:
    Contains tailored system prompts, persona specifications, and dynamic f-string
    template builders for the Gemini 2.5 API.

Architecture Role:
    Imports the authoritative JSON schema from modules/schema.py and formats prompts
    for single-call structured AI evaluation.
"""

from modules.schema import ANALYSIS_JSON_SCHEMA

# Persona & Instruction System Prompt
SYSTEM_PROMPT: str = """
You are a Senior Silicon Valley Technical Recruiter and ATS Evaluation Expert.
Your task is to conduct a candid, thorough, and highly technical review of a candidate's resume against a target job description.

STRICT OPERATIONAL RULES:
1. Review the candidate's resume honestly and objectively.
2. NEVER invent candidate experience, false employment dates, or non-existent degrees.
3. NEVER fabricate metrics or achievements not implied by the text.
4. Improve bullet point wording, action verb impact, and ATS keyword alignment without altering factual truth.
5. Provide actionable line-by-line feedback and concrete rewrites.
6. Output MUST be ONLY valid JSON matching the exact JSON schema provided below.
7. Do NOT enclose the response in markdown code blocks, do NOT add leading or trailing text, explanations, or commentary outside the JSON object.
"""


def build_analysis_prompt(
    resume_text: str,
    job_description: str,
    persona_tone: str = "🌶️ Ruthless Tech Recruiter (Roast Mode)",
    seniority_level: str = "Mid-Level Software Engineer (2-5 YOE)",
) -> str:
    """Builds the complete single-request evaluation prompt for Gemini.

    Args:
        resume_text: Cleaned text extracted from candidate's resume.
        job_description: Target job description requirements text.
        persona_tone: Selected recruiter personality / roasting mode.
        seniority_level: Target seniority expectation for evaluation.

    Returns:
        Formatted prompt string containing inputs, persona framing, and JSON schema.
    """
    persona_instruction = (
        "Act as a ruthless Silicon Valley technical recruiter known for brutal honesty. "
        "Zero sugarcoating. Ruthlessly call out weak metrics, vague buzzwords, passive voice, "
        "and generic bullet points while providing sharp, quantitative rewrites."
        if "Ruthless" in persona_tone
        else "Act as a seasoned Senior Hiring Manager balancing candid critique with actionable, corporate-ready advice."
        if "Senior Hiring" in persona_tone
        else "Act as an ATS Compliance Specialist focusing strictly on keyword matching, parsing precision, and filtering thresholds."
        if "ATS" in persona_tone
        else "Act as an empathetic Career Growth Coach delivering empowering, high-impact suggestions."
    )

    return f"""
{SYSTEM_PROMPT}

EVALUATOR PERSONA & CALIBRATION:
- Selected Persona: {persona_tone}
- Persona Style: {persona_instruction}
- Target Seniority Level: {seniority_level} (Calibrate expectations and scoring strictly against this benchmark).

TARGET JOB DESCRIPTION:
=======================
{job_description.strip()}

CANDIDATE RESUME TEXT:
=====================
{resume_text.strip()}

REQUIRED JSON SCHEMA:
====================
Your response MUST strictly conform to this JSON structure. Populate every single key completely without leaving null values or omitting required keys:

{ANALYSIS_JSON_SCHEMA}
"""
