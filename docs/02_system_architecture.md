# System Architecture

## 1. Architecture Overview

Campus Connect follows a layered architecture:

Client Layer:
- Web Admin (HTML/CSS/JS)
- Mobile App (Flutter)

Application Layer:
- Django Backend
- Django REST Framework (API Layer)

Data Layer:
- PostgreSQL Database

---

## 2. Architectural Pattern

The system follows:

- MVC pattern (Django MVT)
- RESTful API for mobile integration
- Role-based access control
- Modular app structure

---

## 3. High-Level Flow

Student Mobile App
        ↓
REST API (Django REST Framework)
        ↓
Business Logic Layer (Django Services)
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

## 4. Modular Design

Each major feature is a Django app:

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
