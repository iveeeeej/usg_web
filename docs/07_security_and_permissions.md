# Security and Permissions

## 1. Role-Based Access Control (RBAC)

Use Django Groups + Permissions.

Roles:
- Super Admin
- Organization Admin
- Officer
- Student

Each view must verify:

- Authentication
- Role permission
- Organization scope

---

## 2. Geolocation Validation

Attendance must verify:

- Student identity
- Event active session
- Within campus coordinate boundary
- Within allowed time window

---

## 3. File Upload Security

- Restrict file types
- Limit file size
- Store files securely
- Prevent direct execution

---

## 4. Payment Security

Payment validation must:
- Verify transaction ID
- Confirm payment status
- Prevent duplicate processing
