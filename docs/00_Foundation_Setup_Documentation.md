# 00 -- Foundation Setup Documentation

## Campus Connect (USG e-Governance System)

### Phase 0 -- Core Infrastructure Completion

------------------------------------------------------------------------

# 1. Purpose of This Document

This document provides a complete and detailed record of the steps
performed to establish the foundational architecture of the Campus
Connect system.

This includes:

-   Python environment setup
-   Virtual environment configuration
-   Django project initialization
-   Dependency installation
-   Custom User model implementation
-   JWT authentication setup
-   Role-based authorization (OFFICER / STUDENT)
-   Officer-only protected endpoint
-   CORS configuration
-   Frontend integration via JavaScript fetch()
-   Secure login/logout flow
-   Structural endpoint renaming
-   Validation improvements

This document serves as:

-   Rebuild guide
-   Architecture reference
-   Capstone technical documentation
-   Development baseline

------------------------------------------------------------------------

# 2. Development Environment Setup

## 2.1 Python Installation

Verified Python installation:

    python --version

Confirmed version:

    Python 3.14.3

## 2.2 Project Folder Structure (Initial State)

Project root:

    usg_web/
        backend/
        frontend/

Backend contains Django project.
Frontend contains HTML/CSS/JS.

------------------------------------------------------------------------

# 3. Virtual Environment Setup

## 3.1 Create Virtual Environment

Inside `backend/`:

    python -m venv venv

This created:

    backend/venv/

## 3.2 Activate Virtual Environment (Windows)

From `backend/` directory:

    venv\Scripts\activate

Terminal shows:

    (venv)

This confirms activation.

Virtual environment must be activated before running Django.

------------------------------------------------------------------------

# 4. Django Installation and Initialization

## 4.1 Install Django

Inside activated venv:

    pip install django

## 4.2 Create Django Project

Inside `backend/`:

    django-admin startproject config .

This created:

    backend/
        manage.py
        config/
            settings.py
            urls.py

## 4.3 Apply Initial Migrations

    python manage.py migrate

Applied default Django migrations:

-   admin
-   auth
-   contenttypes
-   sessions

## 4.4 Run Development Server

    python manage.py runserver

Server runs at:

    http://127.0.0.1:8000/

------------------------------------------------------------------------

# 5. Installed Dependencies

Installed:

    pip install djangorestframework
    pip install djangorestframework-simplejwt
    pip install django-cors-headers

Final dependency stack includes:

-   Django
-   Django REST Framework
-   SimpleJWT
-   django-cors-headers

------------------------------------------------------------------------

# 6. Django REST Framework Configuration

In `config/settings.py`:

Added to `INSTALLED_APPS`:

``` python
'rest_framework',
'corsheaders',
'accounts',
```

Configured REST Framework:

``` python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

------------------------------------------------------------------------

# 7. CORS Configuration

Problem encountered: browser blocked requests due to:

    Access-Control-Allow-Origin error

Cause:

Frontend served via:

    http://127.0.0.1:5500

Backend served via:

    http://127.0.0.1:8000

Different origins require CORS permission.

## 7.1 CORS Fix Implementation

Added to `INSTALLED_APPS`:

``` python
'corsheaders',
```

Added to top of `MIDDLEWARE`:

``` python
'corsheaders.middleware.CorsMiddleware',
```

Added to bottom of `settings.py`:

``` python
CORS_ALLOW_ALL_ORIGINS = True
```

Restarted server.

CORS issue resolved.

------------------------------------------------------------------------

# 8. Custom User Model Implementation

Created app:

    python manage.py startapp accounts

In `settings.py`:

``` python
AUTH_USER_MODEL = 'accounts.User'
```

This replaced Django's default User model.

## 8.1 Identity Model Design

Primary login field:

    student_id

Configured:

    USERNAME_FIELD = 'student_id'

Email is used for:

-   Password recovery
-   Account verification
-   Mobile verification confirmation

Password:

-   Initially same as student_id
-   Can be changed by user

------------------------------------------------------------------------

# 9. Role Model Design

Only two roles exist:

-   OFFICER
-   STUDENT

No Super Admin role exists at application level.

Position field examples:

-   PRESIDENT
-   VICE_PRESIDENT
-   TREASURER
-   AUDITOR
-   SECRETARY
-   etc.

Position is informational only.

All OFFICER accounts have full module access.

Authorization depends strictly on:

    request.user.role

------------------------------------------------------------------------

# 10. JWT Authentication Setup

## 10.1 Login Endpoint

    POST /api/token/

Body:

``` json
{
  "student_id": "value",
  "password": "value"
}
```

Response:

``` json
{
  "refresh": "...",
  "access": "..."
}
```

## 10.2 Token Usage

Protected endpoint requires:

    Authorization: Bearer <access_token>

Authentication class:

    JWTAuthentication

Stateless authentication model implemented.

------------------------------------------------------------------------

# 11. Role-Based Permission Enforcement

Created custom permission class:

``` python
class IsOfficer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "OFFICER"
```

Applied to protected view:

    /api/officer/dashboard/

## 11.1 Response Behavior

-   401 → No token provided
-   403 → Token valid but role != OFFICER
-   200 → Authorized OFFICER

------------------------------------------------------------------------

# 12. Endpoint Structural Adjustment

Initially endpoint was:

    /api/admin/dashboard/

Renamed to:

    /api/officer/dashboard/

Reason:

Consistency with role model (OFFICER).

Updated:

-   Backend urls.py
-   Frontend fetch call
-   Documentation

------------------------------------------------------------------------

# 13. Superuser Creation

Created using:

    python manage.py createsuperuser

Important:

Django superuser is for admin panel only.

Application authority depends strictly on:

    role = OFFICER

Superuser does not override application-level permission logic.

------------------------------------------------------------------------

# 14. Frontend Officer Login Implementation

Frontend served via:

    http://127.0.0.1:5500

## 14.1 Login Flow (index.html)

1.  Officer enters student_id and password
2.  JavaScript sends POST to /api/token/
3.  On success:
    -   Store access_token
    -   Store refresh_token
    -   Redirect to dashboard

Validation added:

``` javascript
if (!student_id || !password) {
    alert("Please enter ID and password.");
    return;
}
```

## 14.2 Protected Dashboard (usg_dashboard.html)

On page load:

1.  Retrieve access_token from localStorage

2.  If missing → redirect to login

3.  Call:

    GET /api/officer/dashboard/

If:

-   401 → remove token, redirect
-   403 → remove token, redirect
-   200 → allow dashboard access

## 14.3 Logout Implementation

Logout clears:

``` javascript
localStorage.removeItem("access_token");
localStorage.removeItem("refresh_token");
```

Then redirects to login page.

------------------------------------------------------------------------

# 15. Current Architecture State

Officer Web (HTML + JS)
↓
JWT via fetch()
↓
Django REST API
↓
Permission Class
↓
Service Layer (future modules)
↓
ORM
↓
PostgreSQL

Mobile (Future)
↓
JWT-secured API
↓
Same backend

------------------------------------------------------------------------

# 16. Phase 0 Completed Items

✔ Virtual environment configured
✔ Django initialized
✔ REST Framework installed
✔ SimpleJWT integrated
✔ CORS configured
✔ Custom User model implemented
✔ student_id login field
✔ OFFICER / STUDENT role model
✔ Custom permission class
✔ Officer-only protected endpoint
✔ Separate officer login page
✔ Protected dashboard
✔ Proper logout flow
✔ Endpoint naming aligned

------------------------------------------------------------------------

# 17. What Is Not Yet Implemented

-   Events module
-   Attendance system
-   Violation system
-   Payment module
-   Reports module
-   Biometric face recognition module
-   Mobile Flutter integration

These begin in Phase 1.

------------------------------------------------------------------------

# 18. Architectural Decisions Locked

-   API-first architecture
-   Stateless JWT authentication
-   Server-side role enforcement
-   Frontend not trusted for access control
-   No application-level super admin
-   Single-organization governance model

------------------------------------------------------------------------

End of Phase 0 Documentation

This is now your official technical baseline.

From this point forward:

Whenever we modify architecture
→ We update documentation immediately.

You are building this like a real engineering system.

When you're ready, we move into Phase 1 -- Events Module.
