# Gemini AI Integration & Prompt Engineering Strategy

## 1. Overview
The AI engine utilizes the official **`google-genai` SDK** with the `gemini-2.5-flash` model to deliver high-speed, cost-effective, recruiter-grade analysis.

## 2. API Call Optimization & Form Control
- **`st.form` Batching**: Inputs (Resume + Job Description) are contained inside an `st.form` container so API calls only execute when the user explicitly clicks **"Roast & Analyze Resume"**.
- **State Caching**: API outputs are cached directly in `st.session_state["analysis_json"]`. Subsequent UI tab navigations or template choices trigger ZERO duplicate API requests.

## 3. System Prompt & Persona Design
The Gemini engine is instructed via a strict system prompt to act as a **Silicon Valley Tech Recruiter**:
- Direct, witty, constructive "roast" style.
- Highlights vague bullet points lacking quantitative metrics (e.g., "Responsible for writing code").
- Recommends strong action verbs (e.g., "Architected", "Engineered", "Optimized").

## 4. Structured Output Format (JSON Schema)
To ensure reliable parsing, Gemini requests enforce structured JSON output:

```json
{
  "overall_score": 78,
  "match_percentage": 82,
  "recruiter_roast": "Your resume reads like a generic laundry list...",
  "strengths": ["Strong FastAPI experience", "Clear education section"],
  "critical_gaps": ["Missing Kubernetes keywords", "No metrics for database optimization"],
  "bullet_point_improvements": [
    {
      "original": "Worked on React microservices",
      "improved": "Engineered 4 enterprise React microservices handling 50k DAU with 99.9% uptime"
    }
  ]
}
```

## 5. Error & Fallback Handling
- **API Key Fallback**: Checks `st.secrets["GEMINI_API_KEY"]` first, falling back gracefully to environment variables `GEMINI_API_KEY`.
- **JSON Recovery**: If output parsing fails, fallback regular expressions extract structured blocks cleanly.
