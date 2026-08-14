"""
UI Component Module.

Purpose:
    Provides reusable layout renderers, input workspace components, text previews,
    Overview Dashboard, Detailed Analysis Tabs, Resume Builder Preview, Template Gallery,
    and Export controls using native Streamlit elements.

Architecture Role:
    Decouples UI rendering logic from app.py to maintain a clean, modular layout.
"""

from typing import Dict, Any, Tuple
import streamlit as st
from modules.config import (
    APP_NAME,
    APP_SUBTITLE,
    APP_DESCRIPTION,
    APP_VERSION,
    CAPSTONE_PROJECT_NAME,
    PROGRESS_CHECKLIST,
)
from modules.helpers import count_words, count_characters
from modules.visualizations import (
    build_score_card,
    build_badge,
    build_radar_chart,
    build_skill_bar_chart,
    build_donut_chart,
)


def apply_lightweight_custom_css() -> None:
    """Injects lightweight CSS for container margins, max-width, and subtle borders."""
    st.markdown(
        """
        <style>
            /* Main container max-width and padding */
            .main .block-container {
                max-width: 1200px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }
            
            /* Subtle borders for cards */
            div[data-testid="stForm"] {
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 1.5rem;
            }
            
            /* Clean stat telemetry formatting */
            .stat-badge {
                font-size: 0.82rem;
                color: #94A3B8;
                font-family: monospace;
                margin-top: -8px;
                margin-bottom: 12px;
            }

            /* Context Header Banner */
            .context-banner {
                background-color: #1E293B;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 12px 18px;
                margin-bottom: 20px;
                font-size: 0.9rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    """Renders the main application hero section."""
    st.title(APP_NAME)
    st.caption(f"{APP_SUBTITLE} | {CAPSTONE_PROJECT_NAME}")
    st.write(APP_DESCRIPTION)
    st.divider()


def render_sidebar() -> None:
    """Renders the professional sidebar with progress tracking and tech stack info."""
    with st.sidebar:
        st.subheader("Project Control")
        st.text(f"Version: {APP_VERSION}")
        
        st.divider()
        
        st.subheader("Application Progress")
        for stage, status in PROGRESS_CHECKLIST.items():
            if status == "Completed":
                st.write(f"[x] {stage}: Completed")
            else:
                st.write(f"[ ] {stage}: Pending")
                
        st.divider()
        
        st.subheader("Technology Stack")
        st.caption(
            "Frontend: Streamlit Native\n"
            "AI Engine: Gemini 2.5 Flash\n"
            "Data Pipeline: Pandas & Docx\n"
            "Visualizations: Plotly\n"
            "Export: ReportLab & Python-Docx"
        )
        
        st.divider()
        st.caption("MirAI School of Technology Capstone #17")


def render_input_workspace() -> Tuple[str, str, bool, bool, bool]:
    """Renders the 2-column input workspace inside a form container.

    Returns:
        Tuple of (resume_text, job_description, analyze_submitted, load_sample_clicked, clear_clicked)
    """
    st.subheader("Input Workspace")
    st.caption("Provide candidate resume text and target job requirements for analysis.")

    with st.form(key="input_form", clear_on_submit=False):
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("#### Candidate Resume")
            resume_input = st.text_area(
                label="Resume Text",
                value=st.session_state.get("resume_text", ""),
                height=320,
                placeholder="Paste candidate resume text here (experience, skills, projects, education)...",
                help="Accepts plain text, markdown, or text copied from PDF/Word resumes.",
                label_visibility="collapsed",
            )
            r_words = count_words(resume_input)
            r_chars = count_characters(resume_input)
            st.markdown(
                f'<div class="stat-badge">Words: {r_words:,} | Characters: {r_chars:,}</div>',
                unsafe_allow_html=True,
            )

        with col_right:
            st.markdown("#### Job Description")
            job_input = st.text_area(
                label="Job Description Text",
                value=st.session_state.get("job_description", ""),
                height=320,
                placeholder="Paste target job description and requirements here...",
                help="Include role responsibilities, required qualifications, and technical stack.",
                label_visibility="collapsed",
            )
            j_words = count_words(job_input)
            j_chars = count_characters(job_input)
            st.markdown(
                f'<div class="stat-badge">Words: {j_words:,} | Characters: {j_chars:,}</div>',
                unsafe_allow_html=True,
            )

        st.divider()

        # Action Bar inside form
        col_act1, col_act2, col_act3 = st.columns([1, 1, 2])
        
        with col_act1:
            load_sample = st.form_submit_button("Load Sample Data", use_container_width=True)
            
        with col_act2:
            clear_inputs = st.form_submit_button("Clear Inputs", use_container_width=True)
            
        with col_act3:
            analyze_submitted = st.form_submit_button(
                "Analyze Resume", type="primary", use_container_width=True
            )

    return resume_input, job_input, analyze_submitted, load_sample, clear_inputs


def render_preview_section() -> None:
    """Renders text preview expanders for current inputs."""
    st.subheader("Text Previews")
    
    resume_text = st.session_state.get("resume_text", "")
    job_desc_text = st.session_state.get("job_description", "")

    with st.expander("Resume Text Preview", expanded=False):
        if resume_text:
            st.code(resume_text, language="text")
        else:
            st.info("No resume text provided yet.")

    with st.expander("Job Description Preview", expanded=False):
        if job_desc_text:
            st.code(job_desc_text, language="text")
        else:
            st.info("No job description text provided yet.")


def render_context_header(analysis: Dict[str, Any]) -> None:
    """Renders top context banner displaying candidate name, role, date, and model."""
    candidate = analysis.get("candidate", {})
    job = analysis.get("job", {})
    metadata = analysis.get("metadata", {})

    c_name = candidate.get("name", "Candidate")
    j_role = job.get("role", "Target Role")
    j_company = job.get("company", "")
    date_str = metadata.get("analysis_timestamp", "2026-08-14")[:10]
    model = metadata.get("model", "gemini-2.5-flash")

    st.markdown(
        f"""
        <div class="context-banner">
            👤 <strong>Candidate:</strong> {c_name} &nbsp;|&nbsp; 
            💼 <strong>Target Role:</strong> {j_role} {f'({j_company})' if j_company else ''} &nbsp;|&nbsp; 
            📅 <strong>Analyzed:</strong> {date_str} &nbsp;|&nbsp; 
            🤖 <strong>Engine:</strong> {model}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_overview_workspace(analysis: Dict[str, Any]) -> None:
    """Renders Overview Dashboard (KPI cards, executive summary, Plotly charts)."""
    render_context_header(analysis)
    
    st.subheader("Overview Dashboard")

    scores = analysis.get("scores", {})
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        build_score_card("Overall Resume Score", scores.get("overall_resume_score", 0), "Weighted composite score")
    with col2:
        build_score_card("ATS Match Score", scores.get("ats_score", 0), "Parser compatibility")
    with col3:
        build_score_card("Job Match Score", scores.get("job_match_score", 0), "Skill & requirement fit")
    with col4:
        build_score_card("Interview Probability", scores.get("interview_probability", 0), "Estimated callback chance")

    st.divider()

    # Executive Analysis Summary
    st.markdown("#### Executive Summary")
    recruiter = analysis.get("recruiter_feedback", {})
    builder = analysis.get("builder", {})

    verdict = recruiter.get("overall_verdict", "Evaluated")
    decision = recruiter.get("hire_decision", "Under Review")
    recommended_template = builder.get("recommended_template", "ATS Friendly")
    export_ready = "Yes (Ready)" if builder.get("export_ready") else "Pending"

    sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
    with sum_col1:
        st.markdown(f"**Verdict:** {verdict}")
    with sum_col2:
        st.markdown(f"**Hiring Decision:** `{decision}`")
    with sum_col3:
        st.markdown(f"**Recommended Layout:** {recommended_template}")
    with sum_col4:
        st.markdown(f"**Export Status:** {export_ready}")

    st.caption(f"**Recruiter Commentary:** {recruiter.get('final_comments', '')}")

    st.divider()

    # Visual Analytics Charts
    st.markdown("#### Visual Analytics")
    chart_col1, chart_col2 = st.columns(2)

    score_breakdown = scores.get("score_breakdown", {"content": 80, "format": 85, "impact": 75, "readability": 90, "keyword_match": 80})
    skills = analysis.get("skills_analysis", {})

    with chart_col1:
        st.markdown("##### 5-Axis Score Breakdown")
        radar_fig = build_radar_chart(score_breakdown)
        st.plotly_chart(radar_fig, use_container_width=True)

    with chart_col2:
        st.markdown("##### Matched vs Target Skills Confidence")
        skills_fig = build_skill_bar_chart(skills.get("matched_skills", []), skills.get("missing_skills", []))
        st.plotly_chart(skills_fig, use_container_width=True)


def render_detailed_analysis_workspace(analysis: Dict[str, Any]) -> None:
    """Renders Detailed Analysis Tabs (ATS, Skills, Experience, Projects, Optimization)."""
    with st.expander("Detailed Analysis & Line-by-Line Critique", expanded=True):
        tabs = st.tabs(["ATS Analysis", "Skills Analysis", "Experience Review", "Projects Review", "Resume Optimization"])

        # Tab 1: ATS Analysis
        with tabs[0]:
            st.markdown("### ATS Parsing & Compliance Analysis")
            ats = analysis.get("ats_analysis", {})

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Format Score", f"{ats.get('format_score', 0)} / 100")
            with col2:
                st.metric("Readability Score", f"{ats.get('readability_score', 0)} / 100")
            with col3:
                st.metric("Keyword Density", f"{ats.get('keyword_density', 0)*100:.1f}%")
            with col4:
                st.metric("Parsing Risk", ats.get("parsing_risk", "Low"))

            st.markdown("#### ATS Warnings & Compliance Issues")
            issues = ats.get("ats_issues", [])
            if issues:
                for issue in issues:
                    st.warning(f"⚠️ {issue}")
            else:
                st.success("Zero ATS parsing formatting defects detected.")

        # Tab 2: Skills Analysis
        with tabs[1]:
            st.markdown("### Skills Alignment & Confidence Ratings")
            skills = analysis.get("skills_analysis", {})

            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.markdown("#### Matched Skills")
                matched = skills.get("matched_skills", [])
                badges_html = "".join([build_badge(f"{s['skill']} ({s['confidence']}%)", "success") for s in matched])
                st.markdown(badges_html, unsafe_allow_html=True)

            with col_m2:
                st.markdown("#### Missing Target Skills")
                missing = skills.get("missing_skills", [])
                badges_html = "".join([build_badge(f"{s['skill']} ({s['confidence']}%)", "danger") for s in missing])
                st.markdown(badges_html, unsafe_allow_html=True)

            st.divider()

            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.markdown("#### Soft Skills Found")
                found_soft = skills.get("soft_skills_found", [])
                st.markdown("".join([build_badge(s, "info") for s in found_soft]), unsafe_allow_html=True)

            with col_s2:
                st.markdown("#### Recommended Skill Additions")
                rec_skills = skills.get("recommended_skills", [])
                st.markdown("".join([build_badge(s, "warning") for s in rec_skills]), unsafe_allow_html=True)

        # Tab 3: Experience Review
        with tabs[2]:
            st.markdown("### Work Experience Review")
            exp_list = analysis.get("experience_analysis", [])

            for idx, exp in enumerate(exp_list, 1):
                company = exp.get("company", "Company")
                role = exp.get("role", "Role")

                with st.expander(f"{idx}. {role} — {company}", expanded=(idx == 1)):
                    st.markdown("**Strengths:**")
                    for s in exp.get("strengths", []):
                        st.markdown(f"- ✅ {s}")

                    st.markdown("**Identified Weaknesses / Flaws:**")
                    for w in exp.get("issues", []):
                        st.markdown(f"- ⚠️ {w}")

                    st.markdown("**Optimized High-Impact Rewrite:**")
                    st.code(exp.get("improved_description", ""), language="text")

        # Tab 4: Projects Review
        with tabs[3]:
            st.markdown("### Technical Projects Review")
            proj_list = analysis.get("projects_analysis", [])

            for idx, proj in enumerate(proj_list, 1):
                p_name = proj.get("project_name", f"Project #{idx}")

                with st.expander(f"📌 {p_name}", expanded=True):
                    st.markdown("**Strengths:**")
                    for s in proj.get("strengths", []):
                        st.markdown(f"- ✅ {s}")

                    st.markdown("**Missing Metrics / Impact:**")
                    for m in proj.get("missing_metrics", []):
                        st.markdown(f"- ⚠️ {m}")

                    st.markdown("**Optimized Project Summary:**")
                    st.code(proj.get("improved_description", ""), language="text")

        # Tab 5: Resume Optimization
        with tabs[4]:
            st.markdown("### Resume Optimization & Line-by-Line Rewrites")
            
            # Summary Optimization
            st.markdown("#### Professional Summary Optimization")
            summary_info = analysis.get("summary_analysis", {})
            st.caption(f"**Critique:** {summary_info.get('issues', '')}")
            
            col_sum1, col_sum2 = st.columns(2)
            with col_sum1:
                st.markdown("**Original Summary:**")
                st.info(summary_info.get("original_summary", ""))
            with col_sum2:
                st.markdown("**Optimized Executive Summary:**")
                st.success(summary_info.get("improved_summary", ""))

            st.divider()

            # Bullet Point Improvements
            st.markdown("#### Bullet Point Rewrites")
            bullets = analysis.get("bullet_analysis", [])

            for idx, b in enumerate(bullets, 1):
                st.markdown(f"**Bullet #{idx} ({b.get('section', 'Experience')} Section)**")
                st.caption(f"**Flaw:** {b.get('issue', '')}")
                
                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    st.markdown("*Original:*")
                    st.error(b.get("original", ""))
                with b_col2:
                    st.markdown("*Improved:*")
                    st.success(b.get("improved", ""))
                
                st.caption(f"💡 *Rationale:* {b.get('reason', '')}")
                st.divider()

            # Prioritized Recommendations
            st.markdown("#### Prioritized Improvement Recommendations")
            recs = analysis.get("recommendations", [])

            for r in recs:
                sev = r.get("severity", "Medium")
                badge_type = "danger" if sev == "Critical" else ("warning" if sev == "High" else "info")
                badge_html = build_badge(f"{sev} Severity", badge_type)
                
                st.markdown(f"**{r.get('title', '')}** {badge_html}", unsafe_allow_html=True)
                st.write(r.get("description", ""))


def render_resume_builder_preview(analysis: Dict[str, Any]) -> None:
    """Renders clean, printable view of optimized candidate resume."""
    st.divider()
    st.subheader("Printable Resume Preview")
    st.caption("Clean, structured preview of candidate resume compiled from JSON data contract.")

    opt = analysis.get("optimized_resume", {})
    personal = opt.get("personal_information", {})

    st.markdown(
        f"""
        <div style="background-color: #0F172A; border: 1px solid #334155; border-radius: 8px; padding: 24px; color: #F8FAFC;">
            <h2 style="margin: 0; color: #38BDF8;">{personal.get('name', 'Alex Chen')}</h2>
            <p style="margin: 4px 0 12px 0; color: #94A3B8; font-size: 0.95rem;">
                {personal.get('location', '')} &nbsp;|&nbsp; {personal.get('email', '')} &nbsp;|&nbsp; {personal.get('phone', '')}<br>
                {personal.get('linkedin', '')} &nbsp;|&nbsp; {personal.get('github', '')}
            </p>
            <h4 style="margin: 12px 0 6px 0; color: #E2E8F0;">{opt.get('headline', '')}</h4>
            <p style="font-size: 0.9rem; color: #CBD5E1;">{opt.get('professional_summary', '')}</p>
            <hr style="border-color: #334155;">
            
            <h4 style="color: #38BDF8;">Technical Skills Matrix</h4>
            <p style="font-size: 0.88rem;">
                <strong>Languages:</strong> {', '.join(opt.get('skills', {}).get('languages', []))}<br>
                <strong>Frameworks:</strong> {', '.join(opt.get('skills', {}).get('frameworks', []))}<br>
                <strong>Databases & Cloud:</strong> {', '.join(opt.get('skills', {}).get('databases', []) + opt.get('skills', {}).get('cloud', []))}
            </p>
            <hr style="border-color: #334155;">

            <h4 style="color: #38BDF8;">Work Experience</h4>
            {''.join([f"<div><strong>{exp.get('role')}</strong> — <em>{exp.get('company')} ({exp.get('start_date')} - {exp.get('end_date')})</em><ul>{''.join([f'<li>{b}</li>' for b in exp.get('bullets', [])])}</ul></div>" for exp in opt.get('experience', [])])}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_template_gallery_workspace(analysis: Dict[str, Any]) -> None:
    """Renders Template Gallery workspace cards."""
    st.divider()
    st.subheader("Template Gallery")
    st.caption("Select executive, ATS, or developer-specific resume layout templates.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### ATS Professional")
        st.caption("Single-column, high-parseability layout designed for 100% ATS pass rates.")
        st.button("Preview ATS Layout", disabled=True, key="btn_t1", use_container_width=True)
        st.caption("🔒 *Available in next phase.*")

    with col2:
        st.markdown("### Modern Professional")
        st.caption("Executive 2-column corporate layout with subtle accent dividers.")
        st.button("Preview Modern Layout", disabled=True, key="btn_t2", use_container_width=True)
        st.caption("🔒 *Available in next phase.*")

    with col3:
        st.markdown("### Developer Tech Specialist")
        st.caption("Code-focused layout highlighting technical skills matrix and project repos.")
        st.button("Preview Developer Layout", disabled=True, key="btn_t3", use_container_width=True)
        st.caption("🔒 *Available in next phase.*")


def render_export_workspace(analysis: Dict[str, Any]) -> None:
    """Renders Export workspace controls."""
    st.divider()
    st.subheader("Export & Download")
    st.caption("Download ATS-compliant PDF and DOCX files compiled directly from JSON.")

    col1, col2 = st.columns(2)

    with col1:
        st.button("📄 Download PDF Document", disabled=True, key="btn_pdf", use_container_width=True)
        st.caption("🔒 *ReportLab PDF compilation engine will be active in next phase.*")

    with col2:
        st.button("📝 Download DOCX Document", disabled=True, key="btn_docx", use_container_width=True)
        st.caption("🔒 *Python-Docx document builder will be active in next phase.*")


def render_footer() -> None:
    """Renders application footer."""
    st.divider()
    st.caption("MirAI School of Technology — B.Tech Capstone Project #17 | Designed with Streamlit & Gemini AI")
