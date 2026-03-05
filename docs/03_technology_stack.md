# Technology Stack

---

## Backend

Framework: Django
API Layer: Django REST Framework
Language: Python 3.14.3
Authentication: Django Auth + JWT
Database: PostgreSQL
GIS Support: PostGIS (for geolocation validation)

Django is responsible for:
- Authentication
- Authorization
- Business logic
- File handling
- Security validation
- Analytics processing

Supabase is NOT used.

Authentication Implementation:
- Custom User model (student_id as USERNAME_FIELD)
- JWT via djangorestframework-simplejwt
- Token-based authorization for web and mobile

Environment Configuration:
- python-dotenv (.env loading)

PostgreSQL Driver:
- psycopg2-binary

---

## Web Frontend

Languages:
- HTML5
- CSS3
- JavaScript

Framework:
- Bootstrap

Frontend Rendering:
- Static HTML + JavaScript
- API-driven rendering (no server-side templates for admin dashboard)

---

## Mobile Application

Language: Dart
Framework: Flutter
API Communication: REST (JSON)
Authentication: JWT Token-based

---

## Database

Primary DBMS: PostgreSQL

Reason:
- Strong relational integrity
- Advanced indexing
- JSONB support
- PostGIS geospatial validation
- Production-grade reliability