# System Architecture

---

## 1. Architecture Overview

Campus Connect follows a layered, API-first system architecture designed for a
single-organization e-governance and student services platform.

The architecture is built to support the operational needs of the University Student
Government (USG) of USTP-Oroquieta through one centralized backend that serves both
the officer web platform and the student mobile application.

The architecture follows these core system rules:

- one USG organization only
- no multi-tenant organization model
- two application roles only: `OFFICER` and `STUDENT`
- JWT-secured API communication
- centralized backend enforcement of business rules
- attendance based on authenticated student identity, active session QR validation, and geolocation
- tracked payment recording in the current scope
- biometrics excluded from the current core architectural baseline

The architecture is intended to centralize governance, communication, attendance,
accountability, student services, official records, and monitoring workflows
inside one integrated platform.

---

## 2. Layered Architecture Model

Campus Connect is organized into three main architectural layers:

### 2.1 Client Layer

The client layer contains the interfaces used by the two main user groups.

It consists of:

- **Web Officer Interface**
  - primarily used by OFFICER accounts
  - supports management, monitoring, and administrative workflows
  - implemented through frontend pages and JavaScript that consume backend APIs

- **Mobile Student Application**
  - primarily used by STUDENT accounts
  - supports participation, attendance, service requests, record viewing, and notifications
  - implemented as a mobile client that communicates with the backend through JWT-secured API calls

### 2.2 Application Layer

The application layer contains the backend logic and API services.

It consists of:

- **Django Backend**
- **Django REST Framework**
- **JWT Authentication (SimpleJWT)**
- service-layer business logic
- permission and workflow validation logic
- request handling for both web and mobile clients

This is the main enforcement boundary of the system.

### 2.3 Data Layer

The data layer contains the centralized persistent storage and geolocation-aware validation support.

It consists of:

- **PostgreSQL**
- **PostGIS**

This layer supports transactional data, structured records, attendance geolocation
validation, and analytics-oriented querying.

---

## 3. Architectural Pattern

Campus Connect follows a combination of the following design patterns:

- layered architecture
- API-first architecture
- modular backend application structure
- JWT-based stateless authentication
- role-based access control
- service-layer business logic separation
- centralized data and validation model

### 3.1 Django Internal Pattern

Inside the backend, Django follows its internal project/app structure.

However, the system’s external behavior is API-driven rather than page-rendering-driven.

This means the architecture should be understood as:

- Django backend for application logic and API services
- REST API consumed by both web and mobile clients
- database-backed workflows enforced server-side

### 3.2 API-Driven Client Integration

The officer web platform does **not** function as a traditional server-rendered
Django template dashboard as its primary architectural behavior.

Instead:
- the frontend sends authenticated API requests
- the backend enforces business rules
- responses are returned as structured API data

The mobile application follows the same principle:
- it consumes JWT-protected REST endpoints
- it depends on the backend as the source of truth
- it does not operate as an independent system

---

## 4. System Scope at the Architectural Level

The architecture must support the full current core scope of Campus Connect.

This includes the following functional domains:

### 4.1 Governance and Communication
- Dashboard
- Events
- General Assembly
- Announcements
- Discussion Forum
- Notifications / System Alerts

### 4.2 Attendance and Accountability
- Attendance Sessions
- Attendance Records
- Violation Tracking
- Service-Hour Monitoring
- Feedback Submission
- Attendance and Event Summaries

### 4.3 Student Services
- Borrow Requests
- Lost and Found
- Payment Tracking
- Campus Tour / Campus Location Information

### 4.4 Official Records and Structured Reporting
- Resolution Management
- Annual Work and Financial Plan (AWFP)
- President’s Report
- Financial Report
- Auditor’s Report
- Accomplishment Report

### 4.5 Student Profile and Consolidated Monitoring
- student profile summary
- attendance-related summaries
- violation and service-hour summaries
- payment summaries
- request and status summaries

### 4.6 Officer Monitoring and Analytics
- dashboard summaries
- event participation summaries
- attendance monitoring
- payment monitoring
- service request monitoring
- feedback and engagement summaries
- analytics for decision support

The architecture must support all of these domains as parts of one integrated system.

---

## 5. Authorization Model

Campus Connect has only two application-level roles:

- `OFFICER`
- `STUDENT`

There is no application-level Super Admin role inside the business architecture.

### 5.1 OFFICER

OFFICER accounts have access to officer-side administrative workflows such as:
- events
- attendance session control
- violations
- borrow review workflows
- announcements
- structured reporting
- payment monitoring
- dashboard and analytics functions

### 5.2 STUDENT

STUDENT accounts have access to student-facing workflows such as:
- viewing announcements and events
- participating in attendance sessions
- viewing violations and service-hour obligations
- submitting feedback
- submitting service-related requests
- viewing payment records
- viewing profile summaries and notifications

### 5.3 Position Rule

The `position` field for OFFICER is informational only.

Architecturally, this means:
- `position` is stored as organizational metadata
- `position` does not create a separate permission tier
- all OFFICER accounts share the same current application-level authority model

### 5.4 Authorization Enforcement

Authorization is enforced through:
- JWT authentication
- server-side role validation
- permission classes
- resource ownership checks
- workflow-specific validation

---

## 6. High-Level Request Flow

Campus Connect uses a centralized request flow for both web and mobile clients.

### 6.1 Officer Web Flow

Officer Web Interface
        ↓
JavaScript / frontend request
        ↓
JWT-authenticated API call
        ↓
Django REST API
        ↓
Permission / validation / workflow logic
        ↓
Django ORM
        ↓
PostgreSQL / PostGIS

### 6.2 Student Mobile Flow

Flutter Mobile Application
        ↓
JWT-authenticated API call
        ↓
Django REST API
        ↓
Permission / validation / workflow logic
        ↓
Django ORM
        ↓
PostgreSQL / PostGIS

### 6.3 Architectural Meaning

In both flows:
- the client is only the interface layer
- the backend is the business and security enforcement layer
- the database is the source of persistent records
- business rules must never rely only on client behavior

---

## 7. Attendance Architecture Rule

Attendance is one of the most sensitive workflows in the system and must follow the finalized architectural rule.

### 7.1 Attendance Identity Model

Attendance identity comes from:
- authenticated backend user
- active attendance session
- session QR validation
- geolocation validation

The final architecture does **not** treat school-ID QR as the primary current attendance model.

### 7.2 Attendance Validation Layers

The architecture must support server-side validation for:
- active authenticated student
- valid attendance session
- valid QR/session payload
- allowed time window and cutoff
- allowed geographic range
- duplicate attendance prevention

### 7.3 Geolocation Support

Because attendance depends on location validation, the architecture includes PostGIS in the data layer.

This allows the backend to validate:
- center-radius attendance zones
- polygon-based attendance zones when needed
- geospatial comparison between student-submitted coordinates and allowed attendance boundaries

### 7.4 Current-Scope Exclusion

The current core attendance architecture does **not** require:
- biometric verification
- face embedding comparison
- liveness challenge
- mandatory image-based attendance validation

Those belong only to future enhancement scope.

---

## 8. Payment Architecture Rule

The architecture supports payment handling in staged form.

### 8.1 Current Scope

The current architecture supports:
- digital payment tracking
- payment status visibility
- contribution recording
- violation-related payment recording
- officer-side confirmation workflows where needed

This means the architecture supports payment records even if direct payment gateway automation is not yet implemented.

### 8.2 Future Enhancement

Direct third-party payment gateway integration may be added later.

That enhancement would introduce:
- gateway transaction handling
- callback verification
- reconciliation logic

But it is not part of the current required baseline architecture.

---

## 9. Modular Backend Architecture

The backend is designed to grow through a modular Django app structure.

The modular architecture should align with the finalized product scope.

Recommended backend application modules include:

- `accounts`
- `events`
- `announcements`
- `discussions`
- `notifications`
- `attendance`
- `violations`
- `borrow`
- `payments`
- `reports`
- `resolutions`
- `lost_found`
- `campus`
- `analytics`

### 9.1 Why Modularization Matters

A modular backend structure helps:
- isolate domain responsibilities
- reduce coupling
- improve maintainability
- support incremental feature implementation
- keep API logic organized by functional area

### 9.2 Actual vs Intended Structure

The architecture document describes the intended modular backend direction.

It does not require that every module already exists physically in the current repository.

This distinction is important because architectural design describes the target structure,
while the actual repository may still be in an earlier implementation phase.

---

## 10. Module Responsibility Boundaries

Each architectural module should have a clear domain boundary.

### 10.1 `accounts`
- user identity
- custom User model
- role and position metadata
- account-related permissions

### 10.2 `events`
- events
- general assembly scheduling behavior
- event attachments
- schedule visibility

### 10.3 `announcements`
- official announcements
- publication state
- student-facing visibility

### 10.4 `discussions`
- discussion threads
- comments and replies
- discussion participation
- moderation-related rules

### 10.5 `notifications`
- system alerts
- user notification state
- read/unread tracking

### 10.6 `attendance`
- attendance sessions
- attendance records
- QR session validation
- geolocation validation
- timing and cutoff enforcement
- duplicate-prevention logic

### 10.7 `violations`
- missed-attendance accountability
- service-hour tracking
- violation monitoring

### 10.8 `borrow`
- item inventory for borrowing
- request submission
- approval/rejection workflow
- return tracking

### 10.9 `payments`
- payment records
- contribution records
- violation-related payments
- confirmation tracking

### 10.10 `reports`
- structured reports
- report templates
- report attachments
- submission and locking rules

### 10.11 `resolutions`
- resolution records
- legislative tracking
- filing/status metadata

### 10.12 `lost_found`
- lost and found records
- item descriptions and images
- claim status tracking

### 10.13 `campus`
- campus locations
- campus tour information
- facility/location metadata

### 10.14 `analytics`
- summaries
- dashboard metrics
- monitoring aggregates
- historical and decision-support views

---

## 11. Backend as Source of Truth

The architecture requires the backend to remain the source of truth for:

- user identity
- role
- attendance validity
- payment status
- workflow state
- ownership of records
- notification state
- reporting status
- analytics inputs

This means:
- the frontend must not enforce core business rules by itself
- the mobile app must not treat submitted identifiers as stronger than authenticated identity
- important transactional workflows must always be validated server-side

---

## 12. Data Architecture Principles

The architecture assumes a centralized relational data model with geospatial support.

At the system-architecture level, this means:
- major records are stored centrally in PostgreSQL
- geolocation-aware attendance validation uses PostGIS
- dashboard and summary views are derived from transactional records
- structured records and reports remain historically traceable
- future-enhancement features should not distort the current core schema

The data architecture is designed to support:
- integrity
- auditability
- reporting consistency
- analytics-ready querying

---

## 13. Non-Goals in the Current Core Architecture

The following are not part of the current official core architecture:

- multi-tenant organization management
- shared multi-organization calendar architecture
- biometric-first attendance architecture
- mandatory liveness validation
- direct real-time payment gateway automation as a required initial architecture layer

These may be added only if the system officially enters a later enhancement phase.

---

## 14. Future Enhancement Direction

The architecture may expand later to support:
- biometric attendance reinforcement
- payment gateway callback integration
- richer notification delivery mechanisms
- deeper analytics services
- additional automation workflows

These should be treated as architectural extensions, not as part of the present baseline.

---

## 15. Summary

Campus Connect follows a layered, API-first, single-organization architecture.

It is designed to connect:
- an officer-oriented web platform
- a student-oriented mobile application
- a centralized Django REST backend
- a PostgreSQL/PostGIS data layer

The architecture is built around:
- two-role access control
- server-side validation
- modular domain separation
- QR session + geolocation attendance
- structured reporting
- student services
- centralized governance communication
- dashboard and analytics support

This architecture is intended to support the full current official scope of Campus Connect
without reintroducing older assumptions that have already been removed from the project baseline.