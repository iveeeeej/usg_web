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

## Authorization Model

Two roles only:
- ADMIN (full access)
- STUDENT (restricted)

Role validation must be performed in:

- View decorators
- API permission classes
- Service-layer functions

Position field does not restrict access.
It is informational.

---

## Business Logic Placement

All critical logic must be inside:

- Service functions
- Model methods
- Permission validators

Never:
- Inside templates
- Inside frontend JavaScript

---

## Validation Philosophy

- All important validation is server-side.
- Never trust frontend data.

---

## Biometric Processing Module

A dedicated backend module handles biometric verification.

Responsibilities:

- Face registration during account verification
- Liveness challenge validation
- Face embedding generation (backend inference)
- Embedding comparison
- Similarity threshold evaluation

Important:

- Mobile device captures image only.
- Embedding generation occurs on the backend.
- Final verification decision is made server-side.
- Embedding data is never exposed through API responses.