# Assignment 1 — The Identity Echo Interface

**Track:** MirAI School of Technology — Virtual Summer Internship 2026 (AI Builder)  
**Deadline:** August 25, 2026, 11:59 PM  

---

## Objective

Build an interactive Streamlit web interface that collects multiple data inputs from a user, waits for an execution command, and conditionally processes that data.

---

## Tasks Completed

### Task 1 — The UI Shell
- Initialized Streamlit application with `st.title()` and `st.write()`.

### Task 2 — Multi-Data Collection
- `st.text_input()` for **Name** and **Message** fields.

### Task 3 — The Action Gate
- Single `st.button("Transmit")` trigger; all output logic runs only when clicked.

### Task 4 — Conditional Routing (Edge Cases)
- Empty **Name** → `st.error("Please provide your name.")`
- Empty **Message** → `st.warning("Please type a message to transmit.")`

### Task 5 — The Formatted Output
- Both fields valid → `st.success("Transmission successful! Greetings, [Name]. We received your message: [Message]")`

### Advanced Challenge — Token Cost Estimator ✅
- Calculates character length and estimated token count of the message (`len(message) / 4`).
- Displays result via `st.info()`.

---

## Tech Stack
- Python
- Streamlit

---

## Run Locally

```bash
pip install streamlit
streamlit run assignment1.py
```

---

*Built as part of the MirAI School of Technology Virtual Summer Internship 2026.*
