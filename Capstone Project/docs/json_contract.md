# Application Data Contract Specification (`json_contract.md`)

## Executive Summary
This document serves as the official, frozen API data contract for **The AI Resume Critic**. The entire application operates off **ONE unified structured JSON object** returned by Gemini 2.5 Flash (or supplied by `data/mock_analysis.json` during development).

Every downstream feature—including the Recruiter Dashboard, ATS Analysis, Resume Optimizer, Resume Builder, Template Gallery, and PDF/DOCX Export Engine—consumes this exact contract.

---

## Data Pipeline Architecture

```text
User Input (Resume + Job Description)
               │
               ▼
   Gemini API (gemini-2.5-flash)
               │
               ▼
   Structured Analysis JSON (Single Source of Truth)
               │
   ┌───────────┼───────────┬───────────┬───────────┐
   ▼           ▼           ▼           ▼           ▼
Dashboard  ATS Specs  Optimizer  Templates  PDF/DOCX
```

---

## Top-Level Schema Overview

```json
{
  "metadata": {},
  "builder": {},
  "candidate": {},
  "job": {},
  "scores": {},
  "ats_analysis": {},
  "skills_analysis": {},
  "experience_analysis": [],
  "projects_analysis": [],
  "bullet_analysis": [],
  "summary_analysis": {},
  "keyword_analysis": {},
  "strengths": [],
  "weaknesses": [],
  "recommendations": [],
  "optimized_resume": {},
  "recruiter_feedback": {}
}
```

---

## Detailed Schema Field Specifications

### 1. `metadata`
- **Purpose**: System execution tracking, model info, and template compatibility.
- **Type**: `dict`
- **Used By**: App Header, System Diagnostics, Export Engine.

| Field Name | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `analysis_timestamp` | `str` | `"2026-08-14T22:15:00Z"` | ISO-8601 timestamp of analysis execution. |
| `model` | `str` | `"gemini-2.5-flash"` | Gemini model version utilized. |
| `analysis_version` | `str` | `"1.0.0-phase2.5"` | Schema version string. |
| `processing_time_seconds` | `float` | `1.42` | Total AI execution latency in seconds. |
| `supported_templates` | `List[str]` | `["ATS Friendly (Clean)", ...]` | List of valid template names compatible with output. |

---

### 2. `builder`
- **Purpose**: Metadata for resume document generation and page estimation.
- **Type**: `dict`
- **Used By**: Resume Builder, Template Gallery, Export Engine.

| Field Name | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `recommended_template` | `str` | `"ATS Friendly (Clean)"` | Recommended layout template for this candidate profile. |
| `ats_safe` | `bool` | `True` | Flag indicating 100% ATS parser safety. |
| `estimated_pages` | `int` | `1` | Estimated page length of generated document. |
| `export_ready` | `bool` | `True` | Readiness indicator for PDF/DOCX generation. |

---

### 3. `candidate`
- **Purpose**: Extracted contact details and online profile links.
- **Type**: `dict`
- **Used By**: Header, Resume Builder, PDF/DOCX Templates.

| Field Name | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | `"Alex Chen"` | Candidate full name. |
| `email` | `str` | `"alex.chen@email.com"` | Candidate primary email. |
| `phone` | `str` | `"(555) 019-2834"` | Phone number. |
| `location` | `str` | `"San Francisco, CA"` | Geographic location. |
| `linkedin` | `str` | `"linkedin.com/in/alexchen-tech"` | LinkedIn profile URL or handle. |
| `github` | `str` | `"github.com/alexchen-dev"` | GitHub profile handle. |
| `portfolio` | `str` | `"alexchen.dev"` | Portfolio website URL. |

---

### 4. `job`
- **Purpose**: Extracted requirements from target job description.
- **Type**: `dict`
- **Used By**: Dashboard Context, Match Analyzer.

| Field Name | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `company` | `str` | `"Apex Innovations Inc."` | Employer company name. |
| `role` | `str` | `"Senior Full Stack AI Engineer"` | Target job title. |
| `industry` | `str` | `"Enterprise Software & AI"` | Target industry sector. |
| `experience_required` | `str` | `"3+ years"` | Mandatory experience level. |
| `education_required` | `str` | `"B.S. or M.S. in CS"` | Required degree. |
| `primary_skills` | `List[str]` | `["Python", "React", ...]` | Must-have technical skills. |
| `secondary_skills` | `List[str]` | `["Redis", "AWS", ...]` | Nice-to-have technical skills. |

---

### 5. `scores`
- **Purpose**: Quantitative match scores and breakdown metrics.
- **Type**: `dict`
- **Used By**: Recruiter Dashboard, Plotly Radar Charts, Dynamic KPI Cards.

| Field Name | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `overall_resume_score` | `int` | `82` | Weighted composite score (0-100). |
| `ats_score` | `int` | `85` | ATS compliance score. |
| `job_match_score` | `int` | `79` | Skill and experience match %. |
| `interview_probability` | `int` | `78` | Estimated callback probability %. |
| `skills_score` | `int` | `88` | Technical skill alignment score. |
| `experience_score` | `int` | `80` | Work experience depth score. |
| `projects_score` | `int` | `84` | Portfolio & project relevance score. |
| `education_score` | `int` | `90` | Academic background score. |
| `score_breakdown` | `dict` | `{"content": 85, "format": 91, ...}` | 5-axis breakdown for Plotly radar chart. |

---

### 6. `ats_analysis`
- **Purpose**: Parsability ratings and structural defect flags.
- **Type**: `dict`
- **Used By**: ATS Analysis Tab, Risk Badges.

| Field Name | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `format_score` | `int` | `91` | Document layout compliance score. |
| `readability_score` | `int` | `90` | Flesch/Readability metric. |
| `keyword_density` | `float` | `0.048` | Target keyword frequency ratio. |
| `parsing_risk` | `str` | `"Low"` | Risk classification ("Low", "Medium", "High"). |
| `missing_sections` | `List[str]` | `[]` | Omitted critical resume sections. |
| `ats_issues` | `List[str]` | `["Project metrics could..."]` | List of ATS parser formatting warnings. |

---

### 7. `skills_analysis`
- **Purpose**: Matched vs missing skills with AI confidence levels.
- **Type**: `dict`
- **Used By**: Skill Matrix Cards, Missing Keyword Badges.

| Field Name | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `matched_skills` | `List[dict]` | `[{"skill": "Python", "confidence": 98}]` | Matched technical skills + confidence %. |
| `missing_skills` | `List[dict]` | `[{"skill": "Kubernetes", "confidence": 85}]` | Missing target skills + confidence %. |
| `recommended_skills` | `List[str]` | `["Kubernetes", ...]` | Suggested additions for job fit. |
| `soft_skills_found` | `List[str]` | `["Developer Mentorship", ...]` | Extracted interpersonal skills. |
| `soft_skills_missing` | `List[str]` | `["Agile/Scrum Ownership"]` | Missing soft skills. |

---

### 8. `experience_analysis`
- **Purpose**: Detailed breakdown of work history entries.
- **Type**: `List[dict]`
- **Used By**: Experience Reviewer, Line-by-line Rewriter.

| Field Name | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `company` | `str` | `"CloudTech Solutions"` | Employer name. |
| `role` | `str` | `"Senior Full Stack Engineer"` | Job title held. |
| `strengths` | `List[str]` | `["Quantified outcome on..."]` | Highlighted bullet achievements. |
| `issues` | `List[str]` | `["Lacks specific mention..."]` | Flaws or missing metrics. |
| `improved_description` | `str` | `"Architected and deployed..."` | Rewritten high-impact experience paragraph. |

---

### 9. `projects_analysis`
- **Purpose**: Assessment of candidate side projects and open-source contributions.
- **Type**: `List[dict]`
- **Used By**: Project Reviewer.

| Field Name | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `project_name` | `str` | `"Smart-Resume-Optimizer"` | Project title. |
| `strengths` | `List[str]` | `["Open-source initiative..."]` | Strong aspects of project description. |
| `missing_metrics` | `List[str]` | `["GitHub stars, user stats"]` | Unquantified impact areas. |
| `missing_technologies` | `List[str]` | `["PyTest", "Docker"]` | Relevant missing tech stack tags. |
| `improved_description` | `str` | `"Architected an open-source..."` | Optimized project description text. |

---

### 10. `bullet_analysis`
- **Purpose**: Granular bullet point critique and line-by-line rewrites.
- **Type**: `List[dict]`
- **Used By**: Resume Optimizer Tab, Comparison Diff Viewers.

| Field Name | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `section` | `str` | `"Experience"` | Resume section origin. |
| `original` | `str` | `"Integrated OpenAI and Gemini APIs..."` | Original weak bullet string. |
| `issue` | `str` | `"Vague API integration description..."` | Identified flaw / weakness. |
| `improved` | `str` | `"Architected async GenAI..."` | Optimized high-impact action bullet. |
| `reason` | `str` | `"Adds technical architecture..."` | Rationale for the rewrite. |

---

### 11. `summary_analysis`
- **Purpose**: Professional summary critique and rewrite.
- **Type**: `dict`
- **Used By**: Summary Optimizer.

| Field Name | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `original_summary` | `str` | `"Results-driven Software Engineer..."` | Raw original candidate summary text. |
| `issues` | `str` | `"Good summary overall, but..."` | Critique of original summary. |
| `improved_summary` | `str` | `"Senior Full Stack AI Engineer..."` | Rewritten targeted executive summary. |

---

### 12. `keyword_analysis`
- **Purpose**: Keyword frequency and priority matrix.
- **Type**: `dict`
- **Used By**: Keyword Gap Editor (`st.data_editor`), Bar Charts.

| Field Name | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `matched_keywords` | `List[str]` | `["Python", "TypeScript", ...]` | Present job keywords. |
| `missing_keywords` | `List[str]` | `["Kubernetes", "GraphQL", ...]` | Missing critical keywords. |
| `high_priority_keywords` | `List[str]` | `["Gemini API", "FastAPI", ...]` | Must-have high impact keywords. |
| `low_priority_keywords` | `List[str]` | `["GraphQL", "Vue"]` | Secondary keywords. |

---

### 13. `strengths`
- **Purpose**: Bulleted list of candidate strengths.
- **Type**: `List[str]`
- **Used By**: Recruiter Dashboard.

---

### 14. `weaknesses`
- **Purpose**: Bulleted list of candidate weaknesses.
- **Type**: `List[str]`
- **Used By**: Recruiter Dashboard.

---

### 15. `recommendations`
- **Purpose**: Prioritized action items for candidate improvement.
- **Type**: `List[dict]`
- **Used By**: Action Items Cards.

| Field Name | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `severity` | `str` | `"Critical"` | Severity rating ("Critical", "High", "Medium", "Low"). |
| `priority` | `int` | `1` | Numerical sorting rank (1 = highest). |
| `category` | `str` | `"Experience"` | Functional domain ("Experience", "Keywords", "Projects"). |
| `title` | `str` | `"Highlight GenAI Pipeline Architecture"` | Concise action title. |
| `description` | `str` | `"Elaborate on LLM prompt engineering..."` | Detailed step-by-step guidance. |

---

### 16. `optimized_resume`
- **Purpose**: Complete, clean structured JSON representing the rewritten candidate resume.
- **Type**: `dict`
- **Used By**: Resume Builder, Template Engines (`templates/*.py`), PDF/DOCX Exporters.

```json
{
  "personal_information": { "name": "", "email": "", "phone": "", "location": "", "linkedin": "", "github": "", "portfolio": "" },
  "headline": "",
  "professional_summary": "",
  "experience": [ { "company": "", "location": "", "role": "", "start_date": "", "end_date": "", "bullets": [] } ],
  "projects": [ { "project_name": "", "tech_stack": [], "description": "" } ],
  "education": [ { "degree": "", "institution": "", "location": "", "graduation_date": "", "gpa": "" } ],
  "skills": { "languages": [], "frameworks": [], "databases": [], "tools": [], "cloud": [], "other": [] },
  "certifications": [],
  "achievements": [],
  "languages_spoken": [],
  "interests": []
}
```

---

### 17. `recruiter_feedback`
- **Purpose**: Recruiter verdict, decision, concerns, and roast summary.
- **Type**: `dict`
- **Used By**: Executive Feedback Banner, Recruiter Roast Section.

| Field Name | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `overall_verdict` | `str` | `"Strong Candidate for Senior Role"` | High-level candidate evaluation summary. |
| `hire_decision` | `str` | `"Strong Pursue / Move to Technical Onsite"` | Mock hiring manager decision. |
| `top_concerns` | `List[str]` | `["Needs explicit mention of..."]` | Key concerns raised during review. |
| `final_comments` | `str` | `"Alex presents a solid engineering..."` | Recruiter commentary / roast. |
