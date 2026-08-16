# DairyFarm — System Architecture

**Document:** System Architecture & Design  
**Project:** DairyFarm — Smart Milk Production, Expense & Analytics System  
**Phase:** Phase 2 — Architecture & System Design  
**Development Environment:** VS Code  
**Status:** Architecture Defined  
**Primary Language:** Python  
**Database:** PostgreSQL  

---

# 1. Architecture Overview

DairyFarm follows a lightweight layered architecture designed to keep the application understandable, maintainable, modular, and suitable for academic demonstration.

The architecture separates:

1. Presentation
2. Application
3. Business Logic
4. Data Access
5. Database
6. Data Science and Analytics

The system avoids unnecessary frameworks and follows the approved Phase 1 technology stack.

High-level architecture:

```text
                         ┌──────────────────────┐
                         │        USER          │
                         │ Farm Owner / Staff   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │      PRESENTATION LAYER       │
                    │                               │
                    │ HTML5 + CSS3 + Bootstrap     │
                    │ JavaScript                    │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │       APPLICATION LAYER       │
                    │                               │
                    │ Request Handling              │
                    │ Validation                    │
                    │ Application Services          │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │       BUSINESS LOGIC          │
                    │                               │
                    │ Farm Rules                    │
                    │ Production Rules              │
                    │ Expense Rules                 │
                    │ Revenue Rules                 │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │       DATA ACCESS LAYER       │
                    │                               │
                    │ Database Operations            │
                    │ Query Handling                 │
                    │ Transaction Handling           │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │          PostgreSQL            │
                    │            Database            │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │      DATA SCIENCE LAYER       │
                    │                               │
                    │ Python + NumPy                │
                    │ Jupyter Notebook              │
                    │ Data Analysis                 │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │       STREAMLIT LAYER         │
                    │                               │
                    │ Analytics & Visualization     │
                    └───────────────────────────────┘