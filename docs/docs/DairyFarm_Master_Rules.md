# DairyFarm — Master Rules

## Source of Truth
Actual project files are the highest-priority source of truth.

If historical notes and current files differ:
1. Inspect current files.
2. Report the difference.
3. Do not blindly overwrite working code.

## Architecture

```text
Presentation
↓
API / HTTP
↓
Application
↓
Service
↓
Repository
↓
PostgreSQL
```

## Technology
Python + PostgreSQL + HTML5 + CSS3 + Bootstrap 5.3.3 + Vanilla JavaScript + NumPy + Jupyter Notebook + Streamlit.

## Never
- rebuild completed phases
- duplicate business logic
- connect browser code directly to PostgreSQL
- expose secrets
- introduce unnecessary frameworks
- skip tests
- ignore failures
- make large blind rewrites
- invent APIs without inspection
- bring later-phase data science features into an earlier phase

## Quality
The project should be modular, readable, maintainable, responsive, tested, syllabus-aligned, professionally presented, and suitable for final live deployment.

## Deployment Goal
Prepare the project for live deployment after functionality, testing, configuration, and documentation are complete.
