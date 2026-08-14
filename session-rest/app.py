"""
AI Resume Critic & Career Optimizer — Main Streamlit Application Entrypoint.

B.Tech Capstone Project — MirAI School of Technology (Problem Statement #17)

Architecture Note:
    Phase 3: Recruiter Dashboard & Visual Analytics (Mock Data).
    Consumes unified JSON data contract (data/mock_analysis.json) via modules/helpers.py.
    Provides Overview Dashboard, Detailed Analysis, Resume Preview, Templates, and Export.
"""

import time
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
from modules.ui import (
    apply_lightweight_custom_css,
    render_header,
    render_sidebar,
    render_input_workspace,
    render_preview_section,
    render_overview_workspace,
    render_detailed_analysis_workspace,
    render_resume_builder_preview,
    render_template_gallery_workspace,
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

    # Update progress checklist status for Phase 3
    PROGRESS_CHECKLIST["Dashboard"] = "Completed"

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
            with st.spinner("Analyzing candidate resume against target job description using Gemini 2.5 Flash..."):
                time.sleep(0.6)  # Simulated loading state UX
                analysis_data = load_mock_analysis("data/mock_analysis.json")
                if validate_analysis_schema(analysis_data):
                    st.session_state["analysis_json"] = analysis_data
                    st.session_state["analysis_complete"] = True
                    st.session_state["resume_scores"] = analysis_data.get("scores", {})
                    st.rerun()
                else:
                    st.error("Failed to load valid analysis schema.")

    # Render Active Dashboard or Previews
    analysis_json = st.session_state.get("analysis_json")
    analysis_complete = st.session_state.get("analysis_complete", False)

    if analysis_complete and analysis_json:
        # Render Full Dashboard Workspace
        render_overview_workspace(analysis_json)
        render_detailed_analysis_workspace(analysis_json)
        render_resume_builder_preview(analysis_json)
        render_template_gallery_workspace(analysis_json)
        render_export_workspace(analysis_json)
    else:
        # Render Initial Text Previews
        render_preview_section()

    # Render Application Footer
    render_footer()


if __name__ == "__main__":
    main()
