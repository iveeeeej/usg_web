# 00 – Foundation Setup Documentation
## Campus Connect (USG e-Governance System)
### Phase 0 – Core Infrastructure Completion

---

# 1. Purpose of This Document

This document provides a complete and detailed record of the steps performed to establish the foundational architecture of the Campus Connect system.

This includes:

- Python environment setup
- Virtual environment configuration
- Django project initialization
- Dependency installation
- Custom User model implementation
- JWT authentication setup
- Role-based authorization (OFFICER / STUDENT)
- Officer-only protected endpoint
- CORS configuration
- Frontend integration via JavaScript fetch()
- Secure login/logout flow
- Structural endpoint renaming
- Validation improvements

This document serves as:

- Rebuild guide
- Architecture reference
- Capstone technical documentation
- Development baseline

---

# 2. Development Environment Setup

## 2.1 Python Installation

Verified Python installation: # 00 – Foundation Setup Documentation
## Campus Connect (USG e-Governance System)
### Phase 0 – Core Infrastructure Completion

---

# 1. Purpose of This Document

This document provides a complete and detailed record of the steps performed to establish the foundational architecture of the Campus Connect system.

This includes:

- Python environment setup
- Virtual environment configuration
- Django project initialization
- Dependency installation
- Custom User model implementation
- JWT authentication setup
- Role-based authorization (OFFICER / STUDENT)
- Officer-only protected endpoint
- CORS configuration
- Frontend integration via JavaScript fetch()
- Secure login/logout flow
- Structural endpoint renaming
- Validation improvements

This document serves as:

- Rebuild guide
- Architecture reference
- Capstone technical documentation
- Development baseline

---

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

---

# 3. Virtual Environment Setup

## 3.1 Create Virtual Environment

Inside `backend/`:

- python -m venv venv

This created:

backend/venv/

## 3.2 Activate Virtual Environment (Windows)

From `backend/` directory:

venv\Scripts\activate

Terminal shows:

(venv)

This confirms activation.

Virtual environment must be activated before running Django.

---

# 4. Django Installation and Initialization

## 4.1 Install Django

Inside activated venv:

- pip install django

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

- python manage.py migrate

Applied default Django migrations:

- admin
- auth
- contenttypes
- sessions

## 4.4 Run Development Server

- python manage.py runserver

Server runs at: http://127.0.0.1:8000/

---

# 5. Installed Dependencies

Installed:

- pip install djangorestframework
- pip install djangorestframework-simplejwt
- pip install django-cors-headers

Final dependency stack includes:

- Django
- Django REST Framework
- SimpleJWT
- django-cors-headers

---

# 6. Django REST Framework Configuration

In `config/settings.py`:

Added to `INSTALLED_APPS`:

```python
'rest_framework',
'corsheaders',
'accounts',

Configured REST Framework:

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# 7. CORS Configuration

Problem encountered, browser blocked requests due to:

Access-Control-Allow-Origin error

Cause,

Frontend served via:

http://127.0.0.1:5500

Backend served via:

Backend served via:

Different origins require CORS permission.

## 7.1 CORS Fix Implementation

Added to INSTALLED_APPS:
'corsheaders',

Added to top of MIDDLEWARE:
'corsheaders.middleware.CorsMiddleware',

Added to bottom of settings.py:
CORS_ALLOW_ALL_ORIGINS = True

Restarted server.

CORS issue resolved.