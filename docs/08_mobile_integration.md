# Mobile Integration

---

## 1. Authentication Flow

1. User logs in
2. Backend returns JWT
3. Token stored securely
4. Token attached to every API request

Role returned in payload:
- ADMIN
- STUDENT

Mobile primarily serves STUDENT role.
ADMIN uses Web interface.

---

## 2. Account Verification Flow

Before accessing full application features,
students must complete biometric verification.

Process:

1. Student logs in (limited access).
2. Student navigates to Profile.
3. Clicks "Verify Account".
4. Liveness challenge is triggered.
5. Face image captured.
6. Image sent to backend.
7. Backend generates embedding.
8. Embedding stored in UserFaceProfile.
9. user.is_verified set to true.

Full feature access unlocked after verification.

---

## 3. QR Attendance Flow

Mobile sends:
- student_id
- event_id
- timestamp
- GPS coordinates
- captured face image

Backend validates:
- Authenticated STUDENT
- Active attendance session
- Cutoff time window
- Geofence boundary
- Generates face embedding
- Compares embedding to stored template
- Applies similarity threshold
- Prevents duplicate attendance

Attendance record created only after full server-side validation.

---

## 4. Student Module Access (Mobile)

Students can:
- View events
- Scan QR
- View violations
- Submit borrow requests
- View payment records
- Submit feedback

No administrative endpoints are exposed to mobile students.

---

## 5. Offline Handling

Mobile should:
- Detect network loss
- Retry submission
- Prevent duplicate scan submission