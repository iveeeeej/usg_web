# System Architecture

---

## 1. Architecture Overview

Campus Connect follows a layered, API-first architecture designed for a single-organization governance system.

Client Layer:
- Web Officer Interface (HTML, CSS, JavaScript)
- Mobile Student Application (Flutter)

Application Layer:
- Django Backend
- Django REST Framework (API Layer)
- JWT Authentication (SimpleJWT)

Data Layer:
- PostgreSQL Database
- PostGIS (Geolocation validation)

This system is NOT multi-tenant.

---

## 2. Architectural Pattern

- Django MVT (backend internal structure)
- API-driven frontend architecture
- JWT-based authentication (stateless)
- Two-role authorization model (OFFICER / STUDENT)
- Modular Django app structure
- Service-layer business logic separation

The Web Officer Dashboard does NOT use Django template rendering.
It communicates exclusively through REST API calls secured by JWT.

---

## 3. Authorization Model

There are only two roles:

- OFFICER (Full system authority)
- STUDENT (Limited interaction access)

Authorization enforcement is handled via:

- JWT Authentication
- Custom DRF Permission Classes
- Server-side role validation

The `position` field is informational only.

All OFFICER accounts have equal module access.

---

## 4. High-Level Flow

Officer Web (HTML/CSS/JS)
        ↓
JavaScript fetch() with JWT
        ↓
Django REST API
        ↓
Service Layer
        ↓
ORM
        ↓
PostgreSQL Database

Mobile (Flutter)
        ↓
JWT-secured API calls
        ↓
Django REST API

---

## 5. Modular Design (Django Apps)

- accounts
- events
- attendance
- violations
- payments
- borrow
- announcements
- discussions
- reports
- analytics