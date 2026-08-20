# DairyFarm — Architecture & Workflow

## Main Architecture

```text
USER
  ↓
PRESENTATION
HTML5 + CSS3 + Bootstrap + Vanilla JavaScript
  ↓
API / HTTP
  ↓
APPLICATION LAYER
  ↓
SERVICE LAYER
  ↓
REPOSITORY LAYER
  ↓
POSTGRESQL
```

## Analytics Architecture

```text
Project Data / PostgreSQL
        ↓
      Python
        ↓
      NumPy
        ↓
Jupyter Notebook
        ↓
Data Analysis
        ↓
Streamlit
        ↓
Analytics / Visualization
```

## Layer Responsibilities

### Presentation
UI, responsive layout, forms, DOM interaction, validation, loading/success/error feedback.

### API / HTTP
Communication boundary between frontend and backend. Inspect the actual project before assuming a specific framework.

### Application
Coordinates application-level operations and delegates business operations to services.

### Service
Contains business rules and domain operations.

### Repository
Handles persistence and database operations.

### PostgreSQL
Persistent relational database.

## Development Workflow

```text
Read phase specification
↓
Inspect actual files
↓
Understand architecture
↓
Map requirements to syllabus
↓
Plan
↓
Implement small step
↓
Test
↓
Verify
↓
Regression test
↓
Review Git changes
↓
Commit
↓
Confirm clean working tree
```

## Safety
- Never overwrite working files blindly.
- Never duplicate completed functionality.
- Never hide test failures.
- Never introduce unnecessary frameworks.
- Stop when an architectural dependency is missing instead of guessing.
