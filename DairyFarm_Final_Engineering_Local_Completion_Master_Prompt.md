# DairyFarm — Final Engineering Gap Closure & Local QA Master Prompt

## Phase — Local Completion Before Deployment

You are working on:

```text
C:\DairyFarm
```

Project:

**DairyFarm — Smart Milk Production, Expense & Analytics System**

Your role is:

- Senior Software Engineer
- Senior Backend Engineer
- Senior Frontend Engineer
- Senior PostgreSQL Engineer
- Senior QA Engineer
- Senior DevOps/Deployment-readiness Engineer
- MNC/SaaS mentor

Your task is to bring the CURRENT DairyFarm project to a fully verified, locally complete, deployment-ready state.

## CRITICAL RULE

> **LOCAL FIRST. DEPLOYMENT LATER.**

Do NOT begin Supabase, Render, Vercel, Streamlit Cloud, Docker, or any other deployment work during this phase.

First make the complete project work correctly and consistently on the local machine.

---

# 1. MANDATORY PROJECT AUDIT FIRST

Before modifying anything:

1. Inspect the entire project:
   - `backend/`
   - `frontend/`
   - `database/`
   - `docs/`
   - `tests/`
   - configuration files
   - `dashboard.py`
   - `requirements.txt`
   - `.env`
   - `.gitignore`
   - README if present
   - Git state

2. Read the entire relevant `docs/` directory.

3. Read and reconcile:
   - requirements
   - architecture
   - database design
   - API documentation
   - data-science documentation
   - testing documentation
   - theme/UI documentation
   - phase documentation
   - remaining-phase documentation
   - deployment documentation
   - technology-stack constraints

4. Treat the actual repository and documentation as the source of truth.

5. Do NOT silently replace project rules with generic best practices.

6. Before coding, produce a short audit containing:
   - current architecture
   - current completed features
   - current known gaps
   - files likely to change
   - proposed implementation order

Do not start implementation until the audit is complete.

---

# 2. APPROVED TECHNOLOGY STACK

Follow the project documentation.

## Main Frontend

- HTML5
- CSS3
- Bootstrap 5.3.3
- Bootstrap Icons
- Vanilla JavaScript

## Frontend Visualization

### APPROVED FOR THIS PROJECT

**Chart.js**

Chart.js is explicitly approved for the DairyFarm frontend visualization layer for this phase.

Use it through the existing frontend approach, such as CDN delivery, unless the repository already provides another approved integration.

Do NOT replace Chart.js with:
- React
- Vue
- Angular
- Plotly.js
- other unnecessary chart frameworks

## Backend

- Python
- Python standard library `http.server`
- Existing Application / Service / Repository architecture

## Database

- PostgreSQL

## Analytics

- NumPy
- Jupyter Notebook
- Streamlit

## Development

- VS Code
- Git
- GitHub

---

# 3. STRICTLY PROHIBITED

Do NOT introduce:

- React
- Vue
- Angular
- Django
- Flask
- FastAPI
- Node.js
- Express.js
- MongoDB
- Firebase
- Supabase during this local-completion phase
- unnecessary ORMs
- unnecessary frontend frameworks
- unnecessary backend frameworks
- unnecessary cloud services
- unnecessary architectural rewrites

Do NOT replace PostgreSQL.

Do NOT replace `http.server`.

---

# 4. CURRENT PROJECT STATE

The project already contains major completed work:

- layered Python backend
- PostgreSQL database
- frontend HTML/CSS/Bootstrap/Vanilla JS
- Fetch API
- async/await
- validation
- loading/success/error states
- HTTP API
- error mapping:
  - 400
  - 404
  - 409
  - 500
- centralized DB error translation
- NumPy analytics
- Advanced OOP analytics
- Jupyter notebook
- Streamlit dashboard
- frontend SPA redesign
- `/api/analytics`
- Chart.js integration
- Dashboard V2 styling
- manual testing
- 71 passing tests reported previously

However, this phase exists because the project audit identified important local-completion gaps.

---

# 5. P0 — COMPLETE THE HTTP CRUD API

The backend Application/Service/Repository layers already support CRUD operations.

The HTTP layer must expose them consistently.

For each resource:

- Farmers
- Cattle
- Milk Records
- Feed Records
- Expenses
- Revenue

verify and implement the necessary HTTP operations:

```text
GET collection
GET single resource
POST
PUT
DELETE
```

Use appropriate routes such as:

```text
GET    /api/farmers
GET    /api/farmers/{id}
POST   /api/farmers
PUT    /api/farmers/{id}
DELETE /api/farmers/{id}
```

and equivalent routes for the other modules.

IMPORTANT:

- Reuse existing Application classes.
- Reuse existing Services.
- Reuse existing Repositories.
- Do NOT add business logic to `main.py`.
- Keep routing lightweight and standard-library based.
- Do NOT introduce Flask/FastAPI/etc.

---

# 6. HTTP STATUS CONTRACT

Preserve the Phase 15D error model:

```text
200 → successful read/update where appropriate
201 → successful creation
400 → validation error
404 → resource not found
409 → duplicate/conflict
500 → unexpected internal failure
```

Do not expose:

- PostgreSQL exception details
- SQL
- stack traces
- credentials
- internal file paths

Return consistent JSON responses.

---

# 7. P0 — COMPLETE FRONTEND CRUD

The SPA must provide real browser functionality for:

- Farmers
- Cattle
- Milk Production
- Feed
- Expenses
- Revenue

For each module, verify:

```text
Create
Read
Update
Delete
```

where supported by the requirements and current Application layer.

The UI should provide:

- Bootstrap modal or drawer for Add/Edit
- Bootstrap buttons
- responsive tables
- action buttons
- loading state
- success state
- error state
- empty state
- confirmation for destructive operations

Do NOT merely make the buttons visually present.

Each action must perform a real API operation.

---

# 8. P0 — REMOVE HARDCODED LOCALHOST API URLS

Audit `frontend/js/app.js` and all frontend JavaScript.

Find hardcoded references such as:

```text
http://localhost:8000
127.0.0.1:8000
```

Do NOT hardcode production values yet.

Create a clean local configuration mechanism for the API base URL.

Example concept:

```javascript
const API_BASE_URL = window.DAIRYFARM_API_BASE_URL || "http://localhost:8000";
```

The exact implementation should follow the existing architecture and browser constraints.

Rules:

- local development must continue working
- frontend must not directly connect to PostgreSQL
- API base URL must be changeable later for deployment
- do not introduce a frontend build framework

---

# 9. P0 — CONFIGURABLE BACKEND PORT

Inspect `backend/app/main.py`.

If the backend currently uses a fixed port only, change it to support:

```text
PORT environment variable
```

with a local fallback such as:

```text
8000
```

Expected concept:

```text
PORT exists → use it
otherwise → 8000
```

Keep:

```powershell
.venv\Scripts\python.exe -m backend.app.main
```

working locally.

Do NOT introduce WSGI/ASGI frameworks.

---

# 10. P0 — ANALYTICS API VERIFICATION

Verify:

```text
GET /api/analytics
```

works correctly.

It must reuse:

```text
AnalyticsOrchestrator
```

and must NOT duplicate NumPy/business calculations.

Verify:

- KPI data
- chart data
- JSON serialization
- empty-data behavior
- error behavior

---

# 11. CHART.JS — APPROVED VISUALIZATION STACK

Use **Chart.js** for the main web frontend charts.

The dashboard should contain, where data supports it:

## Milk Production Trend

- date axis
- production series
- readable labels
- responsive chart
- empty-state handling

## Financial Overview

- revenue
- expenses
- optional net profit if supported cleanly

Do not fabricate data.

Do not calculate business analytics in JavaScript.

JavaScript should only transform the backend JSON into Chart.js presentation data.

---

# 12. REAL ANALYTICS ONLY

Do NOT use fake or mock metrics.

Particularly review:

- KPI delta percentages
- "vs last month"
- production trend claims
- profit insights
- financial insights

If historical data is not available to calculate a value:

- remove the metric, OR
- clearly label it unavailable

Do NOT display fake percentages such as:

```text
↑ 8.2%
↑ 12.4%
```

unless they are actually calculated from real data.

Do not present hardcoded insights as data-driven insights.

---

# 13. DASHBOARD KPI REQUIREMENTS

Where the real data supports them, verify:

- Total Milk Production
- Total Revenue
- Total Expenses
- Net Profit
- Total Cattle
- Today's Milk Production
- Monthly Milk Production
- Total Feed Cost

Do NOT invent missing metrics.

If a required metric is not currently available from the analytics architecture:

1. identify the gap,
2. determine whether the existing repositories can provide the required data,
3. extend the analytics layer minimally and cleanly if justified,
4. add tests,
5. do not duplicate calculations in the frontend.

---

# 14. STREAMLIT DASHBOARD

The Streamlit dashboard must remain functional.

Verify:

```powershell
.venv\Scripts\python.exe -m streamlit run dashboard.py
```

Check:

- Light theme
- KPI cards
- tabs
- charts
- analytics data
- empty states
- no deprecation warnings
- no raw database errors

Do NOT redesign Streamlit in this phase unless there is a real bug.

---

# 15. P0 — CLEAN `requirements.txt`

Audit `requirements.txt`.

The final local requirements file must:

- use UTF-8
- contain direct project dependencies
- avoid unnecessary transitive-package dumping
- include only required packages
- include Streamlit
- include NumPy
- include Jupyter if required by the project
- include PostgreSQL driver
- include pytest
- include python-dotenv if used
- include any other direct package actually imported by the project

Chart.js and Bootstrap are frontend assets and should not be incorrectly added as Python packages.

Do not remove a dependency until you prove it is unnecessary.

Verify installation in a clean environment if practical.

---

# 16. P0 — API TEST COVERAGE

Extend API tests.

At minimum test:

## Analytics

```text
GET /api/analytics → 200
```

## CRUD

For each resource:

```text
GET collection
GET single
POST
PUT
DELETE
```

## Error handling

Test:

```text
400 validation
404 not found
409 duplicate
500 unexpected
```

Test response JSON structure, not only status codes.

Do not reduce existing test coverage.

---

# 17. P1 — HARDEN MANUAL QA SCRIPT

Inspect:

```text
test_manual_simulation.py
```

The script must fail fast when the backend is unavailable.

Desired behavior:

```text
Backend unavailable
        ↓
Clear error
        ↓
Exit with failure code
```

Do not continue into secondary `NameError` or unrelated failures.

The manual test should report:

- valid operations
- invalid operations
- duplicate operations
- database verification
- expected HTTP status
- overall pass/fail

---

# 18. P1 — FRONTEND VALIDATION CONSISTENCY

The frontend should proactively validate required fields before sending requests.

Examples:

- empty date
- empty required string
- invalid numeric value
- negative quantity
- invalid ID

The backend remains the authoritative validation layer.

Frontend validation is for UX, not security.

---

# 19. P1 — API RESPONSE CONSISTENCY

Audit all endpoints and ensure responses follow a predictable structure.

Example:

```json
{
  "success": true,
  "data": {}
}
```

or the project's existing documented response structure.

Do not introduce multiple inconsistent formats.

If changing the response structure would break existing frontend/tests, preserve the established format and document it.

---

# 20. P1 — FRONTEND SPA QA

Verify:

### Navigation

- Dashboard
- Farmers
- Cattle
- Milk
- Feed
- Expenses
- Revenue

### Data loading

- collection loads
- loading state
- empty state
- error state

### CRUD

- create
- read
- update
- delete

### Modals

- open
- close
- cancel
- submit
- reset

### Tables

- data renders
- action buttons work
- responsive behavior works

---

# 21. RESPONSIVE QA

Manually test:

- desktop
- laptop
- tablet
- mobile

Check:

- sidebar
- cards
- tables
- modals
- buttons
- charts
- form layout

No horizontal page overflow.

---

# 22. ACCESSIBILITY QA

Check:

- semantic structure
- labels
- keyboard navigation
- visible focus
- color contrast
- accessible buttons
- accessible modal behavior
- meaningful error messages

Respect reduced-motion preferences.

---

# 23. SECURITY QA

Verify:

- `.env` excluded from Git
- no credentials in source
- no credentials in notebooks
- no credentials in README
- no credentials in screenshots/docs
- frontend cannot access PostgreSQL directly
- user input remains validated
- SQL remains parameterized
- backend error responses do not leak internal information

---

# 24. DATABASE QA

Verify the actual local `DairyFarmDB`.

Check:

- schema
- constraints
- foreign keys
- unique constraints
- seed data
- CRUD integrity

For each successful browser operation, verify the database state manually.

Do not modify the schema unless a genuine functional requirement requires it.

---

# 25. GIT QA

Before changes:

```powershell
git status
```

Inspect:

```powershell
git diff
```

After implementation:

```powershell
git status
git diff
```

Review all modified files.

Do not commit automatically.

Do not discard user changes.

---

# 26. LOCAL TEST MATRIX

Before declaring this phase complete, verify all of the following locally.

## Backend

- [ ] starts successfully
- [ ] configurable PORT works
- [ ] all routes work
- [ ] JSON works
- [ ] CORS works
- [ ] error mapping works

## Frontend

- [ ] SPA loads
- [ ] Bootstrap loads
- [ ] Chart.js loads
- [ ] sidebar works
- [ ] all views work
- [ ] forms work
- [ ] modals work
- [ ] CRUD works

## Database

- [ ] PostgreSQL connects
- [ ] inserts verified
- [ ] updates verified
- [ ] deletes verified
- [ ] constraints verified
- [ ] duplicates rejected correctly

## Analytics

- [ ] `/api/analytics`
- [ ] KPI values correct
- [ ] Chart.js values correct
- [ ] NumPy calculations unchanged
- [ ] Streamlit works

## QA

- [ ] 400 tested
- [ ] 404 tested
- [ ] 409 tested
- [ ] 500 tested
- [ ] manual test script works
- [ ] responsive QA
- [ ] accessibility QA
- [ ] console has no unexpected errors

---

# 27. AUTOMATED TEST GATE

Before completion run:

```powershell
.venv\Scripts\python.exe -m pytest -v
```

Do not claim completion until the result is actually verified.

Target:

```text
71+ passed
0 failed
```

The count may increase because new tests should be added.

Report the exact final count.

---

# 28. LOCAL END-TO-END TEST

Run the complete local system:

### Terminal 1

```powershell
.venv\Scripts\python.exe -m backend.app.main
```

### Terminal 2

Use the project’s normal frontend serving method.

### Terminal 3

```powershell
.venv\Scripts\python.exe -m streamlit run dashboard.py
```

Then verify:

```text
Browser
  ↓
SPA
  ↓
Fetch
  ↓
http.server
  ↓
Application
  ↓
Service
  ↓
Repository
  ↓
PostgreSQL
```

and separately:

```text
PostgreSQL
  ↓
AnalyticsOrchestrator
  ↓
NumPy
  ↓
Streamlit
```

---

# 29. DOCUMENTATION — LOCAL COMPLETION ONLY

Update the appropriate docs to reflect the ACTUAL current state.

At minimum review:

- README
- architecture
- API
- database
- testing
- data science
- deployment
- phase status

Correct outdated statements.

Do NOT document deployment as complete.

Document:

> Local system verified; deployment intentionally deferred.

---

# 30. FINAL LOCAL COMPLETION REPORT

At the end report:

## Architecture

Explain the final local architecture.

## Files Created

List every new file.

## Files Modified

List every modified file.

## APIs Added/Changed

List all routes.

## Test Result

```text
Previous:
71 tests

Current:
<actual number> passed
```

## Manual QA

Report:

- CRUD
- validation
- duplicates
- database verification
- analytics
- responsive UI
- accessibility
- error handling

## Known Limitations

Only real limitations.

## Deployment Readiness

State:

```text
LOCAL COMPLETE — DEPLOYMENT NOT STARTED
```

or:

```text
LOCAL INCOMPLETE
```

Do not claim production readiness unless the local acceptance criteria are all satisfied.

---

# 31. DEPLOYMENT BOUNDARY

This phase ends BEFORE deployment.

DO NOT:

- create Supabase project
- migrate local PostgreSQL to Supabase
- deploy Render
- deploy Vercel
- deploy Streamlit
- create Docker production infrastructure
- create cloud-specific secrets
- change production DNS
- modify architecture for a cloud platform

Those are separate future tasks after local sign-off.

---

# 32. FINAL DECISION RULE

Do not move forward because:

- the UI looks good
- tests pass
- Streamlit opens

Move forward only when:

```text
Backend
+
Frontend
+
Database
+
Analytics
+
CRUD
+
Validation
+
Error handling
+
Manual QA
+
Automated QA
+
Documentation
```

all pass locally.

---

# 33. END CONDITION

The final state of this phase must be:

```text
              LOCAL DAIRYFARM
                    │
        ┌───────────┴────────────┐
        │                        │
   Main Web App             Streamlit
        │                        │
      Fetch                 Analytics
        │                        │
   http.server             NumPy/OOP
        │                        │
        └──────────┬─────────────┘
                   │
               PostgreSQL
```

with:

```text
71+ tests passing
manual QA passing
no known P0 defects
no fake analytics
no broken CRUD
no hardcoded deployment URLs
no deployment performed yet
```

Only after this local acceptance gate passes should the project move to a separate deployment phase.

## START

Begin with:

**STEP 1 — COMPLETE PROJECT + DOCUMENTATION AUDIT**

Do not modify code before the audit is complete.
