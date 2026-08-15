# 🖥️ GitHub Profile — Hacker Terminal Interface

> A custom neofetch-inspired terminal profile built with Markdown, ASCII art, and live GitHub stats.

---

## Live Profile

👉 **[github.com/ShubhamSnSharma](https://github.com/ShubhamSnSharma)**

---

## What It Does

This assignment unlocks GitHub's hidden **profile README** feature — a special repository named exactly after your username (`ShubhamSnSharma`) whose `README.md` becomes your public profile homepage.

The profile is designed to look like a **terminal / neofetch interface**, featuring:

- 🎨 **ASCII Art Portrait** — a custom ASCII rendering of a profile avatar, generated with AI
- 💻 **System Info Bio** — biography written as terminal key-value pairs (OS, Kernel, Languages, Hobbies, Contact)
- ⌨️ **Typing Animation** — animated Fira Code typewriter banner via `readme-typing-svg`
- 📊 **Dynamic GitHub Stats** — live commit, PR, and star data via [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) by Anurag Hazra
- 🛠️ **Tech Stack SVG** — custom development environment dashboard

---

## How It Was Built

### Task 1 — Unlock the Secret Repository
Created a new GitHub repository named **`ShubhamSnSharma`** (exactly matching the GitHub username). GitHub surfaces a special message and this repo's `README.md` becomes the profile homepage.

### Task 2 — The Terminal Canvas
The entire ASCII section is wrapped in a ` ```txt ` Markdown code block — giving it a dark, monospaced, terminal-like appearance on GitHub.

### Task 3 — ASCII Art Portrait
Custom ASCII art portrait generated using AI, embedded in the left column of the terminal layout alongside the system info.

### Task 4 — System Info Bio
```
shubham@home
------------------------------------------
OS: ........... macOS
Uptime: ....... 22 years, 5 months
Host: ......... Bennett University
Kernel: ....... B.Tech Computer Science & Engineering
Languages: .... Python, C++, SQL
Hobbies: ...... Badminton, Vibe Coding, Movies
Location: ..... Greater Noida, India
Contact: ...... shubhamsnsharma@gmail.com
------------------------------------------
Focus: ........ Machine Learning & AI
Approach: ..... Build → Deploy → Improve
Goal: ......... ML Engineering
GitHub: ....... @ShubhamSnSharma
Portfolio: .... shubhamsn.vercel.app

shubham@home:~$ █
```

### Task 5 — Dynamic GitHub Stats
Integrated **[github-readme-stats](https://github.com/anuraghazra/github-readme-stats)** for live stats that auto-update on every profile visit.

---

## Tech Used

| Element | Tool |
|---|---|
| Terminal layout | Markdown ` ```txt ` code block |
| Typing animation | [readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg) |
| Live GitHub stats | [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) |
| ASCII art | AI-generated (Gemini) |

---

*Built as part of the MirAI School of Technology — Virtual Summer Internship 2026.*
