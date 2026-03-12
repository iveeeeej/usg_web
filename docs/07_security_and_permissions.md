# Security and Permissions

---

## 1. Security Model Overview

Campus Connect follows a role-based security model enforced through authenticated API access,
server-side validation, protected workflow rules, and controlled access to sensitive records.

The security design must align with the current official scope of the system:

- single USG organization only
- two application roles only: OFFICER and STUDENT
- JWT-secured API communication for web and mobile
- attendance secured through authenticated identity, active session QR validation, geolocation, cutoff rules, and duplicate prevention
- payment handled through tracked/recorded workflows in the current scope
- biometrics excluded from the current required core security flow

Security enforcement must be applied consistently across:
- authentication
- authorization
- resource ownership
- transactional workflow validation
- file handling
- payment and reporting actions
- logging and auditability

---

## 2. Role Model

Only two application roles exist:

- `OFFICER`
- `STUDENT`

There is no application-level Super Admin role inside Campus Connect.

Django superuser may still exist for backend maintenance and framework administration,
but it must not be treated as part of the business-level permission model.

### 2.1 OFFICER

OFFICER accounts have access to officer-level administrative modules.

This includes authority to manage functions such as:
- events
- attendance sessions
- announcements
- discussions where moderation applies
- violations
- borrow review workflows
- payment monitoring
- resolutions
- reports
- dashboards and analytics

### 2.2 STUDENT

STUDENT accounts are restricted to student-facing actions and records.

This includes:
- viewing events and announcements
- participating in attendance
- viewing personal violations and payments
- submitting feedback
- submitting service-related requests
- viewing profile summaries and notifications

### 2.3 Position Rule

If a user is an OFFICER, the `position` field is informational only.

`position` must not be used as a hidden authorization layer unless the system is formally redesigned to support position-based permissions.

---

## 3. Authentication Requirements

Campus Connect uses JWT authentication for protected API access.

### 3.1 Required Authentication Flow

Protected endpoints must require:
- a valid access token
- server-side authentication resolution
- backend-derived user identity

The system must not trust:
- client-declared roles
- manually submitted user identifiers as replacements for authenticated identity
- frontend-only session assumptions

### 3.2 Authentication Rules

- all protected endpoints must require authentication
- expired access tokens must be rejected
- refresh flow must be validated server-side
- logout must invalidate local client access state even if JWT remains stateless server-side
- sensitive transactions must always be revalidated through backend identity and permissions

### 3.3 Identity Source of Truth

For protected actions, user identity must come from the authenticated backend request context.

Examples:
- attendance should derive the acting student from JWT-authenticated user context
- borrow requests should derive requester identity from the authenticated session
- record ownership checks must use backend identity, not only client-supplied parameters

---

## 4. Authorization Enforcement

Every protected endpoint must enforce the following layers where applicable:

1. Authentication  
2. Role validation  
3. Resource ownership or access scope  
4. Workflow rule validation  
5. Sensitive-action safeguards

### 4.1 Role Validation

Examples:
- `/api/officer/...` endpoints require `role == OFFICER`
- student-facing protected endpoints require authenticated student access when the endpoint is student-specific

### 4.2 Ownership Validation

For STUDENT-facing resources, the backend must verify that the authenticated student is allowed to access the requested record.

Examples:
- a student may view only their own attendance history
- a student may view only their own violations
- a student may view only their own payment records
- a student may view only their own borrow requests unless a broader public view is intentionally allowed

### 4.3 Workflow Validation

Authorization alone is not enough.

A user may be authenticated and still be blocked if business workflow conditions are not satisfied.

Examples:
- attendance session is not active
- attendance cutoff has already passed
- borrow request transition is invalid
- report is already locked
- payment confirmation action is not allowed for the current record state

---

## 5. Attendance Security

Attendance is a high-risk workflow because it affects accountability, records, and possible violation generation.

The current official attendance security model is:

- JWT-authenticated student identity
- active attendance session validation
- session QR validation
- geolocation validation
- time window / cutoff validation
- duplicate attendance prevention
- server-side record creation only after all checks pass

### 5.1 Required Attendance Validation Layers

The backend must verify all of the following before creating an attendance record:

1. Request is authenticated  
2. Authenticated user exists and is active  
3. Authenticated user role is `STUDENT`  
4. Attendance session exists and is valid  
5. Attendance session is currently open or otherwise eligible for sign-in  
6. QR/session payload matches the active attendance session  
7. Attendance request is within allowed time window and cutoff rules  
8. Submitted location falls within allowed geolocation boundaries  
9. No existing attendance record already exists for the same student and session  

Only after all checks pass may the backend create the attendance record.

### 5.2 Geolocation Security

Attendance geolocation must be validated server-side.

Geolocation security rules:
- client GPS data must never be trusted blindly
- backend must compare submitted coordinates against the allowed session area
- validation should use PostGIS-aware logic
- allowable boundary rules must be explicit, such as center-radius or polygon boundary
- location accuracy metadata may be considered when applying acceptance rules

### 5.3 Duplicate Prevention

The system must prevent multiple attendance records for the same student in the same attendance session.

Protection should exist at both levels:
- service-level validation
- database-level uniqueness constraints where applicable

### 5.4 Session QR Validation

The QR code used for attendance must identify the attendance session, not the student.

Security expectations:
- QR/session payload must be validated server-side
- invalid, expired, or mismatched session payloads must be rejected
- attendance must not rely on school-ID QR as the core final design

### 5.5 Explicit Current-Scope Exclusions

The current attendance security model does **not** require:
- biometric verification
- face embedding comparison
- liveness challenge
- `user.is_verified`
- `verified_at`
- mandatory image capture for standard attendance

Those belong to future enhancement scope, not the current active security baseline.

---

## 6. Resource and Module Security

### 6.1 Announcements

- only OFFICER accounts may create and manage official announcements
- students may only access announcements intended for student viewing
- unpublished or archived announcements must not be exposed unless explicitly allowed by role

### 6.2 Discussion Forum

- authenticated access is required for protected discussion actions
- ownership and moderation rules must be server-side enforced
- deleted or moderated content must not remain publicly exposed through direct object access
- attachment access must follow the same ownership and visibility rules as the post or comment

### 6.3 Borrow Requests

- students may create borrow requests for themselves only
- approval or rejection actions must be OFFICER-only
- invalid status transitions must be blocked
- returned status must not be assigned unless the workflow allows it

### 6.4 Lost and Found

- create/update/delete authority must be explicitly controlled
- only authorized roles may manage official lost-and-found records if that is the chosen business rule
- uploaded images and item data must follow file and input validation rules

### 6.5 Reports and Resolutions

- only OFFICER accounts may create and manage official reports and resolutions
- locked reports must not be freely editable
- report type and template integrity must be enforced server-side
- file attachments must inherit report-level access control

### 6.6 Student Profile and Personal Records

Students must only be able to access their own personal records unless the module is intentionally public.

This includes:
- attendance history
- violation history
- payment records
- borrow request history
- profile summary details
- notification history

---

## 7. Input Validation Security

All important business validation must occur server-side.

The client may assist with basic usability validation, but it must never be treated as the final enforcement layer.

Required server-side validation includes:
- required-field validation
- type validation
- enum/status validation
- ownership validation
- date and time validation
- geolocation validation
- duplicate-prevention validation
- file upload validation
- report structure validation
- workflow transition validation

Examples:
- attendance cutoff must be enforced on the backend
- borrow status transitions must be validated on the backend
- payment status changes must be validated on the backend
- report locking rules must be enforced on the backend

---

## 8. File Upload Security

Any module that supports file or media upload must apply strict upload controls.

Minimum controls:
- allow only approved file types
- enforce size limits
- sanitize file names if needed
- store files outside executable paths
- prevent script execution from uploaded content
- validate MIME type and extension together where possible
- restrict raw path exposure
- require authenticated access for protected file retrieval

Modules that may require upload protection include:
- event attachments
- discussion attachments
- lost-and-found images
- report attachments
- other future document-based workflows

---

## 9. Payment Security

Payment records affect accountability and financial visibility, so they require stronger controls.

### 9.1 Current-Scope Payment Security

Because current payment handling is tracked/recorded first, the backend must enforce:

- positive amount validation
- valid student linkage
- valid violation linkage when payment is violation-related
- controlled status transitions
- restricted confirmation authority
- immutable or tightly controlled confirmed records
- duplicate-reference prevention where reference values are used
- no blind trust in client-confirmed payment success

### 9.2 Confirmation Controls

If payment confirmation is officer-mediated:
- only authorized OFFICER actions may confirm a payment
- confirmation should store who confirmed it and when
- confirmed entries should not be silently altered like draft records

### 9.3 Future Gateway Integration Note

If third-party online payment integration is added later:
- callback verification must be server-side
- transaction references must be validated
- reconciliation logs should be auditable
- the system must never trust client-only payment-success messages

---

## 10. Notification Security

Notifications may reference sensitive actions and records.

The system must ensure:
- user-specific notifications are delivered only to intended recipients
- read/unread state changes apply only to the correct user
- notification-linked records respect the same access controls as the source module
- a student cannot open another student’s notification state or related protected record

---

## 11. Logging and Auditability

Critical actions must be logged for accountability and operational traceability.

### 11.1 Actions That Should Be Logged

At minimum, log:
- login attempts where appropriate
- attendance session creation/opening/closing
- attendance submission outcomes
- announcement creation
- borrow approval or rejection
- payment recording and confirmation
- report submission
- report locking or revision actions
- resolution creation or approval actions where applicable

### 11.2 Logging Principles

- logs must be timestamped
- logs must identify actor when possible
- logs must avoid exposing sensitive secrets
- logs must support troubleshooting and audit review
- logs must remain consistent across important workflows

### 11.3 Current Development Logging Context

The current development environment already uses:
- console logging
- rotating file logging
- log file path: `backend/logs/django.log`

The log directory must exist, or the file handler may fail during application startup.

---

## 12. Data Protection Principles

Sensitive or important records must be protected against casual misuse or accidental corruption.

Security expectations:
- confirmed financial records should be effectively immutable except through controlled correction workflows
- attendance records should not be casually deleted after session closure
- audit-sensitive records should favor traceable correction over silent overwriting
- personal student data should only be visible where role and ownership rules permit

The system should prefer:
- traceability
- explicit state changes
- controlled correction workflows
over silent destructive changes.

---

## 13. API Security Expectations

Security policy must remain consistent with the API layer.

Protected API behavior should enforce:
- JWT authentication for web and mobile
- role restrictions on endpoint groups
- ownership restrictions for personal data
- validation of every sensitive transaction
- no direct trust in client-only state
- safe error responses that do not expose sensitive internals

The API layer must be treated as the enforcement boundary for business security.

---

## 14. Explicit Exclusions from Current Core Security Scope

The following are **not part of the current active required security model**:

- mandatory biometric verification before attendance
- `user.is_verified` requirement for attendance
- face embedding generation as a required live attendance step
- liveness challenge as a required live attendance step
- biometric similarity threshold enforcement in current attendance flow
- multi-tenant organization isolation logic

These may be explored later, but they are not part of the present official baseline.

---

## 15. Future Enhancement Direction

Future security enhancements may include:
- biometric attendance reinforcement
- liveness challenge workflows
- stronger push-notification infrastructure
- direct payment gateway callback verification layers
- expanded audit reporting
- more advanced fraud-detection or anomaly-detection checks

If biometrics is introduced later, it should be added as an optional or advanced attendance-security layer rather than treated as the foundation of the current attendance model.

---

## 16. Summary

Campus Connect security is based on:
- JWT-authenticated identity
- role-based authorization
- ownership-aware access control
- server-side workflow enforcement
- secure file and payment handling
- logging and auditability
- attendance security through session QR + geolocation + cutoff + duplicate prevention

The system must remain aligned with the finalized current scope.
Security rules should protect the platform without reintroducing older biometric-first assumptions into the active core design.