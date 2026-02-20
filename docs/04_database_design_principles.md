# Database Design Principles

---

## 1. Design Philosophy

The database design follows strict relational database engineering standards.

- Strong relational integrity
- Foreign key constraints enforced
- No duplicated data (Normalization up to 3NF)
- UUID primary keys for major entities
- Explicit indexing for frequently queried fields
- Audit timestamps on all models (created_at, updated_at)
- Immutable financial records once confirmed
- Controlled status transitions for workflow tables
- Soft delete only when business logic requires it

This system is designed for a single USG organization, but the schema remains structured for future extensibility.

---

## 2. Core Entities

User
Organization
Event
AttendanceSession
AttendanceRecord
Violation
Payment
BorrowItem
BorrowRequest
Announcement
DiscussionThread
DiscussionComment
Report
Feedback
CampusLocation

Note:
- There is no separate Role table.
- User contains a `role` field (ADMIN or STUDENT).
- User contains a `position` field (informational for ADMIN).

---

## 3. Identity Model

User includes:

- id (UUID)
- student_id (unique for students)
- email (unique)
- password_hash
- role (ADMIN or STUDENT)
- position (nullable, ADMIN only)
- is_active
- is_verified (boolean, default false)
- verified_at (timestamp, nullable)
- created_at
- updated_at

ADMIN users have full system authority.
Position does not affect authorization.

---

## 4. Biometric Identity Model

To address attendance proxy vulnerabilities, the system implements
backend-based biometric verification using face embeddings.

A new entity is introduced:

UserFaceProfile

UserFaceProfile includes:

- id (UUID)
- user_id (FK → User, unique)
- face_embedding (vector or JSONB)
- embedding_model_version
- created_at
- updated_at

Biometric Rules:

- Raw face images are NOT permanently stored.
- Only numerical face embeddings are stored.
- Embeddings are generated using a pre-trained deep learning model.
- The system performs ML inference only (no model training).
- Face comparison is executed server-side.
- Students must have `is_verified = true` before attendance is allowed.
- Face embeddings must not be returned in any API response.
- Embedding data must be stored securely and accessible only within the biometric service layer.
- Similarity threshold must be configurable and tunable.

---

## 5. Example Relationships

User (ADMIN)
    → creates Events
    → creates Announcements
    → approves BorrowRequests
    → creates Reports

User (STUDENT)
    → AttendanceRecords
    → Violations
    → Payments
    → BorrowRequests
    → Feedback

Event
    → has AttendanceSession
    → has Feedback
    → may generate Violations

AttendanceSession
    → belongs to Event
    → has multiple AttendanceRecords

AttendanceRecord
    → belongs to AttendanceSession
    → belongs to Student

Violation
    → belongs to Student
    → may relate to Event
    → may have associated Payment

BorrowItem
    → has multiple BorrowRequests

BorrowRequest
    → belongs to Student
    → belongs to BorrowItem

Report
    → created by ADMIN
    → structured content (JSON or controlled fields)

---

## 6. Data Integrity Rules

- A student may only have one attendance record per session.
- Attendance cannot be recorded outside the allowed time window.
- Attendance must pass geolocation validation.
- Violation hours must be non-negative.
- Payment amounts must be positive.
- Borrow request must follow valid status transitions:
    PENDING → APPROVED → RETURNED or REJECTED
- Reports must maintain structural template integrity.

---

## 7. Indexing Strategy

Indexes must be created for:

- student_id
- event_id
- attendance_session_id
- violation_id
- payment status
- created_at timestamps

These indexes ensure efficient analytics queries.

---

## 8. Data Lifecycle Policy

- Financial records are immutable once confirmed.
- Attendance records cannot be deleted once session is closed.
- Reports may be versioned or locked after submission.
- Soft deletion is allowed only for:
    - Announcements
    - Discussion posts (if needed)