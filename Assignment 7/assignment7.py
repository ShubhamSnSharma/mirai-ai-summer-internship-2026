import streamlit as st
import pandas as pd

from google import genai
from dotenv import load_dotenv
import os

from urllib.parse import quote

# ---------------------------------------
# Page Configuration
# ---------------------------------------

st.set_page_config(
    page_title="ScreenSense AI",
    page_icon="📱",
    layout="wide"
)

# ---------------------------------------
# Load Environment Variables
# ---------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ Google API Key not found. Please add it to your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

# ---------------------------------------
# Dashboard Title
# ---------------------------------------

st.title("📱 ScreenSense AI")
st.write("Understand your digital habits through AI-powered wellbeing analysis.")

# ---------------------------------------
# Load Dataset
# ---------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("screentime.csv")

try:
    df = load_data()

except FileNotFoundError:
    st.error("❌ 'screentime.csv' was not found. Please make sure it is in the project folder.")
    st.stop()

# ---------------------------------------
# Validate Dataset
# ---------------------------------------

required_columns = [
    "Date",
    "Day",
    "App_Name",
    "Category",
    "Minutes_Used"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
    st.stop()

# ---------------------------------------
# Data Preprocessing
# ---------------------------------------

df["Date"] = pd.to_datetime(df["Date"])

# ---------------------------------------
# Data Bridge for Gemini
# ---------------------------------------

def create_summary(day_data):
    """
    Summarize the selected day's screen time by category.
    Returns a string that Gemini can understand.
    """

    summary = (
        day_data.groupby("Category")["Minutes_Used"]
        .sum()
        .sort_values(ascending=False)
    )

    return summary.to_string()

# ---------------------------------------
# Sidebar Controls
# ---------------------------------------

with st.sidebar:

    st.header("📊 Dashboard Controls")

    available_dates = sorted(df["Date"].dt.date.unique())

    selected_date = st.selectbox(
        "📅 Select a Date",
        available_dates
    )

    daily_goal = st.slider(
        "🎯 Daily Screen Time Goal (minutes)",
        min_value=60,
        max_value=600,
        value=360,
        step=30
    )

    st.caption(f"🎯 Daily Goal: {daily_goal} minutes")

# ---------------------------------------
# Filter Data by Selected Date
# ---------------------------------------

filtered_df = df[df["Date"].dt.date == selected_date]

if filtered_df.empty:
    st.warning("⚠️ No screen time data available for the selected date.")
    st.stop()

# ---------------------------------------
# KPI Calculations
# ---------------------------------------

total_screen_time = filtered_df["Minutes_Used"].sum()

most_used_app = (
    filtered_df.groupby("App_Name")["Minutes_Used"]
    .sum()
    .idxmax()
)

goal_difference = total_screen_time - daily_goal

# ---------------------------------------
# KPI Cards
# ---------------------------------------

st.header("📅 Daily Dashboard")

st.caption(
    f"Viewing screen-time data for **{selected_date}**"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="📱 Total Screen Time",
        value=f"{total_screen_time} mins"
    )

with col2:
    st.metric(
        label="🏆 Most Used App",
        value=most_used_app
    )

with col3:

    if goal_difference > 0:
        delta_text = f"{goal_difference} mins over goal"

    elif goal_difference < 0:
        delta_text = f"{abs(goal_difference)} mins under goal"

    else:
        delta_text = "Goal achieved"

    st.metric(
        label="🎯 Daily Goal",
        value=f"{daily_goal} mins",
        delta=delta_text,
        delta_color="inverse"
    )

st.divider()

# ---------------------------------------
# Charts
# ---------------------------------------

st.header("📊 Screen Time Analytics")

category_usage = (
    filtered_df.groupby("Category")["Minutes_Used"]
    .sum()
)

app_usage = (
    filtered_df.groupby("App_Name")["Minutes_Used"]
    .sum()
    .sort_values(ascending=False)
)

daily_trend = (
    df.groupby("Date")["Minutes_Used"]
    .sum()
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Usage by Category")
    st.bar_chart(category_usage)

with col2:
    st.subheader("📱 Usage by App")
    st.bar_chart(app_usage)

st.subheader("📈 Daily Screen Time Trend")
st.line_chart(daily_trend)

# ---------------------------------------
# Screen Time Summary for Gemini
# ---------------------------------------

screen_time_summary = create_summary(filtered_df)

# ---------------------------------------
# Gemini Prompt
# ---------------------------------------

prompt = f"""
You are Life-OS, an AI productivity and wellbeing coach.

Today's screen time summary for {selected_date}.

The user's daily screen time goal is {daily_goal} minutes.

Today's total screen time is {total_screen_time} minutes.

The user is {'above' if goal_difference > 0 else 'below'} their goal by {abs(goal_difference)} minutes.

The most used app today was {most_used_app}.

Screen time summary by category:

{screen_time_summary}

Interpret the categories as follows:

Productive:
- Coding
- Education
- Productivity

Leisure:
- Entertainment
- Social Media

Neutral:
- Communication

Analyze today's digital habits and provide constructive feedback.

Important instructions:

- Start directly with the analysis.
- Do NOT greet the user.
- Do NOT introduce yourself.
- Do NOT say "Hello" or "Hi".
- Do NOT say "Life-OS here".
- Do NOT tell the user to simply reduce screen time.
- Recognize productive screen time separately from leisure screen time.
- If leisure usage is high, explain why it could become unhealthy.
- Suggest practical offline alternatives like:
    • Gym
    • Walking
    • Reading
    • Journaling
    • Meal preparation
    • Spending time with family or friends
- Encourage balance instead of perfection.

Format your response using Markdown with exactly these headings:

## Positive Habits

## Areas to Improve

## Action Plan

Use Markdown formatting.
Keep the response between 150 and 200 words.
Avoid repeating every number from the summary.
Instead, interpret the habits and explain what they mean.
End with exactly THREE practical actions the user can follow tomorrow.
"""

# ---------------------------------------
# Avatar Prompt
# ---------------------------------------

avatar_prompt = f"""
You are an expert prompt engineer for a photorealistic AI image generator.

Your job is to convert the user's digital wellbeing statistics into ONE realistic cinematic scene.

User's screen-time data:

Date: {selected_date}

Daily Goal:
{daily_goal} minutes

Today's Total Screen Time:
{total_screen_time} minutes

Difference From Goal:
{goal_difference} minutes

Most Used App:
{most_used_app}

Category Breakdown:
{screen_time_summary}

Create ONE highly detailed image prompt.

The prompt must describe ONE Indian male college student around 20 years old.

The student should be the ONLY main subject in the image.

The scene should immediately communicate the emotional impact of today's digital habits.

Rules for the scene:

• If productive usage (Coding, Education, Productivity) dominates, portray a focused, motivated student working at a clean study desk with books, laptop, notebook, soft warm sunlight, organized surroundings and confident body language.

• If Entertainment or Social Media dominate, portray the student looking mentally exhausted, tired, distracted or emotionally drained while surrounded by multiple glowing screens, messy desk, dark room, late-night atmosphere and signs of digital overload.

• If the daily goal is exceeded by a large amount, exaggerate the emotional weight naturally. Show eye strain, fatigue, poor posture, scattered snack wrappers, dim lighting, messy workspace or an overflowing digital environment without becoming unrealistic.

The environment should subtly reflect the most-used app.

Examples:
- VS Code → coding workspace
- YouTube → video playing on monitor
- Netflix/Streaming → television or monitor with blurred entertainment visuals
- ChatGPT/Gemini → AI chat open on laptop
- Browser → many open tabs

Image requirements:

- Photorealistic
- Cinematic composition
- Full-body portrait
- Eye-level camera angle
- Natural human anatomy
- Indian male college student
- Approximately 20 years old
- Short black hair
- Casual clothes (hoodie, t-shirt or shirt)
- Expressive face
- Natural skin tones
- Detailed hands
- Realistic proportions
- High detail
- Soft depth of field
- Professional color grading
- Dramatic but believable lighting
- Indoor environment
- Realistic furniture
- Modern study room
- High-quality digital illustration
- Emotionally powerful
- Storytelling composition

Avoid:

- Female characters
- Multiple people
- Robots
- Abstract technology art
- Floating holograms
- Sci-fi interfaces
- Cyberpunk
- Anime
- Cartoon style
- Fantasy elements
- Logos
- Text
- Watermarks
- Extra limbs
- Deformed hands
- Distorted faces

The final image should look like a still frame from an award-winning coming-of-age film about digital wellbeing.

Return ONLY the finished image prompt.
"""

# ---------------------------------------
# AI Productivity Coach
# ---------------------------------------

st.divider()

st.header("AI Wellbeing Analysis")
st.write("Get personalized wellbeing insights based on today's screen time.")

generate = st.button(
    "✨ Analyze My Screen Time",
    use_container_width=True
)

if generate:

    with st.spinner("🧠 Gemini is analyzing today's digital habits..."):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            avatar_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=avatar_prompt
        )
            if not response.text:
                st.warning("No AI wellbeing report was generated.")
                st.stop()

            if not avatar_response.text:
                st.warning("No avatar prompt was generated.")
                st.stop()

            image_prompt = avatar_response.text.strip()

            st.toast(
                "AI report generated successfully!",
                icon="🤖"
            )

            if goal_difference >= 240:
                st.error("🚨 Your screen time is far above your daily goal.")

            elif goal_difference > 0:
                st.warning("⚠️ You exceeded your daily goal today.")

            else:
                st.success("🎉 Excellent! You stayed within your daily goal.")

            # ---------------------------------------
            # AI Report + Avatar
            # ---------------------------------------

            image_url = (
                "https://image.pollinations.ai/prompt/"
                + quote(image_prompt)
            )

            report_col, avatar_col = st.columns([3, 2])

            # --------------------
            # AI Report
            # --------------------

            with report_col:

                with st.container(border=True):
                    st.markdown("## 💡 Digital Wellness Report")
                    st.caption(
                        f"Generated on {selected_date.strftime('%B %d, %Y')}"
                    )

                    st.markdown(response.text)

            # --------------------
            # AI Avatar
            # --------------------

            with avatar_col:

                with st.container(border=True):

                    st.markdown("## 🖼️ AI Wellbeing Avatar")

                    st.info(
                        "Visual interpretation generated from today's digital habits."
                    )

                    st.image(
                        image_url,
                        width=330
                    )

                    st.caption(
                        "AI-generated visual interpretation of today's digital wellbeing."
                    )

        except Exception:
            st.error(
                "❌ Unable to generate AI insights. Please check your internet connection or API key and try again."
            )


st.divider()

st.markdown(
    """
    <div style='text-align:center; color:gray; font-size:14px'>
    ScreenSense AI • Built with Streamlit • Gemini 2.5 Flash • Pollinations AI
    </div>
    """,
    unsafe_allow_html=True
)