# Backend Structure

---

## 1. Purpose of the Backend

The Campus Connect backend is the central business and data-processing layer of the system.

It is responsible for:

- authentication and token issuance
- authorization and role enforcement
- business workflow validation
- attendance processing
- student service request handling
- record management
- reporting and analytics support
- API communication between the officer web interface and the student mobile application

The backend is designed as the single source of truth for the system.

It must enforce the finalized Campus Connect model:

- one USG organization only
- two application roles only: `OFFICER` and `STUDENT`
- API-first architecture
- JWT-secured communication
- attendance based on authenticated student identity, active session QR, and geolocation
- payment tracking first, with payment gateway integration only as a later enhancement
- biometrics excluded from the current core backend scope

---

## 2. Current Repository Context

Root Path:
    c:\Users\Acer\Projects\web\usg_web

Campus Connect is currently organized into three main project areas:

- `backend/`
- `docs/`
- `frontend/`

The backend is the actual Django project and API layer.

The `docs/` directory contains the project documentation set.

The `frontend/` directory currently contains the web officer interface assets and pages.

---

## 3. Current Actual Backend Layout

Based on the current file tree, the backend currently contains:

backend/
    accounts/
        migrations/
            0001_initial.py
            __init__.py
        __init__.py
        admin.py
        apps.py
        models.py
        permissions.py
        tests.py
        views.py
    config/
        settings/
            __init__.py
            base.py
            dev.py
            prod.py
        __init__.py
        asgi.py
        urls.py
        wsgi.py
    logs/
    manage.py

This is the current actual implemented backend structure.

Important clarification:
- `old_settings.py` is not part of the current active backend tree
- `db.sqlite3` is not part of the current active backend tree shown in the latest file structure
- environment-based settings are now organized under `config/settings/`

This means the backend has already moved to a cleaner configuration structure than the older version of this document described.

---

## 4. Backend Architectural Role

Campus Connect follows a layered, API-first backend structure.

High-level backend flow:

Officer Web Interface / Mobile Student App
        ↓
JWT-authenticated API request
        ↓
Django REST API
        ↓
Service / Validation / Permission Logic
        ↓
Django ORM
        ↓
PostgreSQL / PostGIS

The backend does not exist only to serve raw data.
It is the enforcement boundary for:

- identity
- permissions
- workflow rules
- attendance validation
- record ownership
- payment safeguards
- structured reporting rules

The officer web interface does not rely on Django template rendering as its primary behavior.
Instead, it communicates with the backend through API requests secured by JWT.

---

## 5. Core Implemented Backend Components

### 5.1 `backend/accounts/`

This is the currently implemented application module in the backend.

Its current role is to hold the identity and access-control foundation of the system.

It currently includes:
- `models.py`
- `views.py`
- `permissions.py`
- `admin.py`
- `tests.py`
- migrations

This app is the appropriate place for:
- custom User model logic
- role-based access helpers
- authentication-related backend behavior tied to the user domain
- account administration support

### 5.2 `backend/config/`

This is the Django project configuration layer.

It contains:
- `settings/`
- `urls.py`
- `asgi.py`
- `wsgi.py`

The `settings/` package contains:
- `base.py`
- `dev.py`
- `prod.py`

This structure supports environment-based configuration and is the correct replacement for a single monolithic settings file.

### 5.3 `backend/logs/`

This directory is reserved for backend logs and operational logging output.

It supports the logging strategy already defined elsewhere in the documentation and helps separate runtime logs from source code files.

### 5.4 `backend/manage.py`

This remains the standard Django project entry point for:
- running the development server
- migrations
- administrative commands
- test execution
- maintenance utilities

---

## 6. Designed Modular Growth Path

Although the current implemented backend tree is still small, the backend is designed to grow into a modular Django app structure.

The intended backend module set should align with the system architecture and project scope.

Recommended backend app expansion path:

- `accounts`
- `events`
- `announcements`
- `discussions`
- `notifications`
- `attendance`
- `violations`
- `borrow`
- `payments`
- `reports`
- `resolutions`
- `lost_found`
- `campus`
- `analytics`

Important distinction:

- **Current actual structure** = what already exists in the repository now
- **Designed modular growth path** = the intended backend organization as more modules are implemented

This distinction is important so the documentation does not falsely imply that all planned apps already exist physically in the repository today.

---

## 7. Recommended Responsibility Per Backend Module

As the backend expands, each Django app should have a clear responsibility boundary.

### 7.1 `accounts`
Responsible for:
- custom User model
- role and position fields
- identity-related permissions
- account administration helpers

### 7.2 `events`
Responsible for:
- event records
- general assembly scheduling behavior
- event attachments
- officer-created schedule management

### 7.3 `announcements`
Responsible for:
- official announcement records
- publish/archive rules
- student-facing announcement visibility

### 7.4 `discussions`
Responsible for:
- discussion threads
- comments and replies
- moderation-related rules
- discussion attachments if implemented

### 7.5 `notifications`
Responsible for:
- system-generated notifications
- user notification delivery state
- read/unread tracking

### 7.6 `attendance`
Responsible for:
- attendance sessions
- attendance records
- QR-session validation
- geolocation validation
- cutoff and duplicate-prevention logic

### 7.7 `violations`
Responsible for:
- violation records
- accountability tracking
- service-hour obligations

### 7.8 `borrow`
Responsible for:
- borrowable inventory
- borrow requests
- request approval/rejection workflow
- return tracking

### 7.9 `payments`
Responsible for:
- tracked payment records
- contribution records
- violation-related payments
- confirmation workflows

### 7.10 `reports`
Responsible for:
- structured reports
- report templates
- report attachments
- locking, revision, and version-tracking logic if implemented

### 7.11 `resolutions`
Responsible for:
- resolution records
- legislative document tracking
- filing and status metadata

### 7.12 `lost_found`
Responsible for:
- lost and found item records
- item images
- claim status tracking

### 7.13 `campus`
Responsible for:
- campus locations
- campus tour data
- location metadata

### 7.14 `analytics`
Responsible for:
- officer dashboard summaries
- aggregated reporting views
- decision-support metrics
- historical comparison support

---

## 8. Authentication Model

The backend uses a custom authentication model centered on JWT.

Key rules:

- custom User model is used
- `student_id` is the login identifier
- JWT is used through `djangorestframework-simplejwt`
- protected requests use `Authorization: Bearer <access_token>`
- backend authentication is stateless at the API layer
- the backend, not the client, is the source of truth for identity

All protected endpoints must derive the acting user from the authenticated request context.

The backend must not treat client-submitted identifiers as higher authority than authenticated identity.

---

## 9. Authorization Model

Campus Connect uses only two application roles:

- `OFFICER`
- `STUDENT`

Authorization is enforced through:
- JWT authentication
- DRF permission classes
- request-user role checks
- server-side ownership validation
- workflow-specific permission rules

Important rule:
the `position` field is informational only.

This means:
- it may describe the officer’s organizational designation
- it does not create a second hidden authorization layer
- all OFFICER accounts share the same current application-level authority

Django `is_superuser` may still exist for framework administration, but it is not part of the business-level permission model.

---

## 10. Business Logic Placement

Critical business logic must stay inside the backend.

It should be placed in:
- service-layer functions
- model methods where appropriate
- serializer validation where appropriate
- permission validators
- dedicated domain logic helpers

It must not be placed primarily in:
- frontend JavaScript
- HTML pages
- client-side role checks alone
- mobile-only decision logic

The frontend may improve usability, but the backend must remain the final enforcement layer for all important business rules.

---

## 11. Validation Philosophy

All important validation must be server-side.

The backend must validate:
- required fields
- field formats
- enum/status values
- ownership rules
- permission rules
- attendance session state
- QR/session validity
- geolocation rules
- duplicate attendance prevention
- borrow workflow transitions
- payment state changes
- report locking and structure rules

This follows one core principle:

**the frontend is never the final authority for business validation.**

---

## 12. Attendance Logic Placement

Attendance is one of the most sensitive backend workflows.

Its core processing should live in backend attendance services and validators.

The backend must enforce:
- authenticated student identity
- active attendance session validation
- session QR validation
- geolocation validation
- cutoff and timing rules
- duplicate-prevention rules
- attendance-record creation only after all checks pass

The backend should treat attendance identity as coming from:
- authenticated JWT user
- active session
- validated request data

It should not treat school-ID QR as the final core design.

It should also not require biometrics in the current core backend flow.

---

## 13. API-First Backend Rule

The backend is built for an API-driven system.

This means:
- the officer web interface consumes REST endpoints
- the student mobile app consumes REST endpoints
- business workflows must be exposed through protected, validated API endpoints
- the backend should be designed around reusable domain modules rather than page-bound logic

The backend should therefore be organized for:
- maintainable API growth
- reusable service logic
- separation of module concerns
- independent client consumption by web and mobile

---

## 14. Logging and Operational Concerns

The backend should preserve operational visibility through logs and traceable actions.

Logging should support:
- debugging
- error tracking
- audit-friendly visibility for important workflows
- backend maintenance

Examples of important backend events to log include:
- authentication issues
- attendance session changes
- attendance submission outcomes
- payment confirmation actions
- borrow approval actions
- report submission or locking
- system-level failures

The `backend/logs/` directory supports this operational need.

---

## 15. Explicit Exclusions from Current Core Backend Scope

The following are **not part of the current core backend baseline**:

- mandatory biometric verification during attendance
- dedicated biometric processing as a required live module
- liveness challenge as a required current flow
- face embedding comparison as a required current flow
- `is_verified` / `verified_at` as current attendance prerequisites
- multi-tenant organization backend design

These may be introduced only if the project officially enters a future enhancement phase.

---

## 16. Future Enhancement Direction

If Campus Connect later adopts advanced features, the backend may expand with additional modules or services for:

- biometric attendance reinforcement
- payment gateway callbacks and reconciliation
- deeper analytics processing
- richer notification delivery mechanisms
- advanced audit and correction workflows

These should be treated as future extensions of the backend, not as current core requirements.

---

## 17. Summary

The Campus Connect backend is the central enforcement and processing layer of the system.

Its current actual repository structure is still in an early modular state, with `accounts`, `config`, `logs`, and `manage.py` already present.

Its intended growth direction is a clean modular Django backend aligned with the finalized project scope:
- governance and communication
- attendance and accountability
- student services
- official records and structured reporting
- summaries and analytics

The backend must remain API-first, role-secured, validation-driven, and fully aligned with the current official scope of Campus Connect.