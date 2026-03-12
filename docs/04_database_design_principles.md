# Database Design Principles

---

## 1. Design Philosophy

The database design for Campus Connect follows a strict relational and workflow-oriented structure.

The schema is designed to support:
- strong relational integrity
- normalized core transactional data
- clear ownership of records
- controlled workflow state transitions
- auditability of important actions
- efficient querying for dashboards, monitoring, and analytics
- a single USG organization deployment

The database is designed for the **current official core scope** of Campus Connect.

This means the schema must directly support:
- governance and communication
- attendance and accountability
- student services
- legislative records and structured reporting
- profile summary and monitoring views

The schema should avoid introducing advanced entities that belong only to future enhancement scope.

Core design rules:
- foreign key constraints must be enforced
- UUID primary keys should be used for major entities
- timestamps should exist on all important transactional models
- duplicated data should be minimized
- derived summaries should not replace source transactional records
- workflow tables must use explicit statuses
- destructive deletion should be limited where records affect accountability, finance, or reporting

---

## 2. Single-Organization Schema Rule

Campus Connect is designed for **one USG organization only**.

Because the current system is not multi-tenant:
- there is no tenant isolation model
- there is no need to attach an `organization_id` foreign key to every major table
- the schema should not be shaped around multiple parallel organizations

For the current scope:
- a separate `Organization` entity is **not required as a core transactional table**
- organizational identity can be treated as system-level configuration rather than a tenancy model

If the project later needs formal organizational metadata, it may use a lightweight
configuration or profile table. However, the present schema should not pretend that the
system is multi-organization when the architecture explicitly says it is not.

---

## 3. Identity and Access Model

Campus Connect uses only **two application roles**:
- `OFFICER`
- `STUDENT`

There is no separate Role table in the current design.

The `User` model contains the role directly.

### 3.1 User Entity

`User` should contain:

- `id` (UUID, PK)
- `student_id` (unique, indexed)
- `email` (unique, indexed)
- `password_hash`
- `role` (`OFFICER` or `STUDENT`)
- `position` (nullable, OFFICER only, informational only)
- `first_name`
- `middle_name` (nullable if needed)
- `last_name`
- `year_level` (nullable when not applicable)
- `section` (nullable when not applicable)
- `course` (nullable when not applicable)
- `is_active`
- `created_at`
- `updated_at`

Important rules:
- `position` is **organizational metadata only**
- `position` does **not** drive authorization
- all OFFICER accounts share the same application-level authority
- authentication identity comes from the authenticated backend user, not from client-submitted role claims

### 3.2 Fields Removed from Current Core Scope

The following should **not** be part of the current core `User` schema:
- `is_verified`
- `verified_at`

Those fields belonged to the older biometric attendance direction and no longer match the finalized current scope.

---

## 4. Domain-Based Core Entity Model

The schema should be organized by functional domain.

### 4.1 Governance and Communication Domain

#### Event

`Event` is the primary scheduled governance/activity record.

`Event` should contain:
- `id` (UUID, PK)
- `title`
- `description`
- `event_type`
- `start_datetime`
- `end_datetime`
- `venue`
- `status`
- `audience_scope` (single-organization or selected internal audience)
- `audience_label` (nullable descriptive targeting field if needed)
- `created_by` (FK → User, OFFICER)
- `published_at` (nullable)
- `created_at`
- `updated_at`

Notes:
- `event_type` may distinguish regular events from general assemblies
- using `event_type` avoids duplicating schedule structures across separate but similar tables
- the calendar view should be derived from scheduled event records rather than from a separate calendar source-of-truth table

#### EventAttachment

Used for event-related documents or files.

`EventAttachment` should contain:
- `id` (UUID, PK)
- `event_id` (FK → Event)
- `file_name`
- `file_path` or storage reference
- `file_type`
- `uploaded_by` (FK → User)
- `created_at`

This supports the concept paper’s event-related document handling without forcing documents into the Event table itself.

#### Announcement

`Announcement` should contain:
- `id` (UUID, PK)
- `title`
- `content`
- `status`
- `published_at`
- `created_by` (FK → User, OFFICER)
- `created_at`
- `updated_at`
- `deleted_at` (nullable, only if soft delete is allowed)

Students can view announcements, but only officers create and manage them.

#### DiscussionThread

`DiscussionThread` should contain:
- `id` (UUID, PK)
- `title`
- `content`
- `created_by` (FK → User)
- `status`
- `created_at`
- `updated_at`
- `deleted_at` (nullable if moderated soft deletion is supported)

#### DiscussionComment

`DiscussionComment` should contain:
- `id` (UUID, PK)
- `thread_id` (FK → DiscussionThread)
- `parent_comment_id` (nullable FK → DiscussionComment) for replies
- `content`
- `created_by` (FK → User)
- `created_at`
- `updated_at`
- `deleted_at` (nullable)

#### DiscussionAttachment (optional but recommended)

If the discussion module supports media:
- `id` (UUID, PK)
- `thread_id` (nullable FK → DiscussionThread)
- `comment_id` (nullable FK → DiscussionComment)
- `file_name`
- `file_path`
- `file_type`
- `uploaded_by` (FK → User)
- `created_at`

At least one of `thread_id` or `comment_id` must be present.

#### Notification

A system-level notification definition table is recommended.

`Notification` should contain:
- `id` (UUID, PK)
- `title`
- `message`
- `notification_type`
- `source_module`
- `source_record_id` (nullable generic reference)
- `created_at`

#### UserNotification

Per-user delivery/read state should be separated from the notification definition itself.

`UserNotification` should contain:
- `id` (UUID, PK)
- `notification_id` (FK → Notification)
- `user_id` (FK → User)
- `is_read`
- `read_at` (nullable)
- `created_at`

This allows one system event to fan out to multiple student or officer recipients.

---

## 5. Attendance and Accountability Domain

Attendance must reflect the finalized official workflow:
- authenticated user identity
- active attendance session
- session QR validation
- geolocation validation
- cutoff enforcement
- duplicate prevention

### 5.1 AttendanceSession

`AttendanceSession` should contain:
- `id` (UUID, PK)
- `event_id` (FK → Event)
- `session_kind` (for example sign-in / sign-out if needed)
- `status`
- `open_at`
- `close_at`
- `cutoff_at` (nullable if separate from close time)
- `qr_token` or `qr_payload_hash`
- `allowed_center_point` (PostGIS geography/geometry point, if center-radius model is used)
- `allowed_radius_meters` (nullable if polygon model is used)
- `allowed_area` (nullable PostGIS polygon if polygon model is used)
- `created_by` (FK → User, OFFICER)
- `created_at`
- `updated_at`

Notes:
- the QR should identify the session, not the student
- geolocation validation should rely on PostGIS-friendly fields
- session status should be explicit, such as `DRAFT`, `OPEN`, `CLOSED`, `ARCHIVED`

### 5.2 AttendanceRecord

`AttendanceRecord` should contain:
- `id` (UUID, PK)
- `attendance_session_id` (FK → AttendanceSession)
- `student_id_ref` (FK → User, STUDENT)
- `recorded_at`
- `attendance_status`
- `captured_point` (PostGIS geography/geometry point)
- `location_accuracy_meters` (nullable)
- `client_recorded_at` (nullable, for diagnostics only)
- `created_at`

Important rule:
- there must be **one attendance record per student per attendance session**

Recommended unique constraint:
- (`attendance_session_id`, `student_id_ref`)

### 5.3 Violation

`Violation` should contain:
- `id` (UUID, PK)
- `student_id_ref` (FK → User, STUDENT)
- `event_id` (nullable FK → Event)
- `attendance_record_id` (nullable FK → AttendanceRecord)
- `violation_type`
- `description`
- `service_hours_required`
- `service_hours_completed`
- `status`
- `created_at`
- `updated_at`

This supports both monitoring and service-hour accountability resulting from missed attendance or related obligations.

### 5.4 Feedback

`Feedback` should contain:
- `id` (UUID, PK)
- `event_id` (FK → Event)
- `student_id_ref` (FK → User, STUDENT)
- `rating` (nullable if multi-format feedback is supported)
- `comment` (nullable)
- `submitted_at`
- `created_at`

Recommended unique constraint:
- (`event_id`, `student_id_ref`)

This prevents duplicate event feedback submissions unless the business rules explicitly allow revisions.

---

## 6. Student Services Domain

### 6.1 BorrowItem

`BorrowItem` should contain:
- `id` (UUID, PK)
- `item_name`
- `description`
- `quantity_total`
- `quantity_available`
- `status`
- `created_at`
- `updated_at`

### 6.2 BorrowRequest

`BorrowRequest` should contain:
- `id` (UUID, PK)
- `student_id_ref` (FK → User, STUDENT)
- `borrow_item_id` (FK → BorrowItem)
- `purpose`
- `quantity_requested`
- `requested_start`
- `requested_end`
- `status`
- `reviewed_by` (nullable FK → User, OFFICER)
- `reviewed_at` (nullable)
- `decision_notes` (nullable)
- `returned_at` (nullable)
- `created_at`
- `updated_at`

Recommended statuses:
- `PENDING`
- `APPROVED`
- `REJECTED`
- `RETURNED`

### 6.3 LostFoundItem

`LostFoundItem` should contain:
- `id` (UUID, PK)
- `item_name`
- `description`
- `image_path` (nullable)
- `date_found` (nullable)
- `location_found`
- `claim_status`
- `created_by` (FK → User, typically OFFICER)
- `created_at`
- `updated_at`

This directly supports the lost-and-found behavior described in your concept paper.

### 6.4 Payment

The current payment scope is **tracked/recorded first**, not gateway-first.

`Payment` should contain:
- `id` (UUID, PK)
- `student_id_ref` (FK → User, STUDENT)
- `violation_id` (nullable FK → Violation)
- `payment_type`
- `amount`
- `status`
- `payment_method` (nullable)
- `reference_number` (nullable)
- `recorded_by` (nullable FK → User, OFFICER)
- `recorded_at` (nullable)
- `confirmed_by` (nullable FK → User, OFFICER)
- `confirmed_at` (nullable)
- `notes` (nullable)
- `created_at`
- `updated_at`

Suggested `payment_type` examples:
- `CONTRIBUTION`
- `VIOLATION`

Suggested `status` examples:
- `PENDING`
- `RECORDED`
- `CONFIRMED`
- `VOID`

This structure supports manual/tracked confirmation now while leaving room for future gateway integration later.

### 6.5 CampusLocation

`CampusLocation` should contain:
- `id` (UUID, PK)
- `name`
- `description`
- `building_or_area`
- `latitude` or geospatial point
- `longitude` or geospatial point
- `image_path` (nullable)
- `status`
- `created_at`
- `updated_at`

This powers the campus tour module.

---

## 7. Legislative Records and Structured Reporting Domain

### 7.1 Resolution

`Resolution` should contain:
- `id` (UUID, PK)
- `title`
- `reference_code` (nullable but recommended unique if used)
- `content`
- `status`
- `created_by` (FK → User, OFFICER)
- `approved_at` (nullable)
- `created_at`
- `updated_at`

### 7.2 Report

Rather than separate physical tables for each report type, the schema should use one structured `Report` entity with a controlled report type.

`Report` should contain:
- `id` (UUID, PK)
- `report_type`
- `title`
- `status`
- `created_by` (FK → User, OFFICER)
- `submitted_at` (nullable)
- `locked_at` (nullable)
- `content_json` or structured controlled fields
- `version_number`
- `created_at`
- `updated_at`

Suggested `report_type` values:
- `AWFP`
- `PRESIDENT`
- `FINANCIAL`
- `AUDITOR`
- `ACCOMPLISHMENT`

This keeps reporting extensible while preserving structured template rules.

### 7.3 ReportAttachment

`ReportAttachment` should contain:
- `id` (UUID, PK)
- `report_id` (FK → Report)
- `file_name`
- `file_path`
- `file_type`
- `uploaded_by` (FK → User)
- `created_at`

### 7.4 ReportAuditLog (recommended)

If report revision tracking is important:
- `id` (UUID, PK)
- `report_id` (FK → Report)
- `acted_by` (FK → User)
- `action_type`
- `notes` (nullable)
- `created_at`

This is useful for locking, revising, and submission auditability.

---

## 8. Derived Views and Non-Transactional Summaries

Some important screens should be treated as **derived views**, not primary source tables.

### 8.1 Student Profile Summary

The student profile summary should be derived from:
- `User`
- `AttendanceRecord`
- `Violation`
- `Payment`
- `BorrowRequest`
- other related transactional records when needed

This summary should not become an independent source of truth if it only duplicates already stored data.

### 8.2 Dashboard and Analytics Views

Officer dashboards and analytics should be computed from transactional tables through:
- queries
- database views
- materialized views when performance requires it
- aggregation services in the backend

The analytics layer should summarize data, not replace the transactional model.

---

## 9. Relationship Overview

Recommended high-level relationships:

`User (OFFICER)`
- creates `Event`
- creates `Announcement`
- creates `AttendanceSession`
- reviews `BorrowRequest`
- creates `Resolution`
- creates `Report`

`User (STUDENT)`
- has many `AttendanceRecord`
- has many `Violation`
- has many `Payment`
- has many `BorrowRequest`
- has many `Feedback`
- receives many `UserNotification`

`Event`
- has many `EventAttachment`
- has many `AttendanceSession`
- has many `Feedback`
- may have many `Violation`

`AttendanceSession`
- belongs to `Event`
- has many `AttendanceRecord`

`AttendanceRecord`
- belongs to `AttendanceSession`
- belongs to `User (STUDENT)`

`Violation`
- belongs to `User (STUDENT)`
- may belong to `Event`
- may reference `AttendanceRecord`
- may have related `Payment` records

`BorrowItem`
- has many `BorrowRequest`

`BorrowRequest`
- belongs to `BorrowItem`
- belongs to `User (STUDENT)`

`Notification`
- has many `UserNotification`

`UserNotification`
- belongs to `Notification`
- belongs to `User`

`Report`
- has many `ReportAttachment`
- may have many `ReportAuditLog`

---

## 10. Data Integrity Rules

The following rules should be enforced at the schema and service level:

### 10.1 Identity and Access
- `student_id` must be unique
- `email` must be unique
- `role` must only allow `OFFICER` or `STUDENT`
- `position` must not be treated as an authorization key

### 10.2 Attendance
- one student may only have one attendance record per session
- attendance cannot be recorded outside allowed session rules
- attendance must pass geolocation validation
- attendance must use a valid active session QR payload
- attendance identity must come from authenticated user context, not a client-trusted submitted identity alone

### 10.3 Violations
- service hours must never be negative
- completed service hours must not exceed logical business rules unless explicitly allowed
- violation status changes must be controlled

### 10.4 Borrow
- borrow requests must follow valid status transitions
- approved requests must not exceed available quantity
- returned items must update availability consistently

### 10.5 Payments
- payment amounts must be positive
- violation-linked payments must reference valid violation records when applicable
- confirmed payment records should not be silently editable like draft records
- duplicate confirmed entries should be prevented by service logic and reference validation rules

### 10.6 Reports and Resolutions
- report types must be restricted to approved values
- structured report content must preserve template integrity
- locked reports must not be freely editable
- resolution references should remain traceable and unique when a reference code is used

---

## 11. Indexing Strategy

Indexes should be added for frequently queried and filtering fields.

Recommended indexes include:

### User
- `student_id`
- `email`
- `role`

### Event / Announcement / Discussion
- `start_datetime`
- `status`
- `published_at`
- `created_by`

### Attendance
- `attendance_session_id`
- `student_id_ref`
- unique index on (`attendance_session_id`, `student_id_ref`)
- spatial indexes for geolocation fields where PostGIS is used
- `recorded_at`

### Violations / Payments / Borrow
- `student_id_ref`
- `status`
- `violation_id`
- `recorded_at` / `confirmed_at`
- `borrow_item_id`

### Reports / Resolutions
- `report_type`
- `status`
- `submitted_at`
- `reference_code` (if used)

### Notifications
- `user_id`
- `is_read`
- `created_at`

These indexes are needed for fast filtering, profile lookups, dashboards, and analytics queries.

---

## 12. Data Lifecycle Policy

### 12.1 Financial Records
Confirmed financial records should be treated as effectively immutable except through explicit correction workflows.

### 12.2 Attendance Records
Attendance records should not be deleted once the session is closed, except through tightly controlled administrative correction logic.

### 12.3 Borrow and Violation Records
Borrow, violation, and related accountability records should remain auditable and should not be casually removed.

### 12.4 Announcements and Discussion
Soft deletion may be allowed for announcements, threads, or comments when moderation or cleanup requires it.

### 12.5 Reports
Reports may support:
- draft state
- submission state
- lock state
- version tracking

The exact implementation may vary, but structured governance records should remain historically traceable.

---

## 13. Explicit Exclusions from Current Core Schema

The following are **not part of the active current core schema**:

- `UserFaceProfile`
- mandatory biometric attendance tables
- `is_verified`
- `verified_at`
- biometric embeddings as current required user data
- multi-tenant organization ownership modeling

These belong to future enhancement scope, not the present official database baseline.

---

## 14. Future Enhancement Direction

If biometrics is introduced later as an optional attendance reinforcement layer, it should be added separately and carefully.

Possible future entities may include:
- `UserFaceProfile`
- biometric verification logs
- liveness verification results

If direct payment gateway integration is later added, future tables may include:
- gateway transaction records
- callback logs
- reconciliation logs

These should be added only when the project officially enters that enhancement phase.

---

## 15. Summary

The Campus Connect database should be modeled around the current official product scope,
not around older assumptions.

The schema should support:
- a single USG organization
- two-role access model
- event-driven governance workflows
- QR session + geolocation attendance
- service and accountability tracking
- structured reporting
- derived student summaries
- dashboard and analytics queries

The database must remain disciplined, normalized, and extensible without forcing future-enhancement features into the current core design.