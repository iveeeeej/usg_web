# API Design Guidelines

---

## 1. REST Standards

GET → Retrieve  
POST → Create  
PUT → Update  
DELETE → Remove  

---

## 2. Authentication

Login Endpoint:

POST /api/token/

Returns:
- access token
- refresh token

Token Refresh:

POST /api/token/refresh/

All protected endpoints require:

Authorization: Bearer <access_token>

JWT authentication is mandatory for both Web and Mobile.

---

## 3. Role Access Rules

OFFICER:
- Full access to administrative endpoints.

STUDENT:
- Limited to student-related endpoints only.

Example protected endpoint:

GET /api/officer/dashboard/
Requires:
- Authenticated user
- role == OFFICER

---

## 4. Validation Rules

- All input validated server-side.
- Geolocation verified using PostGIS.
- Attendance cutoff strictly enforced.
- Duplicate attendance prevented.
- Borrow status transitions validated.
- Biometric similarity threshold enforced.