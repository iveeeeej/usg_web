# Security and Permissions

---

## 1. Role Model

Only two roles exist:

- ADMIN
- STUDENT

There is no Super Admin.

All ADMIN accounts have full system authority.

---

## 2. Authorization Enforcement

Every protected endpoint must verify:

1. Authentication
2. Role validation
3. Resource ownership (if STUDENT)

---

## 3. Attendance Security

Attendance validation uses multi-layer security:

1. Verify JWT authentication
2. Verify user role (STUDENT)
3. Ensure user.is_verified = true
4. Verify active attendance session
5. Validate geofence using PostGIS
6. Validate time cutoff
7. Perform server-side face embedding comparison
8. Confirm liveness challenge completion
9. Prevent duplicate scans

Biometric verification:

- Face image is captured via mobile camera.
- Image is transmitted securely to backend.
- Backend generates embedding using pre-trained model.
- Embedding compared to stored template.
- Match must exceed configured similarity threshold.

The similarity threshold must be:

- Configurable in system settings
- Tested during development
- Tuned to minimize false positives and false negatives

---

## 4. File Upload Security

- Restrict file types (PDF, DOCX, etc.)
- Enforce file size limits
- Store in secure media directory
- Prevent script execution

---

## 5. Payment Security

- Verify transaction reference
- Prevent duplicate transactions
- Store immutable payment logs
- Do not auto-trust client confirmation

---

## 6. Logging

Critical actions must be logged:

- Event creation
- Attendance session opening
- Borrow approval
- Payment confirmation
- Report submission