# Assignment 3 — The Memory Vault (Stateful Chatbot)

**Track:** MirAI School of Technology — Virtual Summer Internship 2026 (AI Builder)  
**Deadline:** August 25, 2026, 11:59 PM  

---

## Objective

Upgrade the AI Multiverse chatbot from a **stateless** app (forgets everything on rerun) to a **stateful** app (remembers full conversation history) using Streamlit's `st.session_state`.

---

## Tasks Completed

### Task 1 — Initialize the Memory Vault
- Checks if `"messages"` exists in `st.session_state` at startup.
- Initializes `st.session_state.messages = []` if not present.

### Task 2 — Render the Chat History
- `for` loop iterates through `st.session_state.messages`.
- Each message rendered with `st.chat_message(role)` so history is redrawn on every rerun.

### Task 3 — Upgrade the Input UI
- Replaced `st.text_input()` + `st.button("SEND")` with `st.chat_input("Say something...")`.
- Used the walrus operator (`:=`) for single-line assignment and check.

### Task 4 — Save New Messages to Memory
- User message appended to `st.session_state.messages` as `{"role": "user", "content": user_message}`.
- AI response appended as `{"role": "assistant", "content": response.text}`.

---

## Tech Stack
- Python
- Streamlit
- Google Gemini API (`google-genai`)
- python-dotenv

---

## Run Locally

```bash
pip install streamlit google-genai python-dotenv
# Create a .env file with: GEMINI_API_KEY=your_key_here
streamlit run assignment3.py
```

---

*Built as part of the MirAI School of Technology Virtual Summer Internship 2026.*
