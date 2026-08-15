"""
ResumeForge AI — AI Resume Critic & Career Optimizer.

B.Tech Capstone Project — MirAI School of Technology (Problem Statement #17)

Architecture Note:
    Phase 4: Gemini AI Engine & JSON Pipeline Integration.
    Connects single-call Google Gemini 2.5 Flash API to generate structured candidate evaluation JSON.
    Consumes unified JSON data contract (data/mock_analysis.json) as fallback or live output.
"""

import streamlit as st

# Import Modules
from modules.config import (
    APP_NAME,
    INITIAL_SESSION_STATE,
    SAMPLE_RESUME_PATH,
    SAMPLE_JOB_DESC_PATH,
    PROGRESS_CHECKLIST,
)
from modules.helpers import load_sample_file, load_mock_analysis, validate_analysis_schema
from modules.ai_engine import analyze_resume_with_gemini, resolve_api_key
from modules.ui import (
    apply_lightweight_custom_css,
    render_header,
    render_sidebar,
    render_input_workspace,
    render_preview_section,
    render_overview_workspace,
    render_detailed_analysis_workspace,
    render_resume_studio,
    render_resume_builder_preview,
    render_export_workspace,
    render_footer,
)

# 1. Page Configuration
st.set_page_config(
    page_title=f"{APP_NAME} | MirAI Capstone",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# 2. Session State Initialization
def initialize_session_state() -> None:
    """Initializes all session_state keys with strict default values to prevent KeyErrors."""
    for key, default_value in INITIAL_SESSION_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def main() -> None:
    """Main application runtime function."""
    initialize_session_state()
    apply_lightweight_custom_css()

    # Render Header & Sidebar
    render_header()
    render_sidebar()

    # Render Input Workspace Form
    resume_input, job_input, analyze_submitted, load_sample, clear_inputs = render_input_workspace()

    # Update session state with current text area values
    st.session_state["resume_text"] = resume_input
    st.session_state["job_description"] = job_input

    # Form Action Handlers
    if load_sample:
        sample_resume = load_sample_file(SAMPLE_RESUME_PATH)
        sample_job = load_sample_file(SAMPLE_JOB_DESC_PATH)
        st.session_state["resume_text"] = sample_resume
        st.session_state["job_description"] = sample_job
        st.rerun()

    if clear_inputs:
        st.session_state["resume_text"] = ""
        st.session_state["job_description"] = ""
        st.session_state["analysis_complete"] = False
        st.session_state["analysis_json"] = None
        st.rerun()

    if analyze_submitted:
        cur_resume = st.session_state.get("resume_text", "").strip()
        cur_job = st.session_state.get("job_description", "").strip()
        
        if not cur_resume or not cur_job:
            st.warning("Please provide both a candidate resume and a target job description before analyzing.")
        else:
            api_key = resolve_api_key()
            if api_key:
                # Execute Live Gemini API Evaluation with Staged Loading Status
                try:
                    with st.status("Executing Gemini 2.5 Flash Evaluation...", expanded=True) as status:
                        st.write("📌 Preparing prompt and validating document inputs...")
                        st.write("🤖 Transmitting single-call request to Gemini 2.5 Flash model...")
                        
                        persona = st.session_state.get("evaluator_persona", "🌶️ Ruthless Tech Recruiter (Roast Mode)")
                        seniority = st.session_state.get("target_seniority", "Mid-Level Software Engineer (2-5 YOE)")
                        
                        analysis_dict = analyze_resume_with_gemini(
                            resume_text=cur_resume,
                            job_description=cur_job,
                            api_key=api_key,
                            persona_tone=persona,
                            seniority_level=seniority,
                        )
                        
                        st.write("🔍 Cleaning response and performing deep schema validation...")
                        st.write("✅ Analysis JSON successfully validated!")
                        status.update(label=f"Evaluation Complete ({persona.split(' ')[0]} Mode)!", state="complete", expanded=False)

                    st.session_state["analysis_json"] = analysis_dict
                    st.session_state["analysis_complete"] = True
                    st.session_state["resume_scores"] = analysis_dict.get("scores", {})
                    st.rerun()

                except Exception as e:
                    st.error("Unable to analyze the resume. Please check your API key configuration and try again.")
                    with st.expander("Offline Development Testing Mode"):
                        st.caption("No API key configured? You can load pre-evaluated mock data to test the workspace.")
                        if st.button("Load Pre-evaluated Mock Analysis"):
                            mock_data = load_mock_analysis("data/mock_analysis.json")
                            st.session_state["analysis_json"] = mock_data
                            st.session_state["analysis_complete"] = True
                            st.session_state["resume_scores"] = mock_data.get("scores", {})
                            st.rerun()
            else:
                st.error("Gemini API Key missing. Please set `GEMINI_API_KEY` in Streamlit secrets or environment variables.")
                col_off1, _ = st.columns([1, 2])
                with col_off1:
                    if st.button("Load Pre-evaluated Mock Analysis (Offline Mode)", use_container_width=True):
                        mock_data = load_mock_analysis("data/mock_analysis.json")
                        st.session_state["analysis_json"] = mock_data
                        st.session_state["analysis_complete"] = True
                        st.session_state["resume_scores"] = mock_data.get("scores", {})
                        st.rerun()

    # Render Active Dashboard or Previews
    analysis_json = st.session_state.get("analysis_json")
    analysis_complete = st.session_state.get("analysis_complete", False)

    if analysis_complete and analysis_json:
        # Render Full Dashboard Workspace
        render_overview_workspace(analysis_json)
        render_detailed_analysis_workspace(analysis_json)
        render_resume_studio(analysis_json)
        render_resume_builder_preview(analysis_json)
        render_export_workspace(analysis_json)
    else:
        # Render Initial Text Previews
        render_preview_section()

    # Render Application Footer
    render_footer()


if __name__ == "__main__":
    main()
