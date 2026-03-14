# Mobile Integration

---

## 1. Purpose of Mobile Integration

The mobile application serves as the primary student-facing client of Campus Connect.

It is designed to allow STUDENT users to securely access participation, communication,
service, and record-related features through a mobile interface connected to the same
centralized backend used by the officer web platform.

The mobile app is not an independent system. It is a client application that communicates
with the Campus Connect backend through JWT-secured REST API calls.

The mobile client may be maintained in a separate repository from the backend and officer
web frontend. This document therefore describes the system-wide mobile integration contract
and backend communication rules, not only the contents of the current repository.

The mobile layer must remain fully aligned with the core system rules:

- single USG organization only
- only two application roles: OFFICER and STUDENT
- JWT-secured API communication
- attendance based on authenticated access, active session QR validation, and geolocation
- payment tracking available in the current scope
- biometrics excluded from the current core mobile workflow

---

## 2. Role Boundary on Mobile

Mobile primarily serves the STUDENT role.

The student mobile application is intended for:
- viewing events and announcements
- participating in attendance sessions
- receiving notifications and reminders
- interacting with discussion and communication features
- submitting service-related requests
- viewing personal summaries and records

Even if an OFFICER account is technically able to authenticate through mobile, the mobile
application does not function as the official administrative interface of the system.

Administrative operations such as:
- event creation
- attendance session control
- report management
- approval workflows
- analytics review
- officer dashboard monitoring

must remain centered on the web officer platform.

This keeps the mobile app focused on student participation and prevents role-boundary
confusion between the student client and the officer management system.

---

## 3. Authentication Flow

The mobile app uses JWT authentication through the backend API.

### 3.1 Login Flow

1. User submits credentials to `/api/token/`
2. Backend validates the account
3. Backend returns:
   - access token
   - refresh token
4. Mobile stores the tokens securely
5. Access token is attached to protected API requests
6. Refresh token is used only for token renewal
7. User role is derived from the authenticated backend account

The mobile application must not independently decide the user’s authority level.
Role must always come from the backend-authenticated user record.

### 3.2 Session Handling Rules

The mobile app must support:
- secure token storage
- automatic token refresh when allowed
- forced logout if refresh fails
- session expiration handling
- explicit logout that clears local tokens and protected cached data

### 3.3 Authenticated Identity Rule

The authenticated account identity comes from JWT.

This means the mobile application must not treat manually submitted identifiers such as
`student_id` as the primary source of user identity for protected workflows.

The backend should derive the acting student from the authenticated request context.

---

## 4. Mobile Navigation Scope

The student mobile app should expose only student-facing modules.

Recommended primary mobile sections:

- Home
- Events
- Announcements
- General Assembly
- Discussion Forum
- Attendance
- Violations
- Borrow
- Lost and Found
- Payment
- Campus Tour
- Feedback
- Profile Summary
- Notifications

The exact UI layout may vary, but the module boundaries should remain consistent with the
business scope of Campus Connect.

---

## 5. Home / Student Dashboard Behavior

The Home screen acts as the main student entry point.

It should provide a consolidated view of the most relevant student-facing information,
such as:

- currently active or upcoming events
- recent announcements
- active attendance opportunities
- reminders or notifications
- pending service-related items
- account-related alerts
- shortcuts to commonly used student modules

The Home screen is a visibility layer only.
It should summarize information from other modules without replacing their full detail views.

---

## 6. Events and General Assembly on Mobile

### 6.1 Event Visibility

Students should be able to:
- view event list
- open event details
- view date, time, venue, description
- view attached event-related information if exposed to students
- see whether attendance is available, upcoming, closed, or completed

### 6.2 General Assembly Visibility

Students should be able to:
- view upcoming general assemblies
- open meeting details
- see whether the assembly applies to them
- receive schedule-related reminders or updates when applicable

### 6.3 Calendar Behavior

The mobile app should present schedule visibility for the single USG environment only.

This is not a multi-organization calendar model.
The mobile app should reflect the current organizational event schedule relevant to the
single Campus Connect deployment.

---

## 7. Announcements and Discussion Forum

### 7.1 Announcements

Students should be able to:
- view active announcements
- open announcement details
- see posting date and content
- optionally dismiss an announcement from their own view if the product design keeps that behavior

Announcements are read-oriented for students.
Students do not create official announcements.

### 7.2 Discussion Forum

The mobile app should support student participation in the in-system discussion space.

This may include:
- viewing discussion threads
- creating student posts if allowed by policy
- adding comments or replies
- reacting to posts if reactions are implemented
- viewing attached media if supported

The discussion feature should remain inside the Campus Connect ecosystem so communication
is not fragmented across external apps.

---

## 8. Official Attendance Flow

Attendance is the most critical mobile workflow and must follow the finalized system rule.

### 8.1 Attendance Identity Model

Attendance identity must come from:
- authenticated JWT user
- active attendance session
- session QR validation
- geolocation validation

The mobile app must not rely on school-ID QR as the final core attendance design.

The mobile app also must not rely on manually entered student identity fields
as the primary source of attendance identity.

### 8.2 Student Attendance Flow

Recommended flow:

1. Student logs in to the mobile app
2. Student opens the relevant event or attendance screen
3. Student taps the attendance action when a session is active
4. Student scans the QR code for the active attendance session
5. Mobile app captures current geolocation and related metadata
6. Mobile app sends attendance request to backend
7. Backend validates:
   - authenticated user is STUDENT
   - session is active
   - QR/session payload is valid
   - attendance is inside allowed time window
   - location is within allowed range
   - no existing duplicate attendance record exists
8. Backend creates attendance record if validation succeeds
9. Mobile app displays success or failure result clearly

### 8.3 Data That Mobile Should Send for Attendance

Attendance requests should send only the information necessary for validation.

Recommended attendance payload includes:
- session identifier or QR-derived session payload
- current GPS coordinates
- location accuracy metadata if available
- client timestamp if useful for debugging or logging

The backend should derive the student identity from JWT rather than trusting a submitted
`student_id` as the authoritative user reference.

### 8.4 What Mobile Should Not Require in Current Scope

The mobile attendance flow should not require:
- biometric verification
- face capture
- liveness challenge
- face embedding upload
- mandatory image transmission for standard attendance

Those belong to possible future enhancement, not the current mobile core scope.

### 8.5 Attendance Result States

The mobile app should clearly present attendance outcomes such as:
- success
- duplicate attempt
- session closed
- session not active
- outside allowed location
- after cutoff
- invalid QR/session
- network or permission failure

This improves transparency and reduces student confusion during sign-in.

---

## 9. Violations and Accountability Visibility

Students should be able to view:
- violation records linked to missed obligations
- assigned service hours where applicable
- violation-related payment status if supported
- basic explanation of the violation source when available

The mobile app is mainly for visibility and acknowledgment on this module.
Core violation administration remains officer-side.

---

## 10. Feedback Submission

The mobile app should support event-related feedback after eligible events.

Students should be able to:
- open feedback-eligible completed events
- rate the event
- submit comments if required
- see whether feedback has already been submitted

Feedback submission windows must be enforced by the backend.

The mobile app should not assume that feedback is always open.
It must reflect the actual backend eligibility rules.

---

## 11. Student Services on Mobile

### 11.1 Borrow

Students should be able to:
- browse available borrowable items if exposed
- submit borrow requests
- specify purpose and borrowing period
- view request status
- view request history where applicable

The mobile app does not approve or reject borrow requests.
It only supports student-side submission and visibility.

### 11.2 Lost and Found

Students should be able to:
- view lost/found item listings
- open item details
- see item description, image, and status where applicable
- follow any claim or inquiry process defined by the backend

### 11.3 Payment

In the current scope, mobile payment behavior should prioritize visibility and tracking.

Students should be able to:
- view contribution records
- view violation-related payment records
- view balances or status if available
- see whether a payment is pending, recorded, or confirmed based on backend rules

Direct online payment gateway processing is not required for the current core mobile workflow.

If gateway integration is added later, it should be treated as an extension of the current
payment tracking module rather than as a dependency for the first complete mobile version.

### 11.4 Campus Tour

Students should be able to:
- browse campus locations
- open location details
- view building/office/facility descriptions
- use simple campus-orientation visuals if implemented

The campus tour is informational.
It is not intended to replicate full map-navigation platforms.

---

## 12. Profile Summary on Mobile

The mobile app should provide a consolidated student profile view.

This summary may include:
- personal profile information
- attendance totals or summaries
- violation and service-hour summary
- payment summary
- borrow/request summary
- recent activity
- overall account-related status

This profile view is important because it gives the student one place to review
their standing instead of checking separate manual records.

---

## 13. Notifications and Alerts

The mobile app should support student-facing notifications for important system events.

Examples include:
- new announcements
- upcoming events
- general assembly reminders
- attendance session reminders if implemented
- borrow request results
- payment-related updates
- other account-related alerts

Notifications may be implemented as:
- in-app alerts
- notification center records
- push notifications in later stages if infrastructure supports them

At minimum, the mobile app should provide a consistent in-system way to surface
important student-facing updates.

---

## 14. API Communication Rules for Mobile

### 14.1 General Rules

All protected mobile actions must use JWT-authenticated API calls.

The mobile app must not:
- bypass backend validation
- enforce business rules only on the client
- assume successful actions before backend confirmation
- expose officer-only endpoints in the student experience

### 14.2 Backend as Source of Truth

The backend remains the source of truth for:
- user identity
- role
- attendance validity
- request status
- payment status
- notification state
- record ownership
- eligibility windows

### 14.3 Media and File Handling

If the mobile app uploads files or media in supported modules, it must:
- use approved file types only
- respect file size limits
- follow secure upload endpoints
- avoid exposing raw storage paths
- rely on backend validation for all uploads

---

## 15. Offline and Network Handling

The mobile app must distinguish between:
- read-oriented features that may tolerate temporary caching
- critical transactional features that require live backend validation

### 15.1 Features That May Use Cached Read Data

Examples:
- event list
- announcements
- campus tour information
- previously loaded profile summaries
- discussion content already retrieved

### 15.2 Features That Should Require Live Validation

Examples:
- attendance submission
- borrow request submission
- payment-status-changing actions
- feedback submission windows if time-sensitive

Attendance especially should not be treated as an offline-first action because the backend
must validate:
- active session state
- cutoff time
- geolocation
- duplicate prevention

### 15.3 Network Failure Behavior

The mobile app should:
- detect no-connection state
- show clear error messages
- prevent accidental repeated submission
- allow safe retry where appropriate
- avoid creating duplicate transactions or requests from repeated taps

---

## 16. Security Principles for Mobile Integration

The mobile app must follow these security principles:

- never trust client role claims without backend verification
- never treat submitted student identifiers as higher authority than JWT identity
- never make biometrics a required mobile core dependency in current scope
- never expose officer-only admin workflows to the student client
- never treat payment success as valid without backend-confirmed status
- never bypass server-side validation for attendance, requests, or record ownership

Sensitive operations must always be confirmed by the backend before the UI presents them
as final.

---

## 17. Error Handling and UX Expectations

The mobile experience should provide clear, non-technical feedback for common failures.

Important cases include:
- invalid login credentials
- expired session
- permission denied
- QR/session invalid
- session already closed
- outside allowed location
- duplicate attendance
- submission failed
- network interruption
- backend unavailable

Students should not be left guessing whether an important action succeeded or failed.

---

## 18. Integration Testing Priorities

Mobile integration testing should verify:

- login and token refresh behavior
- protected endpoint access by role
- student-only module exposure
- event and announcement retrieval
- attendance submission success flow
- attendance rejection edge cases
- borrow request submission
- profile summary retrieval
- notification display behavior
- duplicate-submission protection
- network interruption handling

Testing should cover the full path:
Flutter app → JWT-secured API → Django backend → PostgreSQL database.

---

## 19. Future Enhancement Direction

The following may be added later but are not part of the current required mobile core flow:

- biometric identity verification
- liveness challenge workflow
- secure face-template-based attendance reinforcement
- direct online payment gateway integration
- richer push notification infrastructure
- more advanced offline sync strategies

These enhancements must remain separate from the current official mobile integration baseline.

---

## 20. Summary

The Campus Connect mobile application is the primary student-facing client of the platform.

It must remain aligned with the finalized system model:
- STUDENT-centered mobile access
- JWT-authenticated communication
- backend-driven role enforcement
- attendance through active session QR + geolocation + authenticated identity
- visibility into communication, services, records, and summaries
- no mandatory biometrics in the current core scope

The mobile layer must function as a secure extension of the centralized backend, even when the Flutter client is maintained in a separate repository from the backend and officer web frontend.