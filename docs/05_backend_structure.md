# Backend Structure

---

## Project Layout

project_root/
    manage.py
    config/
    apps/
        accounts/
        events/
        attendance/
        violations/
        payments/
        borrow/
        announcements/
        discussions/
        reports/
        analytics/

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