# Backend Structure

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

## Configuration

- Use environment variables
- No secrets in code
- DEBUG = False in production

---

## Business Logic Rule

All critical logic must be inside:

- Service functions
- Model methods
- Signals (when appropriate)

Avoid placing business logic in views.
