# Backend Structure

---

## Project Layout

Root Path:
    c:\Users\Acer\Projects\web\usg_web

Actual repo structure (generated 3/5/2026):

backend/
    accounts/
        migrations/
            0001_initial.py
            __init__.py
        admin.py
        apps.py
        models.py
        permissions.py
        views.py
    config/
        settings/
            __init__.py
            base.py
            dev.py
            prod.py
        __init__.py
        asgi.py
        old_settings.py
        urls.py
        wsgi.py
    logs/
    db.sqlite3
    manage.py

docs/
    00_Foundation_Setup_Documentation.md
    01_project_overview.md
    02_system_architecture.md
    03_technology_stack.md
    04_database_design_principles.md
    05_backend_structure.md
    06_api_design_guidelines.md
    07_security_and_permissions.md
    08_mobile_integration.md
    09_development_phases.md
    file_structure.md

frontend/
    (static HTML/CSS/JS officer UI)

---

## Authentication Model

- Custom User model
- USERNAME_FIELD = student_id
- JWT authentication via djangorestframework-simplejwt
- Stateless token-based authentication
- No session-based authentication for Web Officer dashboard

All protected endpoints require:

Authorization: Bearer <access_token>

---

## Authorization Model

Two roles only:
- OFFICER (full access)
- STUDENT (restricted)

Role validation is enforced via:

- DRF Permission Classes (e.g., IsOfficer)
- request.user.role checks
- Server-side validation

Position field does not restrict access.
It is informational only.

---

## Business Logic Placement

All critical logic must be inside:

- Service functions
- Model methods
- Permission validators

Never inside:
- Templates
- Frontend JavaScript

---

## Validation Philosophy

- All important validation is server-side.
- Frontend is never trusted.

---

## Biometric Processing Module

A dedicated backend module handles biometric verification.

Responsibilities:

- Face registration during account verification
- Liveness challenge validation
- Face embedding generation (backend inference only)
- Embedding comparison
- Similarity threshold evaluation

Important:

- Mobile captures image only.
- Embedding generation occurs on backend.
- Decision is made server-side.
- Embeddings are never exposed in API responses.