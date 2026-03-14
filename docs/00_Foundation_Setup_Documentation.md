# 00 -- Foundation Setup Documentation

## Campus Connect (USG e-Governance System)

### Phase 1 -- Core Infrastructure Completion

------------------------------------------------------------------------

# 1. Purpose of This Document

This document provides a complete and detailed record of the steps
performed to establish the foundational architecture of the Campus
Connect system.

This includes:

- Django project structure
- PostgreSQL database integration
- Required PostgreSQL extensions (UUID, PostGIS)
- Custom User model
- Role-based access system (OFFICER / STUDENT)
- JWT authentication
- Admin panel setup
- Environment configuration (dev / prod)
- Base API structure
- Logging configuration

------------------------------------------------------------------------

# 2. Development Environment Setup

## 2.1 Tools Installed

- Python (Version used: 3.14.3)
- VS Code
- PostgreSQL (Version used: PostgreSQL 18)
- pgAdmin 4

## 2.2 Virtual Environment Setup

Create a virtual environment in the backend folder:

    python -m venv venv

Activate it:

Windows PowerShell:

    venv\Scripts\Activate.ps1

Windows CMD:

    venv\Scripts\activate.bat

------------------------------------------------------------------------

# 3. Backend Setup (Django Project)

## 3.1 Install Required Python Packages

Install Django + key dependencies:

    pip install django djangorestframework djangorestframework-simplejwt django-cors-headers

Additional infra dependencies (implemented):

    pip install python-dotenv
    pip install psycopg2-binary

------------------------------------------------------------------------

# 4. Create Django Project Structure

Inside backend directory:

    django-admin startproject config .

Verify server runs:

    python manage.py runserver

------------------------------------------------------------------------

# 5. Create Core Django Apps

Create the accounts app:

    python manage.py startapp accounts

Add it to INSTALLED_APPS.

------------------------------------------------------------------------

# 6. Configure Django REST Framework (DRF)

Add DRF to installed apps:

    "rest_framework",

JWT Auth via SimpleJWT:

    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        ),
    }

------------------------------------------------------------------------

# 7. CORS Setup

Install and configure django-cors-headers:

- Add "corsheaders" to INSTALLED_APPS
- Add "corsheaders.middleware.CorsMiddleware" to MIDDLEWARE (preferably near the top)

During development:

    CORS_ALLOW_ALL_ORIGINS = True

------------------------------------------------------------------------

# 7.2 Environment Configuration (Dev/Prod) + .env Loading (Implemented)

To prevent hardcoding secrets and database credentials, the settings
configuration was upgraded from a single `config/settings.py` file into a
settings package:

    backend/config/settings/
        base.py
        dev.py
        prod.py
        __init__.py

Runtime selection:

- `manage.py` defaults to `config.settings.dev`
- `wsgi.py` and `asgi.py` default to `config.settings.prod`

A `.env` file is stored in:

    backend/.env

and loaded at startup in `base.py` using `python-dotenv`.

Environment variables used:

- DJANGO_SECRET_KEY
- DJANGO_DEBUG
- DJANGO_ALLOWED_HOSTS
- DJANGO_TIME_ZONE
- CORS_ALLOW_ALL_ORIGINS
- DJANGO_LOG_LEVEL
- DB_ENGINE, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

Notes:

- `.env` is not automatically loaded by Django; it must be loaded using
  `load_dotenv(...)` in `base.py`.
- `.env` must be placed in `backend/.env` to match the configured path.

------------------------------------------------------------------------

## 7.2.1 Settings Package Migration Steps (Exact Implementation)

This subsection records the exact change that made `config.settings.dev` and
`config.settings.prod` work correctly.

### Why this change was required

- We needed `config.settings.dev` and `config.settings.prod` to exist.
- Python cannot treat `config/settings.py` as both a file module and a package.
  If `config/settings.py` exists, `config.settings.dev` will fail because
  `config.settings` points to the file, not a folder package.

### Step-by-step migration performed

1) Rename the original settings file:

    backend/config/settings.py  →  backend/config/old_settings.py

2) Create a settings package folder:

    backend/config/settings/
        __init__.py
        base.py
        dev.py
        prod.py

3) Update the settings module used by runtime entrypoints:

- In `backend/manage.py`:

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

- In `backend/config/wsgi.py`:

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")

- In `backend/config/asgi.py`:

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")

### Verification

Run:

    python manage.py check

Expected result:

    System check identified no issues (0 silenced).

------------------------------------------------------------------------

# 8. Custom User Model

A custom user model is implemented in `accounts/models.py`.

Key identity field:

- student_id (unique)

Role field:

- role (OFFICER / STUDENT)

Current profile and academic fields:

- first_name
- middle_name (nullable)
- last_name
- year_level (nullable)
- section (nullable)
- course (nullable)
- created_at
- updated_at

Reminder:

- Django `is_staff` / `is_superuser` are for Django Admin only.
- Application authority is based on `role`.
- `position` is informational metadata for OFFICER accounts and does not create a separate authorization layer.

AUTH_USER_MODEL is set in settings:

    AUTH_USER_MODEL = "accounts.User"

------------------------------------------------------------------------

# 9. Role System (OFFICER / STUDENT)

Role-based access is implemented:

- OFFICER users can access officer-only endpoints
- STUDENT users are blocked from officer-only endpoints

------------------------------------------------------------------------

# 10. JWT Authentication

JWT endpoints are provided:

- POST /api/token/
- POST /api/token/refresh/

Clients use:

Authorization: Bearer <access_token>

------------------------------------------------------------------------

# 11. Django Admin Panel Setup

Admin panel is enabled (default):

- /admin

A Django superuser can be created:

    python manage.py createsuperuser

Important:

- This superuser is stored in the current active database.
- When switching from SQLite → PostgreSQL, the old SQLite superuser does
  not automatically exist in PostgreSQL; a new one must be created (or
  user data migrated).

------------------------------------------------------------------------

# 12. Base API Structure

Example protected endpoint exists:

- GET /api/officer/dashboard/  (OFFICER-only)

------------------------------------------------------------------------

# 13. Officer Web Login Proof (HTML)

A minimal proof-of-flow was implemented:

- index.html: login using student_id/password, calls /api/token/
- usg_dashboard.html: uses stored access token to call protected endpoint

Result:

- Login works
- Dashboard redirect works
- Protected endpoint access works for OFFICER

------------------------------------------------------------------------

# 14. Logging Configuration (Implemented)

Basic logging was implemented using:

- Console logs (for local dev)
- Rotating file logs to:

    backend/logs/django.log

Folder requirement:

    backend/logs/

Log level is configurable via:

- DJANGO_LOG_LEVEL=INFO (in `.env`)

Verification:

1) Ensure folder exists:

    backend/logs/

2) Run server:

    python manage.py runserver

3) Perform a login and dashboard access.

Expected:
- A file is created/updated at `backend/logs/django.log`
- Logs include runserver reload notices and request/auth activity

------------------------------------------------------------------------

# 14.4 PostgreSQL Migration (Implemented)

Database backend was migrated from SQLite to PostgreSQL.

Key change:

- `DATABASES` is now environment-driven using `.env`:

  ENGINE/NAME/USER/PASSWORD/HOST/PORT

Critical detail (local setup):

- pgAdmin server connection used `localhost` and port `5433`.
- Django `.env` must match the same host/port to connect to the correct
  running PostgreSQL instance.

Verification steps:

- `python manage.py shell` → `from django.conf import settings; print(settings.DATABASES)`
- `python manage.py migrate` applies migrations to PostgreSQL
- Officer login + dashboard remains functional after migration

------------------------------------------------------------------------

## 14.4.1 Sample `.env` (Local Development)

This reflects the working local PostgreSQL connection configuration used
in development.

    DJANGO_SECRET_KEY=your-long-secret
    DJANGO_DEBUG=True
    DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
    DJANGO_TIME_ZONE=Asia/Manila

    CORS_ALLOW_ALL_ORIGINS=True
    DJANGO_LOG_LEVEL=INFO

    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=campus_connect
    DB_USER=postgres
    DB_PASSWORD=12345 (local dev only password)
    DB_HOST=localhost
    DB_PORT=5433

Critical local note:

- Your pgAdmin server registration is running PostgreSQL on port **5433**
  (not the default 5432).
- If Django uses DB_PORT=5432, it may connect to a different PostgreSQL instance,
  causing authentication failures even if the username/password is correct.

------------------------------------------------------------------------

# 15. Current Architecture State

Frontend (HTML prototype)
↓
JWT Auth (SimpleJWT)
↓
Django REST API
↓
Custom User + Role-based Access
↓
ORM
↓
PostgreSQL (current)

------------------------------------------------------------------------

# 15.1 Phase 1 Infrastructure Additions (Completed)

✔ PostgreSQL configured and connected (env-driven DATABASES)
✔ Settings split into base/dev/prod
✔ `.env` loading via python-dotenv
✔ Rotating file logging (backend/logs/django.log)

------------------------------------------------------------------------

# 16. Phase 1 Completed Items

- Setup Django project structure
- Implement custom User model
- Implement role system
- Implement JWT authentication
- Configure Django admin panel
- Establish base API structure
- Implement basic logging configuration (implemented as part of infra add-ons)
- Configure PostgreSQL database (implemented as part of infra add-ons)

------------------------------------------------------------------------

# 17. Next Development Step

Proceed to Phase 2 (Governance and Communication Core) after
foundation + infra are stable:

- Dashboard module
- Events module (including General Assembly via event_type)
- Calendar / event scheduling view
- Announcements module
- Discussion Forum foundation
- Notification / system alert foundation
- Corresponding REST API endpoints
- Officer web interface connections

------------------------------------------------------------------------

# 18. Phase 2 Preparation (Pre-Implementation Cleanup)

Date: 2026-03-12

Before beginning Phase 2 implementation, the following preparation
steps were completed to bring the codebase into alignment with the
revised documentation set.

## 18.1 Removed `is_verified` and `verified_at` from User Model

Reason:
The revised `04_database_design_principles.md` (Section 3.2) specifies
that `is_verified` and `verified_at` are NOT part of the current core
User schema. These fields belonged to the older biometric attendance
direction which has been moved to Phase 9 (Future Enhancements).

Changes:
- `backend/accounts/models.py`: removed `is_verified` and `verified_at`
  fields from the User model
- `backend/accounts/admin.py`: removed the Verification fieldset from
  CustomUserAdmin that referenced those fields
- Migration generated and applied:
  `accounts/migrations/0002_remove_user_is_verified_remove_user_verified_at.py`

Verification:
- `python manage.py makemigrations` detected field removal correctly
- `python manage.py migrate` applied successfully
- `python manage.py check` returned: System check identified no issues

Mistakes: None encountered during this step.

## 18.2 Fixed Stale Documentation References

- Section 16 heading: changed "Phase 0" → "Phase 1" (user applied)
- Section 17: updated Phase 2 scope from old attendance-focused list
  to the new Governance and Communication Core module list
- Section 1: removed `pgvector` from listed PostgreSQL extensions,
  since pgvector related to the biometric embedding direction which
  is no longer in the current core scope

## 18.3 Added Current User Profile Fields to Match Revised Schema

Date: 2026-03-13

Reason:
The revised `04_database_design_principles.md` (Section 3.1) defines a
larger current-scope `User` schema than the original Phase 1 backend
implementation. The live backend therefore needed to add the missing
profile and academic fields so the code, database, and docs all match.

Changes:
- `backend/accounts/models.py`: added `first_name`, `middle_name`,
  `last_name`, `year_level`, `section`, `course`, and `updated_at`
- `backend/accounts/admin.py`: expanded `CustomUserAdmin` fieldsets,
  list display, filters, and search fields to support the new User fields
- `backend/accounts/migrations/0003_add_user_profile_fields.py`:
  created and applied to sync the PostgreSQL schema
- `backend/accounts/tests.py`: added model tests covering the new fields
  and full-name behavior

Verification:
- `python manage.py makemigrations --check --dry-run` returned
  `No changes detected`
- `python manage.py test accounts` passed successfully
- `python manage.py migrate` applied the new User field migration

Mistakes: None encountered during this step.

## 18.4 Started Phase 2 Governance and Communication Backend Modules

Date: 2026-03-13

Reason:
With the Phase 1 identity and infrastructure work stable, the backend
began the first active Phase 2 implementation slice from the revised
roadmap. The goal of this step was to start the governance and
communication layer without jumping ahead to later phases.

Changes:
- `backend/events/`: implemented the `Event` and `EventAttachment`
  models, admin registration, serializers, permissions, views, URLs,
  tests, and initial migration
- `backend/announcements/`: implemented the `Announcement` model, admin
  registration, serializers, permissions, views, URLs, tests, and
  initial migration
- `backend/config/settings/base.py`: registered the new Phase 2 apps in
  `INSTALLED_APPS`
- `backend/config/urls.py`: mounted the new `/api/events/` and
  `/api/announcements/` routes
- `docs/09_development_phases.md`: updated Phase 2 progress and task
  markers to reflect the completed backend slices
- `docs/05_backend_structure.md`: updated the actual backend tree to
  include the new `events` and `announcements` apps

Verification:
- `python manage.py makemigrations events`
- `python manage.py makemigrations announcements`
- `python manage.py migrate`
- `python manage.py test announcements accounts events`
- `python manage.py makemigrations --check --dry-run` returned
  `No changes detected`
- `python manage.py check` returned: System check identified no issues

Mistakes:
- The initial implementation pace was too fast relative to the workflow
  rules in `10_agent_development_rules.md`
- The correction was to pause, restate the active phase, propose only
  one small Phase 2 slice, wait for user confirmation, and then continue
  incrementally
