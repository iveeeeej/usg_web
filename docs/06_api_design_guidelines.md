# API Design Guidelines

---

## 1. API Design Philosophy

Campus Connect follows an API-first architecture.

The API serves as the central integration layer between:
- the OFFICER web platform
- the STUDENT mobile application
- the backend business logic
- the PostgreSQL/PostGIS data layer

The API is the official enforcement boundary for:
- authentication
- authorization
- workflow validation
- ownership checks
- attendance validation
- service request rules
- reporting and record protection

The API must remain aligned with the current official system scope:

- single USG organization only
- two application roles only: OFFICER and STUDENT
- JWT-secured authentication
- attendance based on authenticated student identity, active session QR, and geolocation
- payment tracking implemented in the current scope
- biometrics excluded from the current active API baseline

---

## 2. API Style and Standards

Campus Connect uses REST-oriented API design.

Standard method usage:

- `GET` → retrieve data
- `POST` → create a new record or trigger a protected action
- `PUT` → full update of an existing record when appropriate
- `PATCH` → partial update of an existing record when appropriate
- `DELETE` → remove a record only when deletion is allowed by the business rules

General style expectations:
- endpoints should use clear resource-based naming
- nouns should be preferred over action-heavy endpoint names
- request and response formats should be JSON unless file upload/download requires otherwise
- endpoint behavior must be consistent across modules
- protected actions must never depend on client trust alone

Examples:
- `/api/events/`
- `/api/announcements/`
- `/api/attendance/sessions/`
- `/api/borrow/requests/`
- `/api/reports/`

---

## 3. Authentication

Campus Connect uses JWT authentication.

### 3.1 Login Endpoint

`POST /api/token/`

Returns:
- `access`
- `refresh`

### 3.2 Refresh Endpoint

`POST /api/token/refresh/`

Returns:
- refreshed `access` token when the refresh token is valid

### 3.3 Authentication Rule

All protected endpoints must require:

`Authorization: Bearer <access_token>`

JWT authentication is mandatory for both:
- Web Officer Interface
- Mobile Student Application

### 3.4 Identity Source Rule

The backend must treat the authenticated request user as the source of truth for identity.

This means:
- protected student actions must not rely on client-submitted `student_id` as the primary identity authority
- role must come from the authenticated backend user
- ownership checks must use authenticated backend identity

---

## 4. Role Access Model

Only two application roles exist:

- `OFFICER`
- `STUDENT`

There is no application-level Super Admin role inside the business API model.

Django superuser may still exist for framework administration, but it is not part of the application permission design.

### 4.1 OFFICER Access

OFFICER endpoints may include access to:
- dashboard data
- events and attendance session control
- announcements
- discussion moderation when applicable
- violation monitoring
- borrow review workflows
- payment monitoring and confirmation workflows
- reports and resolutions
- analytics and summaries

### 4.2 STUDENT Access

STUDENT endpoints may include access to:
- event viewing
- announcement viewing
- discussion participation where allowed
- attendance participation
- feedback submission
- borrow request submission
- lost-and-found viewing
- payment visibility
- campus tour content
- profile summary and notification viewing

### 4.3 Position Rule

The `position` field for OFFICER is informational only.

The API must not silently use `position` as an authorization layer unless the project is formally redesigned for position-based permissions.

---

## 5. Endpoint Grouping Strategy

For consistency, endpoints should be grouped by module and audience.

Recommended grouping examples:

### 5.1 Authentication
- `/api/token/`
- `/api/token/refresh/`

### 5.2 Dashboard and Officer-Focused
- `/api/officer/dashboard/`
- `/api/dashboard-message/`
- `/api/officer/analytics/`

`/api/dashboard-message/` is intended as a shared authenticated dashboard-content endpoint.
It can be read by authenticated clients and updated by OFFICER users so both the officer
web dashboard and the student mobile dashboard can surface the same current "What's New"
message when needed.

### 5.3 Governance and Communication
- `/api/events/`
- `/api/events/{id}/`
- `/api/events/{id}/attachments/`
- `/api/announcements/`
- `/api/announcements/{id}/`
- `/api/discussions/`
- `/api/discussions/{id}/comments/`
- `/api/notifications/`

For announcements in the current Phase 2 implementation:
- OFFICER users create announcements through `POST /api/announcements/`
- OFFICER users manage existing announcements through `/api/announcements/{id}/`
- STUDENT users only read published announcements through authenticated `GET` requests

### 5.4 Attendance and Accountability
- `/api/attendance/sessions/`
- `/api/attendance/sessions/{id}/`
- `/api/attendance/submit/`
- `/api/attendance/history/`
- `/api/violations/`
- `/api/feedback/`

### 5.5 Student Services
- `/api/borrow/items/`
- `/api/borrow/requests/`
- `/api/lost-found/`
- `/api/payments/`
- `/api/campus-locations/`

### 5.6 Records and Reporting
- `/api/resolutions/`
- `/api/reports/`
- `/api/reports/{id}/attachments/`

### 5.7 Profile and Summary
- `/api/profile/summary/`

Exact paths may evolve, but the grouping should remain predictable and role-aware.

---

## 6. Request and Response Principles

### 6.1 JSON as Standard Format

The API should use JSON request and response bodies for standard create/read/update flows.

### 6.2 Consistent Response Shape

Responses should be predictable.

Recommended response style:
- successful responses return the relevant resource or action result
- validation failures return structured field or rule errors
- permission failures return clear authorization errors
- not-found cases return standard not-found responses
- internal failures return safe, non-sensitive server error responses

### 6.3 Do Not Leak Sensitive Internals

Responses must not expose:
- password hashes
- internal secrets
- raw storage paths when avoidable
- sensitive server configuration details
- future biometric template data if such features are added later

---

## 7. Validation Rules

All important validation must happen server-side.

The client may help with UX validation, but final enforcement belongs to the API.

### 7.1 General Validation

The API must validate:
- required fields
- types and formats
- enum/status values
- date/time logic
- ownership rules
- workflow transitions
- duplicate-prevention rules
- file-upload constraints
- report structure constraints

### 7.2 Attendance Validation

Attendance requests must validate:
- authenticated request exists
- authenticated user role is `STUDENT`
- attendance session exists
- session is active
- QR/session payload is valid
- attendance is within allowed time window
- submitted geolocation is valid
- duplicate attendance does not already exist

### 7.3 Borrow Workflow Validation

Borrow requests must validate:
- item exists
- quantity requested is allowed
- request belongs to the authenticated student
- status transitions are valid
- approvals/rejections are OFFICER-only actions

### 7.4 Payment Validation

Payment-related API actions must validate:
- amount is positive
- related student exists
- related violation exists when applicable
- confirmation actions are authorized
- duplicate or conflicting payment references are rejected where reference logic is used

### 7.5 Report Validation

Report APIs must validate:
- report type is allowed
- required structured fields are present
- template integrity is preserved
- locked reports are not modified through standard edit actions

### 7.6 Explicit Current-Scope Exclusion

The current API validation rules do **not** include:
- biometric similarity threshold enforcement
- face embedding comparison
- liveness challenge as a required attendance step
- `user.is_verified` as a required attendance precondition

Those belong to future enhancement scope, not the current active API rules.

---

## 8. Attendance API Design Rules

Attendance is a sensitive transactional workflow and must be designed carefully.

### 8.1 Identity Model

The acting student identity must come from JWT-authenticated backend context.

The API must not treat a submitted `student_id` as higher authority than authenticated identity.

### 8.2 Session QR Model

The QR code must identify the active attendance session, not the student.

The attendance submission API should accept:
- session identifier or validated QR-derived session payload
- current coordinates
- optional accuracy metadata
- optional client timestamp for diagnostics

### 8.3 Duplicate Prevention

The API must ensure only one attendance record exists per student per session.

This should be backed by:
- service-layer validation
- database uniqueness constraints where applicable

### 8.4 Failure Handling

Attendance responses should clearly differentiate cases such as:
- session not active
- invalid QR/session
- outside allowed location
- after cutoff
- duplicate submission
- permission denied

This improves frontend behavior and reduces user confusion.

---

## 9. Ownership and Record Access Rules

For STUDENT-facing endpoints, the API must enforce ownership.

Examples:
- students can only retrieve their own attendance history
- students can only retrieve their own violations
- students can only retrieve their own payment records
- students can only retrieve their own borrow request history
- students can only retrieve their own profile summary and notification state

For OFFICER-facing endpoints, the API may expose broader organizational records within the authorized module scope.

Ownership checks must always be server-side.

---

## 10. Workflow Transition Design

APIs that change status must enforce valid transitions.

### 10.1 Borrow Example

Allowed example transitions:
- `PENDING → APPROVED`
- `PENDING → REJECTED`
- `APPROVED → RETURNED`

Invalid transitions must be rejected.

### 10.2 Attendance Session Example

Example session states may include:
- `DRAFT`
- `OPEN`
- `CLOSED`
- `ARCHIVED`

APIs must reject actions that do not fit the current session state.

### 10.3 Payment Example

Example payment states may include:
- `PENDING`
- `RECORDED`
- `CONFIRMED`
- `VOID`

Only allowed actors and valid transitions should be accepted.

### 10.4 Report Example

Reports may move through states such as:
- `DRAFT`
- `SUBMITTED`
- `LOCKED`

Standard update endpoints must reject modifications when the report state forbids editing.

---

## 11. Pagination, Filtering, and Query Design

List endpoints should support scalable retrieval.

Recommended support where appropriate:
- pagination
- filtering by status
- filtering by date range
- search by text fields
- ordering by created date or scheduled date

Examples:
- events filtered by upcoming/completed
- announcements filtered by published status or announcement type
- borrow requests filtered by status
- payments filtered by student or status
- reports filtered by type and status

Query behavior should remain predictable and documented.

---

## 12. File Upload and Attachment API Rules

Modules that support file uploads must use secure upload handling.

API rules should include:
- authenticated upload access where required
- allowed file-type enforcement
- size-limit enforcement
- controlled attachment association to parent records
- no direct trust in client-declared file type alone

Upload-enabled modules may include:
- event attachments
- discussion attachments
- report attachments
- lost-and-found images

Download or retrieval endpoints must also respect authorization and ownership where applicable.

---

## 13. Payment API Design Direction

The current payment module is tracking-first, not gateway-first.

### 13.1 Current-Scope API Behavior

The API should support:
- payment record retrieval
- payment entry creation where authorized
- status updates under controlled workflows
- confirmation recording by authorized OFFICER actions
- profile-linked payment visibility

### 13.2 Do Not Trust Client Payment Success Alone

The API must not mark payments as successful purely because the client claims payment succeeded.

### 13.3 Future Gateway Integration Note

If direct gateway integration is later added, the API may introduce:
- callback endpoints
- transaction verification endpoints
- reconciliation endpoints

These should be added only when that enhancement becomes officially in scope.

---

## 14. Security Expectations at the API Layer

The API is the main enforcement boundary for business security.

It must enforce:
- JWT authentication
- role validation
- ownership validation
- workflow validation
- secure attendance rules
- payment safeguards
- safe file handling
- report lock protection
- non-leaky error responses

The frontend must never be treated as the final security authority.

---

## 15. Error Handling Principles

Errors should be consistent and safe.

Recommended principles:
- use standard HTTP status codes
- return structured validation errors where possible
- avoid exposing stack traces or internal server details
- make role/permission failures distinguishable from validation failures
- provide clear client-usable messages for common transactional failures

Examples of important client-usable failures:
- invalid credentials
- token expired
- forbidden action
- not found
- duplicate attendance
- outside allowed location
- session closed
- invalid status transition

---

## 16. Versioning and Evolution

If the API changes significantly over time, versioning should be considered.

For the current project stage, internal consistency is more important than premature multi-version complexity.

Versioning can be introduced later if:
- mobile and web clients must support different release timelines
- breaking changes become unavoidable
- external integrations are added

---

## 17. Documentation Expectations

Every important endpoint should eventually document:
- purpose
- allowed roles
- request fields
- response fields
- validation rules
- ownership rules
- status transition rules where applicable

This is especially important for:
- attendance submission
- borrow review workflows
- payment status handling
- report submission and locking
- profile summary retrieval

---

## 18. Explicit Exclusions from Current Core API Scope

The following are **not part of the current active API baseline**:

- biometric verification endpoints as required attendance flow
- face embedding upload endpoints as required attendance flow
- liveness challenge endpoints as required attendance flow
- mandatory `is_verified` attendance checks
- multi-tenant organization-scoped API design

These may be added later only if the project officially enters that enhancement phase.

---

## 19. Future Enhancement Direction

Possible later API additions may include:
- biometric attendance reinforcement endpoints
- payment gateway callback endpoints
- advanced notification delivery endpoints
- deeper analytics endpoints
- richer audit and reconciliation endpoints

These must remain separate from the current official API baseline.

---

## 20. Summary

Campus Connect API design must remain aligned with the finalized system model.

The API should:
- enforce JWT-authenticated identity
- apply role-based and ownership-aware access control
- validate workflows server-side
- support governance, attendance, services, and reporting modules
- use session QR + geolocation attendance rules
- avoid reintroducing biometric-first logic into the current core design

The API is not just a transport layer.
It is the main enforcement layer for the business rules of Campus Connect.
