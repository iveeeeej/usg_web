# Technology Stack

---

## 1. Technology Stack Overview

Campus Connect uses a web + mobile + API architecture supported by a centralized
backend and relational database.

The stack is designed to support:

- one USG organization only
- API-first communication
- JWT-secured web and mobile access
- role-based backend enforcement
- attendance workflows with geolocation validation
- structured reporting and service workflows
- future extensibility without requiring unnecessary third-party platform dependencies

The technology stack is divided into the following layers:

- Backend
- Web Frontend
- Mobile Application
- Database
- Development and Environment Support

---

## 2. Backend Stack

### 2.1 Core Backend Framework

**Framework:** Django  
**API Layer:** Django REST Framework  
**Language:** Python

The backend is responsible for:

- authentication
- authorization
- business logic
- workflow validation
- attendance processing
- file handling
- reporting support
- analytics-related processing
- centralized API delivery for both web and mobile clients

Django is used as the core backend framework because it provides:

- strong project structure
- ORM support
- admin integration
- secure authentication foundations
- modular app organization
- compatibility with Django REST Framework

### 2.2 API Framework

**API Framework:** Django REST Framework (DRF)

DRF is used to expose protected REST endpoints for:

- officer web interface requests
- student mobile application requests
- record retrieval
- workflow submissions
- role-based protected actions

This supports the project’s API-first architecture.

### 2.3 Authentication

**Authentication Approach:** Django Authentication + JWT  
**JWT Package:** `djangorestframework-simplejwt`

Authentication is implemented using:

- a custom User model
- `student_id` as the `USERNAME_FIELD`
- JWT access tokens
- JWT refresh tokens
- Bearer-token authorization for protected endpoints

JWT is used so both the web and mobile clients can authenticate consistently through the same backend.

### 2.4 Environment Configuration

**Environment Configuration:** `python-dotenv`

Environment-based configuration is used to avoid hardcoding:

- secret keys
- debug settings
- allowed hosts
- database credentials
- log level settings
- environment-specific runtime behavior

The backend uses a split settings structure:

- `base.py`
- `dev.py`
- `prod.py`

This supports cleaner local development and production deployment setup.

### 2.5 Database Driver

**PostgreSQL Driver:** `psycopg2-binary`

This package enables Django to communicate with PostgreSQL in the current backend setup.

---

## 3. Web Frontend Stack

### 3.1 Core Web Technologies

**Languages:**
- HTML5
- CSS3
- JavaScript

The current web frontend is primarily used for the OFFICER-side interface.

### 3.2 UI Framework

**Framework:** Bootstrap

Bootstrap is used to support:

- faster UI development
- responsive layouts
- consistent component styling
- easier officer dashboard and admin-style page construction

### 3.3 Rendering Style

The officer web frontend currently follows a **partially API-driven rendering approach**.

In the current repository:
- login and token-based access control are live
- officer dashboard summaries and recent announcement rendering are live
- the officer "What's New" card is backed by a shared backend-stored message and editable through the API
- backend APIs for events and announcements are implemented
- several officer-facing pages remain partially integrated and still function as UI-first scaffolds

This means:
- the frontend does not act primarily as a Django server-rendered dashboard
- backend APIs remain the source of truth for business rules
- full page-level API integration is still in progress

This aligns with the system's API-first architecture while accurately reflecting the current implementation stage.


---

## 4. Mobile Application Stack

### 4.1 Mobile Framework

**Framework:** Flutter  
**Language:** Dart

Flutter is the intended framework for the student-facing mobile application of Campus Connect.

The Flutter mobile client may be maintained in a separate repository from the backend and officer web frontend. This document therefore describes the system-wide mobile stack and integration direction, not only the contents of the current repository.

The mobile is responsible for:

- viewing events and announcements
- attending active attendance sessions
- viewing violations and payment records
- submitting requests and feedback
- viewing profile summaries
- accessing student-facing service features

### 4.2 Mobile-to-Backend Communication

**Communication Style:** REST API using JSON  
**Authentication:** JWT Bearer Token

The mobile app communicates with the same centralized backend used by the officer web interface.

In the current project setup, the backend in this repository is the shared API and data layer for both:
- the officer web frontend contained in this repository
- the student mobile application maintained in a separate project when applicable

This supports:
- consistent authentication
- shared backend rules
- single-source-of-truth data handling
- reusable workflow enforcement across platforms

---

## 5. Database Stack

### 5.1 Primary Database

**DBMS:** PostgreSQL

PostgreSQL is the primary database system used by Campus Connect.

It is chosen because it supports:

- strong relational integrity
- reliable transactional behavior
- indexing flexibility
- structured schema management
- JSON-compatible fields where needed
- production-grade reliability

### 5.2 Geospatial Support

**Extension / GIS Support:** PostGIS

PostGIS is part of the planned geospatial database stack for Phase 3 attendance and geolocation workflows.

In the current repository, PostgreSQL is the active backend database baseline. Application-level attendance geolocation models and PostGIS-backed validation are not yet implemented.

When Phase 3 attendance work begins, PostGIS is intended to support:
- point-based coordinate storage
- center-radius validation
- polygon-based geospatial checks if needed later


---

## 6. Development and Infrastructure Support

### 6.1 Version Control and Development Tools

The documented development environment includes tools such as:

- Python
- PostgreSQL
- pgAdmin
- VS Code

These support local backend development, database inspection, and project maintenance.

### 6.2 Logging Support

The backend uses logging support for:

- development diagnostics
- request and authentication visibility
- application troubleshooting
- operational monitoring

Current logging includes:

- console logging
- rotating file logging

### 6.3 Local Environment Versions

The project foundation documentation records the local development versions used during setup, including:

- Python 3.14.3
- PostgreSQL 18

These are useful implementation references, but the technology stack itself should be understood mainly in terms of framework and platform choices rather than local machine version numbers alone.

---

## 7. Stack Summary by Layer

### Backend
- Django
- Django REST Framework
- Python
- SimpleJWT
- python-dotenv
- psycopg2-binary

### Web Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

### Mobile
- Flutter (student mobile client, may be maintained in a separate repository)
- Dart
- REST API (JSON)
- JWT-based authentication

### Database
- PostgreSQL
- PostGIS (planned Phase 3 geolocation support)

---

## 8. Explicit Non-Dependencies

The current Campus Connect stack does **not** use:

- Supabase
- biometric-processing infrastructure as part of the current core stack
- direct third-party payment gateway infrastructure as part of the current required baseline
- multi-tenant platform services

These are excluded from the present core stack definition.

---

## 9. Why This Stack Fits Campus Connect

This stack fits Campus Connect because it supports:

- centralized backend control
- role-based secured access
- web and mobile client integration
- structured relational data handling
- geolocation-aware attendance
- modular growth as additional features are implemented

It also matches the current project direction of building a single-USG,
API-first e-governance and student services platform without unnecessary
dependency on external backend-as-a-service platforms.

---

## 10. Summary

Campus Connect uses a practical and scalable stack built around:

- Django + Django REST Framework for backend and APIs
- JWT for authentication
- PostgreSQL for the current backend data layer, with PostGIS planned for Phase 3 attendance geolocation
- Bootstrap-based web frontend development
- Flutter for the student mobile application, which may be maintained in a separate repository
- environment-based configuration through `python-dotenv`

This stack is aligned with the project’s current scope, architecture,
security model, and attendance workflow requirements.
