"""
csv_generator.py

Generates a realistic screen-time dataset for ScreenSense AI.

Output:
    screentime.csv

Used for demonstration and testing purposes.
"""

import pandas as pd
from datetime import datetime, timedelta
import random

random.seed(42)

START_DATE = datetime(2026, 7, 18)
NUM_DAYS = 30

rows = []

for day_index in range(NUM_DAYS):

    current_date = START_DATE + timedelta(days=day_index)
    weekday = current_date.weekday()
    weekend = weekday >= 5

    progress = day_index / (NUM_DAYS - 1)

    # ---------------------------------------
    # Usage gradually increases over time
    # ---------------------------------------

    github_min = int(8 + progress * 60)
    github_max = int(18 + progress * 80)

    linkedin_min = int(6 + progress * 25)
    linkedin_max = int(12 + progress * 35)

    chatgpt_min = int(120 + progress * 35)
    chatgpt_max = int(180 + progress * 45)

    claude_min = int(65 + progress * 20)
    claude_max = int(95 + progress * 25)

    gemini_min = int(45 + progress * 15)
    gemini_max = int(70 + progress * 20)

    vscode_min = int(180 + progress * 45)
    vscode_max = int(260 + progress * 60)

    brave_research_min = int(70 + progress * 25)
    brave_research_max = int(120 + progress * 35)

    # ---------------------------------------
    # Different workload every day
    # ---------------------------------------

    workload = random.choice([
        0.90,
        0.95,
        1.00,
        1.05,
        1.10,
        1.20
    ])

    if weekday in [0, 2, 4]:
        workload *= 1.15

    elif weekday == 5:
        workload *= 0.85

    elif weekday == 6:
        workload *= 0.80

    day_entries = []

    def add(app, category, minutes):
        if minutes > 0:
            day_entries.append([
                current_date.strftime("%Y-%m-%d"),
                current_date.strftime("%A"),
                app,
                category,
                int(minutes)
            ])

    # ---------------------------------------
    # DAILY APPS
    # ---------------------------------------

    add(
        "Instagram",
        "Social Media",
        random.randint(55, 70)
    )

    add(
        "WhatsApp",
        "Social Media",
        random.randint(8, 18)
    )

    add(
        "LinkedIn",
        "Social Media",
        random.randint(linkedin_min, linkedin_max)
    )

    add(
        "ChatGPT",
        "Education",
        random.randint(chatgpt_min, chatgpt_max) * workload
    )

    add(
        "Claude",
        "Education",
        random.randint(claude_min, claude_max) * workload
    )

    add(
        "Gemini",
        "Education",
        random.randint(gemini_min, gemini_max) * workload
    )

    add(
        "Brave (Research)",
        "Education",
        random.randint(brave_research_min, brave_research_max) * workload
    )

    add(
        "Gmail",
        "Productivity",
        random.randint(10, 20)
    )

    # ---------------------------------------
    # WEEKDAY / WEEKEND
    # ---------------------------------------

    if weekend:

        add(
            "VS Code",
            "Coding",
            random.randint(60, 140)
        )

        add(
            "GitHub",
            "Coding",
            random.randint(github_min, github_max)
        )

        add(
            "Brave (Streaming)",
            "Entertainment",
            random.randint(150, 240)
        )

        add(
            "YouTube",
            "Entertainment",
            random.randint(100, 180)
        )

    else:

        add(
            "VS Code",
            "Coding",
            random.randint(vscode_min, vscode_max) * workload
        )

        add(
            "GitHub",
            "Coding",
            random.randint(github_min, github_max)
        )

        add(
            "Brave (Streaming)",
            "Entertainment",
            random.randint(30, 60)
        )

        add(
            "YouTube",
            "Entertainment",
            random.randint(15, 40)
        )

    # ---------------------------------------
    # MIRAI INTERNSHIP
    # Monday Wednesday Friday
    # ---------------------------------------

    if weekday in [0, 2, 4]:

        add(
            "Zoom",
            "Communication",
            90
        )

    # ---------------------------------------
    # GOOGLE COLAB
    # Tuesday Thursday Saturday
    # ---------------------------------------

    if weekday in [1, 3, 5]:

        add(
            "Google Colab",
            "Coding",
            random.randint(50, 70)
        )

    # ---------------------------------------
    # GOOGLE DOCS
    # Wednesday Friday
    # ---------------------------------------

    if weekday in [2, 4]:

        add(
            "Google Docs",
            "Productivity",
            random.randint(15, 25)
        )

    # ---------------------------------------
    # MICROSOFT TEAMS
    # Very Rare
    # ---------------------------------------

    if random.random() < 0.15:

        add(
            "Microsoft Teams",
            "Communication",
            random.randint(5, 10)
        )

    # Highest usage first

    day_entries.sort(
        key=lambda x: x[4],
        reverse=True
    )

    rows.extend(day_entries)

# ---------------------------------------

df = pd.DataFrame(
    rows,
    columns=[
        "Date",
        "Day",
        "App_Name",
        "Category",
        "Minutes_Used"
    ]
)

df.to_csv(
    "screentime.csv",
    index=False
)

print("=" * 70)
print("Life-OS Dataset Generated Successfully!")
print("=" * 70)
print(df.head(20))
print("=" * 70)

print("\nCategory Totals\n")
print(df.groupby("Category")["Minutes_Used"].sum())

print("\nTop Apps\n")
print(df.groupby("App_Name")["Minutes_Used"].sum().sort_values(ascending=False))

print("\nDaily Totals\n")
print(df.groupby("Date")["Minutes_Used"].sum())

print("=" * 70)

print(f"Rows Generated : {len(df)}")
print(f"Days Covered   : {NUM_DAYS}")
print("Output File    : screentime.csv")

print("=" * 70)