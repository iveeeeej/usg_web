# Mobile Integration

## 1. Authentication Flow

1. User logs in
2. Backend returns JWT
3. Token stored securely
4. Token sent with every API request

---

## 2. QR Attendance Flow

1. Mobile scans QR
2. Mobile sends:
    - student_id
    - event_id
    - timestamp
    - GPS coordinates
3. Backend validates:
    - active session
    - cutoff time
    - geofence
4. Attendance recorded

---

## 3. Offline Handling

Mobile should:
- Gracefully handle network failure
- Retry submission
