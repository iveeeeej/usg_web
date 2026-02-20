# API Design Guidelines

---

## 1. REST Standards

GET → Retrieve
POST → Create
PUT → Update
DELETE → Remove

---

## 2. Role Access Rules

ADMIN:
- Full access to administrative endpoints.

STUDENT:
- Limited to student-related endpoints only.

---

## 3. Example Endpoints

POST /api/auth/login
GET /api/events/
POST /api/events/{id}/attendance/
GET /api/profile/
POST /api/borrow/request/
GET /api/payments/history/

ADMIN endpoints must validate role.

---

## 4. Validation Rules

- All input validated server-side.
- Geolocation verified using PostGIS.
- Attendance cutoff strictly enforced.
- Duplicate attendance prevented.
- Borrow status transitions validated.