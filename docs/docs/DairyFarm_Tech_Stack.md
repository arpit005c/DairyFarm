# DairyFarm — Technology Stack

| Area | Technology |
|---|---|
| Primary language | Python |
| Database | PostgreSQL |
| Markup | HTML5 |
| Styling | CSS3 |
| UI framework | Bootstrap 5.3.3 |
| Client-side programming | Vanilla JavaScript |
| Numerical/data analysis | NumPy |
| Notebook | Jupyter Notebook |
| Analytics UI | Streamlit |
| IDE | VS Code |
| Version control | Git |

## Architecture Constraint
Stay within the approved stack. Do not introduce unnecessary alternatives such as React, Vue, Angular, Node.js, Express, MongoDB, Firebase, Supabase, Axios, jQuery, Tailwind, Material UI, or another backend framework unless the actual project specification explicitly requires and approves it.

## Database Rule
Frontend JavaScript must never connect directly to PostgreSQL.

Correct:
`Frontend → HTTP/API → Application → Service → Repository → PostgreSQL`

Incorrect:
`Frontend JavaScript → PostgreSQL`
