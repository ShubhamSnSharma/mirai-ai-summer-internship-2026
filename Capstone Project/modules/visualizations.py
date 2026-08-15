"""
Data Visualization & UI Component Module.

Purpose:
    Generates interactive Plotly charts (Radar, Skills Bar, Score Donut) and reusable
    UI score cards, info cards, and badges using Streamlit native primitives.

Architecture Role:
    Consumes unified JSON analysis data and provides clean visualization objects to modules/ui.py.
"""

from typing import Dict, Any, List, Tuple
import plotly.graph_objects as go
import streamlit as st


def get_score_rating(score: int) -> Tuple[str, str]:
    """Returns qualitative rating label and benchmark percentile based on numerical score.

    Args:
        score: Numerical score (0-100).

    Returns:
        Tuple of (rating_label, benchmark_percentile).
    """
    if score >= 90:
        return "Excellent", "Top 10%"
    elif score >= 80:
        return "Strong", "Top 20%"
    elif score >= 70:
        return "Competitive", "Top 35%"
    else:
        return "Needs Improvement", "Below Target"


def build_score_card(title: str, score: int, description: str = "") -> None:
    """Renders a structured KPI metric card with qualitative benchmark rating inside a container card.

    Args:
        title: Metric title.
        score: Numerical score (0-100).
        description: Subtitle description or guidance.
    """
    rating, benchmark = get_score_rating(score)
    with st.container():
        st.metric(
            label=title,
            value=f"{score}",
            delta=f"{rating} • {benchmark}",
            delta_color="normal" if score >= 70 else "inverse",
        )
        if description:
            st.caption(description)


def build_info_card(title: str, value: str, subtext: str = "") -> None:
    """Renders a clean information card for context bars and sidebars.

    Args:
        title: Card label title.
        value: Primary value string.
        subtext: Optional caption or subtitle text.
    """
    st.markdown(f"**{title}**")
    st.markdown(f"### {value}")
    if subtext:
        st.caption(subtext)


import html


def build_badge(text: str, badge_type: str = "info") -> str:
    """Returns HTML for a styled inline badge component.
    Applies html.escape() for security against HTML/script injection.

    Args:
        text: Badge label text.
        badge_type: 'success', 'warning', 'danger', 'info', or 'neutral'.

    Returns:
        HTML string.
    """
    color_map = {
        "success": ("#10B981", "#064E3B"),
        "warning": ("#F59E0B", "#78350F"),
        "danger": ("#EF4444", "#7F1D1D"),
        "info": ("#3B82F6", "#1E3A8A"),
        "neutral": ("#94A3B8", "#1E293B"),
    }
    fg, bg = color_map.get(badge_type, color_map["info"])
    escaped_text = html.escape(str(text))
    return (
        f'<span style="background-color: {bg}; color: {fg}; font-size: 0.78rem; '
        f'font-weight: 600; padding: 4px 10px; border-radius: 6px; margin-right: 6px; '
        f'border: 1px solid {fg}40; display: inline-block; margin-bottom: 4px;">{escaped_text}</span>'
    )


def build_radar_chart(score_breakdown: Dict[str, int]) -> go.Figure:
    """Generates a 5-axis Plotly radar chart for candidate score breakdown.

    Args:
        score_breakdown: Dictionary mapping axes ('content', 'format', 'impact', 'readability', 'keyword_match') to scores.

    Returns:
        Plotly Figure object.
    """
    categories = [k.replace("_", " ").title() for k in score_breakdown.keys()]
    values = list(score_breakdown.values())
    
    # Close the polygon by repeating first value
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name="Candidate Score",
            line=dict(color="#38BDF8", width=2),
            fillcolor="rgba(56, 189, 248, 0.2)",
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=True,
                ticksuffix="%",
                gridcolor="#334155",
            ),
            angularaxis=dict(
                gridcolor="#334155",
                linecolor="#334155",
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=30, b=30),
        showlegend=False,
        height=320,
    )
    return fig


def build_skill_bar_chart(matched_skills: List[Dict[str, Any]], missing_skills: List[Dict[str, Any]]) -> go.Figure:
    """Generates a horizontal bar chart comparing matched vs missing skills and confidence ratings.

    Args:
        matched_skills: List of matched skill dicts (skill, confidence).
        missing_skills: List of missing skill dicts (skill, confidence).

    Returns:
        Plotly Figure object.
    """
    matched_names = [s.get("skill", "") for s in matched_skills[:6]]
    matched_conf = [s.get("confidence", 80) for s in matched_skills[:6]]
    
    missing_names = [s.get("skill", "") for s in missing_skills[:6]]
    missing_conf = [s.get("confidence", 70) for s in missing_skills[:6]]

    fig = go.Figure()

    if matched_names:
        fig.add_trace(
            go.Bar(
                y=matched_names,
                x=matched_conf,
                name="Matched Skills",
                orientation="h",
                marker=dict(color="#10B981"),
            )
        )

    if missing_names:
        fig.add_trace(
            go.Bar(
                y=missing_names,
                x=missing_conf,
                name="Missing / Target Skills",
                orientation="h",
                marker=dict(color="#EF4444"),
            )
        )

    fig.update_layout(
        barmode="group",
        xaxis=dict(range=[0, 100], title="Confidence Rating (%)", gridcolor="#334155"),
        yaxis=dict(autorange="reversed"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=40, b=20),
        height=320,
    )
    return fig


def build_donut_chart(score_breakdown: Dict[str, int]) -> go.Figure:
    """Generates a Plotly donut chart displaying relative quality distribution.

    Args:
        score_breakdown: Dictionary mapping quality axes to scores.

    Returns:
        Plotly Figure object.
    """
    labels = [k.replace("_", " ").title() for k in score_breakdown.keys()]
    values = list(score_breakdown.values())

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.55,
                marker=dict(colors=["#38BDF8", "#10B981", "#F59E0B", "#818CF8", "#06B6D4"]),
                textinfo="label+percent",
            )
        ]
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC"),
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        height=320,
    )
    return fig
