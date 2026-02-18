# API Design Guidelines

## 1. REST Standards

Use standard HTTP methods:

GET → Retrieve
POST → Create
PUT → Update
DELETE → Remove

---

## 2. Example Endpoints

POST /api/auth/login
GET /api/events/
POST /api/events/{id}/attendance/
GET /api/user/profile/
POST /api/borrow/request/
GET /api/payments/history/

---

## 3. Authentication

Use JWT authentication.

Access token required for all protected endpoints.

---

## 4. Validation Rules

- All input validated
- No trust on frontend validation
- Location verified server-side
- Attendance cut-off enforced server-side
