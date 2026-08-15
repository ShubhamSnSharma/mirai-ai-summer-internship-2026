# Assignment 4 — Upgrading the AI Image Studio

**Track:** MirAI School of Technology — Virtual Summer Internship 2026 (AI Builder)  
**Deadline:** August 25, 2026, 11:59 PM  

---

## Objective

Debug and extend the AI Image Studio prototype: fix broken slider parameters, correct the file download extension, and add two new UX features — "Magic Enhance" and "Surprise Me!".

---

## Tasks Completed

### Task 1 — The Broken Sliders Fix (URL Parameters)
- Width and height sliders now inject correctly into the Pollinations API URL:
  ```
  https://image.pollinations.ai/prompt/{full_prompt}?width={width}&height={height}
  ```

### Task 2 — The File Extension Fix
- `file_name` updated to `f"{art_style}_image.png"` so downloaded files open correctly as images.

### Task 3 — The "Magic Enhance" Toggle ✨
- `st.sidebar.checkbox("✨ Enable Magic Enhance")` added to the sidebar.
- When checked, appends boost words to the prompt:
  ```
  ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"
  ```

### Task 4 — The "Surprise Me!" Feature 🎲
- Imported Python's built-in `random` module.
- A list of 5 creative prompts defined.
- `st.button("🎲 Surprise Me!")` selects a random prompt via `random.choice()` and generates the image instantly.

---

## Tech Stack
- Python
- Streamlit
- Pollinations AI (Image Generation API)
- `random` (stdlib)

---

## Run Locally

```bash
pip install streamlit requests
streamlit run assignment4.py
```

---

*Built as part of the MirAI School of Technology Virtual Summer Internship 2026.*
