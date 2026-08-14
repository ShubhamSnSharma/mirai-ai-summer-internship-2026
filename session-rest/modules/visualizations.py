"""
Data Visualization & UI Component Module.

Purpose:
    Generates interactive Plotly charts (Radar, Skills Bar, Score Donut) and reusable
    UI score cards and badges using Streamlit native primitives.

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
    """Renders a structured KPI metric card with qualitative benchmark rating.

    Args:
        title: Metric title.
        score: Numerical score (0-100).
        description: Subtitle description or guidance.
    """
    rating, benchmark = get_score_rating(score)
    st.metric(
        label=title,
        value=f"{score} / 100",
        delta=f"{rating} ({benchmark})",
        delta_color="normal" if score >= 70 else "inverse",
    )
    if description:
        st.caption(description)


def build_badge(text: str, badge_type: str = "info") -> str:
    """Returns HTML for a styled inline badge component.

    Args:
        text: Badge label text.
        badge_type: 'success', 'warning', 'danger', 'info', or 'neutral'.

    Returns:
        HTML string.
    """
    color_map = {
        "success": ("#059669", "#ECFDF5"),
        "warning": ("#D97706", "#FFFBEB"),
        "danger": ("#DC2626", "#FEF2F2"),
        "info": ("#2563EB", "#EFF6FF"),
        "neutral": ("#475569", "#F8FAFC"),
    }
    fg, bg = color_map.get(badge_type, color_map["info"])
    return (
        f'<span style="background-color: {bg}; color: {fg}; font-size: 0.78rem; '
        f'font-weight: 600; padding: 3px 10px; border-radius: 12px; margin-right: 6px; '
        f'border: 1px solid {fg}40; display: inline-block; margin-bottom: 4px;">{text}</span>'
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
            line=dict(color="#2563EB", width=2),
            fillcolor="rgba(37, 99, 235, 0.25)",
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
                marker=dict(color="#059669"),
            )
        )

    if missing_names:
        fig.add_trace(
            go.Bar(
                y=missing_names,
                x=missing_conf,
                name="Missing / Target Skills",
                orientation="h",
                marker=dict(color="#DC2626"),
            )
        )

    fig.update_layout(
        bmode="group",
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
                marker=dict(colors=["#2563EB", "#059669", "#D97706", "#7C3AED", "#06B6D4"]),
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
