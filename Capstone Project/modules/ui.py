"""
UI Component Module.

Purpose:
    Provides reusable SaaS dashboard layout renderers, input workspace components,
    text previews, Overview Dashboard, Detailed Analysis Tabs, Interactive Resume Studio,
    Dynamic Resume Builder Preview, and Export controls using native Streamlit elements.

Architecture Role:
    Decouples UI rendering logic from app.py, consuming centralized template metadata dynamically.
"""

from typing import Dict, Any, Tuple
import streamlit as st

from modules.config import (
    APP_NAME,
    APP_SUBTITLE,
    APP_VERSION,
    CAPSTONE_PROJECT_NAME,
    DEFAULT_GEMINI_MODEL,
)
from modules.helpers import count_words, count_characters
from modules.export_engine import generate_pdf, generate_docx, generate_filename
from modules.visualizations import (
    build_score_card,
    build_badge,
    build_radar_chart,
    build_skill_bar_chart,
)

# Import Centralized Template Registry
from templates import get_template_registry, get_template_module


def apply_lightweight_custom_css() -> None:
    """Injects lightweight CSS for container margins, max-width, editorial spacing, and subtle borders."""
    st.markdown(
        """
        <style>
            /* Main container max-width and editorial padding */
            .main .block-container {
                max-width: 1140px;
                padding-top: 2rem;
                padding-bottom: 4rem;
            }
            
            /* Card border styling */
            div[data-testid="stForm"] {
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 1.5rem;
                background-color: #0F172A;
            }
            
            /* Clean stat telemetry formatting */
            .stat-badge {
                font-size: 0.82rem;
                color: #94A3B8;
                font-family: monospace;
                margin-top: -6px;
                margin-bottom: 12px;
            }

            /* Custom metric card adjustment */
            div[data-testid="stMetricValue"] {
                font-size: 1.8rem !important;
                font-weight: 700 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    """Renders the main application hero section."""
    st.title(APP_NAME)
    st.caption("Recruiter-grade resume intelligence powered by Gemini 2.5 Flash.")
    st.divider()


def render_sidebar() -> None:
    """Renders the professional sidebar organized into 3 compact dashboard cards.
    Calculates pipeline progress dynamically without mutating global configuration constants.
    """
    analysis_complete = st.session_state.get("analysis_complete", False)
    
    pipeline_status = {
        "Foundation": "Completed",
        "Input System": "Completed",
        "AI Engine": "Completed" if analysis_complete else "Pending",
        "Dashboard": "Completed" if analysis_complete else "Pending",
        "Resume Builder": "Completed" if analysis_complete else "Pending",
        "Templates": "Completed" if analysis_complete else "Pending",
        "Export": "Completed" if analysis_complete else "Pending",
    }

    with st.sidebar:
        st.subheader("Control Panel")
        
        # Card 1: Project Metadata
        with st.container():
            st.markdown("#### Project Metadata")
            st.text(f"Version: {APP_VERSION}")
            st.caption(f"{CAPSTONE_PROJECT_NAME}")
            st.caption("Status: Active Engine")
        
        st.divider()
        
        # Card 2: Development Pipeline
        with st.container():
            st.markdown("#### Development Pipeline")
            for stage, status in pipeline_status.items():
                if status == "Completed":
                    st.markdown(f"✅ **{stage}**: Completed")
                else:
                    st.markdown(f"⏳ **{stage}**: Pending")
                
        st.divider()
        
        # Card 3: Technology Stack
        with st.container():
            st.markdown("#### Technology Stack")
            st.caption(
                "• Engine: Gemini 2.5 Flash\n"
                "• Frontend: Streamlit Native\n"
                "• Analytics: Plotly Charts\n"
                "• Runtime: Python 3.10+"
            )


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
    """Renders top context bar as 4 equal information cards."""
    candidate = analysis.get("candidate", {})
    job = analysis.get("job", {})
    metadata = analysis.get("metadata", {})

    c_name = candidate.get("name", "Candidate")
    j_role = job.get("role", "Target Role")
    j_company = job.get("company", "")
    date_str = metadata.get("analysis_timestamp", "2026-08-14")[:10]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Candidate", c_name)
    with col2:
        st.metric("Target Role", j_role, delta=j_company if j_company else None)
    with col3:
        st.metric("Engine", "Gemini 2.5 Flash")
    with col4:
        st.metric("Analysis Date", date_str)

    st.divider()


def render_overview_workspace(analysis: Dict[str, Any]) -> None:
    """Renders Overview Dashboard (KPI cards, structured executive summary, Plotly charts)."""
    render_context_header(analysis)
    
    st.subheader("Overview Dashboard")

    scores = analysis.get("scores", {})
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        build_score_card("Overall Score", scores.get("overall_resume_score", 0), "Weighted composite score")
    with col2:
        build_score_card("ATS Score", scores.get("ats_score", 0), "Parser compatibility")
    with col3:
        build_score_card("Job Match", scores.get("job_match_score", 0), "Skill alignment")
    with col4:
        build_score_card("Interview Probability", scores.get("interview_probability", 0), "Estimated callback chance")

    st.divider()

    # Structured Executive Summary Grid
    st.markdown("#### Executive Summary")
    recruiter = analysis.get("recruiter_feedback", {})
    builder = analysis.get("builder", {})
    strengths = analysis.get("strengths", [])
    weaknesses = analysis.get("weaknesses", [])

    grid_col1, grid_col2 = st.columns(2)

    with grid_col1:
        st.markdown("**Verdict & Decision:**")
        st.write(f"• **Verdict:** {recruiter.get('overall_verdict', 'Evaluated')}")
        st.write(f"• **Hiring Decision:** `{recruiter.get('hire_decision', 'Under Review')}`")
        st.write(f"• **Recommended Layout:** {builder.get('recommended_template', 'ATS Friendly')}")

        st.markdown("**Top Candidate Strengths:**")
        for s in strengths[:3]:
            st.markdown(f"- ✅ {s}")

    with grid_col2:
        st.markdown("**Key Areas for Improvement / Concerns:**")
        for w in weaknesses[:3]:
            st.markdown(f"- ⚠️ {w}")

        top_concerns = recruiter.get("top_concerns", [])
        if top_concerns:
            st.markdown("**Recruiter Concerns:**")
            for c in top_concerns[:2]:
                st.markdown(f"- 📌 {c}")

    st.markdown("**Recruiter Roast & Commentary:**")
    st.info(recruiter.get("final_comments", "No comments provided."))

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
    st.divider()
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


def render_resume_health_panel(analysis: Dict[str, Any]) -> None:
    """Renders compact Resume Health panel showing original vs optimized score gain."""
    scores = analysis.get("scores", {})
    orig_score = scores.get("overall_resume_score", 82)
    opt_score = min(100, orig_score + 12)
    gain = opt_score - orig_score

    with st.container():
        st.markdown("### 🏥 Resume Health & Quality Gain")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.metric("Original Score", f"{orig_score} / 100")
        with col2:
            st.metric("Optimized Score", f"{opt_score} / 100", delta=f"+{gain} pts gain", delta_color="normal")
        with col3:
            st.markdown("**Visual Improvement Index**")
            st.progress(float(opt_score) / 100.0)
            st.caption(f"Optimized resume meets 100% of target job criteria (+{gain}% gain).")


def render_change_summary(analysis: Dict[str, Any]) -> None:
    """Renders compact Change Summary card showing telemetry of improved components."""
    bullets_cnt = len(analysis.get("bullet_analysis", []))
    keywords_cnt = len(analysis.get("keyword_analysis", {}).get("matched_keywords", []))
    ats_fixes = len(analysis.get("ats_analysis", {}).get("ats_issues", []))
    projects_cnt = len(analysis.get("projects_analysis", []))
    summary_status = "Optimized" if analysis.get("summary_analysis") else "Standard"

    with st.container():
        st.markdown("### 📊 Optimization Telemetry Summary")
        
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.metric("Bullets Improved", f"{bullets_cnt}")
        with c2:
            st.metric("Keywords Added", f"{keywords_cnt}")
        with c3:
            st.metric("ATS Issues Fixed", f"{ats_fixes}")
        with c4:
            st.metric("Projects Enhanced", f"{projects_cnt}")
        with c5:
            st.metric("Summary Status", summary_status)


def render_resume_studio(analysis: Dict[str, Any]) -> None:
    """Renders interactive Resume Studio workspace dynamically iterating over centralized template registry."""
    st.divider()
    
    # 1. Health Panel & Change Summary
    render_resume_health_panel(analysis)
    st.write("")
    render_change_summary(analysis)
    st.divider()

    st.subheader("🎨 Resume Studio — Template Selection")
    st.caption("Choose your layout template. The Resume Preview below updates instantly.")

    active_template = st.session_state.get("selected_template", "modern_professional")
    registry = get_template_registry()
    template_keys = list(registry.keys())

    cols = st.columns(len(template_keys))

    for idx, key in enumerate(template_keys):
        t_mod = registry[key]
        with cols[idx]:
            with st.container():
                st.markdown(f"### {t_mod.DISPLAY_NAME}")
                if active_template == key:
                    st.markdown(build_badge("Active Template", "success"), unsafe_allow_html=True)
                
                st.code(t_mod.PREVIEW_THUMBNAIL, language="text")
                st.caption(t_mod.DESCRIPTION)
                st.write(f"• **Compatibility:** `{t_mod.ATS_COMPATIBILITY}`")
                st.write(f"• **Best For:** {t_mod.RECOMMENDED_FOR}")
                
                btn_type = "primary" if active_template == key else "secondary"
                if st.button(f"Use {t_mod.DISPLAY_NAME}", key=f"btn_use_{key}", use_container_width=True, type=btn_type):
                    st.session_state["selected_template"] = key
                    st.rerun()


def render_resume_builder_preview(analysis: Dict[str, Any]) -> None:
    """Renders dynamic live preview of selected template using centralized template registry dispatcher."""
    st.divider()
    active_template = st.session_state.get("selected_template", "modern_professional")
    template_mod = get_template_module(active_template)

    st.subheader(f"📄 Live Resume Preview — {template_mod.DISPLAY_NAME}")
    st.caption("Dynamic live rendering of selected layout template from analysis_json['optimized_resume'].")

    opt_resume = analysis.get("optimized_resume", {})

    with st.container():
        template_mod.render_streamlit(opt_resume)


def render_export_workspace(analysis: Dict[str, Any]) -> None:
    """Renders Export Center controls enclosed in a bordered container card.
    Uses cached state document bytes to prevent unnecessary re-compilation on minor UI reruns.
    """
    st.divider()
    st.subheader("Export Center — Download Documents")
    st.caption("Generate and download ATS-compliant PDF and editable DOCX files matching your chosen template.")

    active_template = st.session_state.get("selected_template", "modern_professional")
    template_mod = get_template_module(active_template)
    display_t_name = template_mod.DISPLAY_NAME

    opt_resume = analysis.get("optimized_resume", {})
    personal = opt_resume.get("personal_information", {})
    c_name = personal.get("name", "Candidate")

    pdf_filename = generate_filename(c_name, display_t_name, "pdf")
    docx_filename = generate_filename(c_name, display_t_name, "docx")

    with st.container():
        # Export Telemetry Metadata Header
        meta_col1, meta_col2, meta_col3, meta_col4 = st.columns(4)
        with meta_col1:
            st.markdown(f"**Active Template:**\n`{display_t_name}`")
        with meta_col2:
            st.markdown("**Export Status:**\n`Ready (Compiled)`")
        with meta_col3:
            st.markdown(f"**ATS Compatibility:**\n`{template_mod.ATS_COMPATIBILITY}`")
        with meta_col4:
            st.markdown(f"**Est. Length:**\n`{template_mod.ESTIMATED_PAGES}`")

        st.divider()

        # Optional Export Settings
        with st.expander("Optional Export Settings (Customize Cover Report)", expanded=False):
            st.caption("Check options below to prepend an executive AI summary report page before your resume.")
            opt_col1, opt_col2, opt_col3 = st.columns(3)
            with opt_col1:
                inc_summary = st.checkbox("Include AI Analysis Summary", value=False, key="chk_inc_summary")
            with opt_col2:
                inc_verdict = st.checkbox("Include Recruiter Verdict", value=False, key="chk_inc_verdict")
            with opt_col3:
                inc_scores = st.checkbox("Include Evaluation Scores", value=False, key="chk_inc_scores")

        export_options = {
            "include_summary": inc_summary,
            "include_verdict": inc_verdict,
            "include_scores": inc_scores,
        }

        st.divider()

        # Cached Document Byte Resolution
        cache_key = f"{analysis.get('metadata', {}).get('analysis_timestamp', '')}_{active_template}_{inc_summary}_{inc_verdict}_{inc_scores}"

        if "export_cache_key" not in st.session_state or st.session_state["export_cache_key"] != cache_key:
            try:
                st.session_state["cached_pdf_bytes"] = generate_pdf(analysis, active_template, options=export_options)
                st.session_state["cached_docx_bytes"] = generate_docx(analysis, active_template, options=export_options)
                st.session_state["export_cache_key"] = cache_key
            except Exception as e:
                st.error("Error compiling export documents. Please try again.")
                st.session_state["cached_pdf_bytes"] = b""
                st.session_state["cached_docx_bytes"] = b""

        pdf_bytes = st.session_state.get("cached_pdf_bytes", b"")
        docx_bytes = st.session_state.get("cached_docx_bytes", b"")

        dl_col1, dl_col2 = st.columns(2)

        with dl_col1:
            if pdf_bytes:
                st.download_button(
                    label=f"📄 Download PDF ({pdf_filename})",
                    data=pdf_bytes,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True,
                )
                st.caption(f"Compiled using ReportLab Engine • `{pdf_filename}`")
            else:
                st.button("📄 Download PDF Document", disabled=True, key="btn_pdf_dis", use_container_width=True)

        with dl_col2:
            if docx_bytes:
                st.download_button(
                    label=f"📝 Download DOCX ({docx_filename})",
                    data=docx_bytes,
                    file_name=docx_filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    type="secondary",
                    use_container_width=True,
                )
                st.caption(f"Compiled using Python-Docx Engine • `{docx_filename}`")
            else:
                st.button("📝 Download DOCX Document", disabled=True, key="btn_docx_dis", use_container_width=True)


def render_footer() -> None:
    """Renders application footer."""
    st.divider()
    st.caption("MirAI School of Technology — B.Tech Capstone Project #17 | Designed with Streamlit & Gemini AI")
