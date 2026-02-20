# System Architecture

---

## 1. Architecture Overview

Campus Connect follows a layered architecture designed for a single-organization governance system.

Client Layer:
- Web Admin Interface (HTML, CSS, JavaScript)
- Mobile Student Application (Flutter)

Application Layer:
- Django Backend
- Django REST Framework (API Layer)

Data Layer:
- PostgreSQL Database

This system is NOT multi-tenant.
It is designed exclusively for the USG of USTP-Oroquieta.

---

## 2. Architectural Pattern

- Django MVT (Model-View-Template)
- RESTful API architecture for mobile integration
- Two-role authorization model (ADMIN / STUDENT)
- Modular Django app structure
- Service-layer business logic

There is no Super Admin layer.

ADMIN users have full system access.

---

## 3. Authorization Model

There are only two roles:

- ADMIN (Full system authority)
- STUDENT (Limited interaction access)

The `position` field is informational and organizational.
It does NOT restrict module access.

All ADMIN accounts can access all modules.

---

## 4. High-Level Flow

Student Mobile App
        ↓
REST API (Django REST Framework)
        ↓
Business Logic Layer (Service functions)
        ↓
PostgreSQL Database

Admin Web
        ↓
Django Template Rendering
        ↓
ORM
        ↓
Database

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
- campus_map
- analytics