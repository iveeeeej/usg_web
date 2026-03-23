# Development Phases

The development roadmap follows a layered implementation strategy.
Each phase builds on the previous one to maintain architectural stability,
clear scope control, and gradual feature expansion.

This roadmap aligns with the current Campus Connect direction:

- single USG organization only
- two application roles only: OFFICER and STUDENT
- role-based access using JWT-secured APIs
- attendance based on authenticated student access, active session QR, and geolocation
- payment tracking implemented first before direct online gateway automation
- biometrics treated as a future enhancement, not part of the current core scope

Legend:
    √ - Complete
    ~ - Incomplete / Partially Complete
    x - Not Complete

---

## Phase 1 – Foundation & Core Infrastructure

Objective:
Establish the backend architecture, identity model, authentication flow,
and core development environment required for all later modules.

Status:
√ Mostly Complete

Completed / Established:
√ Setup Django project structure
    • Django project initialized
    • config/ created
    • accounts/ app created
    • server runs successfully

√ Configure PostgreSQL database
    • PostgreSQL is now the active primary database
    • environment-based DATABASES configuration is implemented
    • local PostgreSQL connection has been verified

√ Implement custom User model
    • AUTH_USER_MODEL configured
    • student_id used as login identifier
    • role field added
    • position field included for OFFICER reference

√ Implement role system (OFFICER / STUDENT)
    • application authority is role-based
    • OFFICER-only endpoint protection exists
    • STUDENT is separated from officer-only logic

√ Implement JWT authentication
    • SimpleJWT installed and configured
    • /api/token/ working
    • /api/token/refresh/ available
    • Bearer token authentication validated

√ Configure Django admin panel
    • /admin/ accessible
    • custom User registered
    • admin access working for backend maintenance

√ Setup environment configuration (dev / production)
    • settings package structure created
    • base.py / dev.py / prod.py in place
    • .env loading implemented

√ Establish base API structure
    • API-first architecture established
    • initial protected endpoint exists
    • role-based permission foundation is in place

√ Implement basic logging configuration
    • console logging enabled for development
    • rotating file logging configured
    • backend/logs/django.log in use

Remaining refinement:
~ Minor Django admin polish if needed
    • list_display already implemented
    • list filters already implemented
    • search fields already implemented
    • cleaner admin forms remain optional refinement only

~ Harden environment handling
    • validate production-only settings
    • verify deployment-ready secret handling
    • confirm CORS policy for non-dev environments

Deliverable:
A stable backend foundation with PostgreSQL, JWT authentication, role-based access,
environment-based settings, and reusable API structure.

---

## Phase 2 – Governance and Communication Core

Objective:
Build the foundational governance and communication modules used by the
single USG organization for visibility, coordination, and centralized updates.

Status:
~ Partially Complete

Scope:
- Officer dashboard foundation
- Events module
- USG calendar / event scheduling view
- General Assembly management
- Announcements module
- Discussion Forum foundation
- Notification / system alert foundation

Tasks:
~ Implement Dashboard module
    • summary cards now render live counts for announcements and events
    • the "What's New" card is now backed by a shared database record and editable through the web dashboard
    • deeper analytics and broader dashboard modules are still pending

√ Implement Events module
    • create, update, publish, archive events
    • store date, time, venue, description
    • attachment metadata endpoints added for event-related files

~ Implement calendar-oriented event scheduling
    • API-level event schedule listing is available
    • meeting / assembly visibility is supported through filtering and event_type
    • dedicated calendar-specific presentation layer is still pending

√ Implement General Assembly module
    • implemented through `Event.event_type = GENERAL_ASSEMBLY`
    • title, date, time, venue, description, and audience targeting are supported
    • shared event workflow is now reusable for assembly records

√ Implement Announcements module
    • officers create and manage official announcements
    • students can view published announcements
    • announcement visibility and status are managed centrally through the API

    â€¢ announcement type classification is now stored separately from publish status

x Implement Discussion Forum foundation
    • discussion threads
    • comments / replies
    • post ownership and moderation rules
    • centralized in-system communication flow

x Implement notification / alert foundation
    • announcement-related notifications
    • event-related reminders or updates
    • request status notifications where applicable

~ Develop corresponding REST API endpoints
    • `/api/events/`, `/api/events/{id}/`, and `/api/events/{id}/attachments/` added
    • `/api/announcements/` and `/api/announcements/{id}/` added
    • `/api/officer/dashboard/` now returns officer summary, dashboard message, stats, and recent announcements
    • `/api/dashboard-message/` now supports authenticated reads and OFFICER-only updates
    • Phase 2 APIs for discussions and notifications are still pending
~ Connect officer web interfaces
    • login flow is connected to `/api/token/`
    • dashboard cards and recent announcement panel now render live data from `/api/officer/dashboard/`
    • the "What's New" card can now edit the shared dashboard message through `/api/dashboard-message/`
    • fuller API integration for events, announcements, assemblies, and discussions is still pending

~ Define backend support for basic mobile read/view integration for student-facing communication features
    • events and announcements APIs are available for student-facing clients
    • `/api/dashboard-message/` provides shared authenticated "What's New" content reusable by future mobile dashboard views
    • the student mobile application may be implemented in a separate project
    • client-side mobile implementation status is tracked outside this repository

Progress update (2026-03-13):
~ `events` app created in the backend
~ `Event` and `EventAttachment` models implemented
~ `/api/events/`, `/api/events/{id}/`, and `/api/events/{id}/attachments/` added
~ authenticated read access and OFFICER-only write access implemented for events
~ General Assembly support started through `event_type = GENERAL_ASSEMBLY`
~ event filtering added for `status`, `event_type`, `audience_scope`, and `upcoming`
~ `announcements` app created in the backend
~ `Announcement` model implemented
~ `/api/announcements/` and `/api/announcements/{id}/` added
~ OFFICER-only announcement writes and published-only student reads implemented

Progress update (2026-03-14):
~ `DashboardMessage` model and migration added in `accounts`
~ `/api/dashboard-message/` added with authenticated reads and OFFICER-only updates
~ `/api/officer/dashboard/` expanded with shared dashboard message data and live summary payloads
~ officer dashboard now renders live counts, recent announcements, and an editable backend-backed "What's New" card

Progress update (2026-03-18):
~ `Announcement` now stores `announcement_type` separately from workflow status
~ officer announcement creation now defaults to `PUBLISHED` when status is omitted
~ officer announcement web form now captures `type` instead of exposing raw status selection

Progress update (2026-03-19):
~ officer announcement cards in the web interface now expose edit and delete actions
~ officer announcement modal now supports both create and edit flows against `/api/announcements/{id}/`
~ announcement API coverage now includes update and delete tests for officer users

Progress update (2026-03-20):
~ `frontend/assets/js/app-config.js` added as a shared frontend API base
  URL config source
~ `frontend/index.html`, `frontend/org_usg/usg_dashboard.html`, and
  `frontend/org_usg/usg_announcement.html` now consume the shared
  frontend API config instead of hardcoding `127.0.0.1:8000`
~ `frontend/assets/js/api-client.js` added so current API pages can share
  request helpers, auth headers, token storage, and auth-failure logout
  behavior
~ `frontend/org_usg/usg_announcement.html` cleaned up duplicate
  announcement CSS and now keeps static subtitle copy in HTML instead of
  rewriting it through JavaScript on page load
~ officer announcement card actions now clone from an HTML template, and
  announcement action lookup now normalizes ID types so edit/delete
  buttons stay reliable when API IDs are numeric

Progress update (2026-03-22):
~ officer announcement feedback now supports timed auto-dismiss for
  success and info messages while keeping error messages persistent
~ create, edit, and delete success confirmations on the officer
  announcement page now auto-hide after a short delay

Deliverable:
A working governance and communication layer that centralizes updates,
events, assemblies, and in-system discussion inside one USG platform.

---

## Phase 3 – Attendance and Accountability Core

Objective:
Implement the official attendance workflow and related accountability features
without biometrics.

Status:
x Not Complete

Current implementation note:
x Attendance and geolocation modules are not yet implemented in this repository
~ PostGIS remains part of the planned Phase 3 attendance stack


Scope:
- AttendanceSession model
- AttendanceRecord model
- Session QR attendance flow
- Geolocation validation
- Time cutoff rules
- Duplicate prevention
- Violation automation
- Feedback submission
- Event participation summaries

Tasks:
x Implement AttendanceSession model
    • session status
    • open / close timing
    • sign-in configuration
    • attendance cutoff configuration

x Implement AttendanceRecord workflow
    • one attendance record per student per session
    • attendance timestamps
    • attendance status validation

x Implement QR session generation
    • QR identifies the active session or attendance instance
    • QR is not based on school-ID QR as the final core flow

x Implement geolocation validation using PostGIS
    • validate whether student is within allowed location boundary
    • reject attendance outside the approved area

x Implement time cutoff enforcement
    • sign-in window rules
    • configurable late or missed attendance handling

x Implement duplicate attendance prevention
    • prevent repeated sign-ins in the same session
    • validate one-record-per-session logic

x Implement violation auto-assignment logic
    • generate violation or accountability records for missed obligations
    • support service-hour related consequences where applicable

x Implement event feedback module
    • allow students to submit feedback after event completion
    • store ratings and comments when required

x Implement attendance and participation summaries
    • officer-side session summaries
    • count present / absent / late outcomes
    • event-level participation visibility

x Develop corresponding REST API endpoints
x Integrate Flutter event listing
x Integrate mobile QR scanning capability
x Integrate mobile geolocation capture
x Integrate student attendance history view

Deliverable:
A fully functional attendance and accountability system based on
JWT-authenticated student access, active session QR validation,
geolocation checks, cutoff rules, and accountability tracking.

---

## Phase 4 – Student Services Core

Objective:
Build the non-attendance student service workflows and student summary visibility.

Status:
x Not Complete

Scope:
- Borrow
- Lost & Found
- Payment tracking
- Campus Tour
- Profile summary

Tasks:
x Implement Borrow item management
    • create and manage available items
    • define borrowable inventory information

x Implement Borrow request workflow
    • submit request
    • review request
    • approve / reject request
    • track return status
    • enforce valid status transitions:
      PENDING → APPROVED → RETURNED / REJECTED

x Implement Lost & Found module
    • create lost / found records
    • item description
    • image support if applicable
    • location found
    • claim status tracking

x Implement Payment tracking module
    • record required contributions
    • record violation-related payment entries
    • link payment records to student profile
    • support payment status monitoring

x Implement manual / tracked payment confirmation flow
    • allow tracked recording first
    • support administrative confirmation workflow
    • avoid making gateway integration a blocker for current core scope

x Implement Campus Tour module
    • create campus location records
    • display building / office / facility information
    • support simple interactive location viewing

x Implement Profile Summary module
    • attendance summary
    • violations / service-hour summary
    • payment summary
    • borrow / request summary
    • overall account status summary

x Develop corresponding REST API endpoints
x Integrate Flutter service interfaces
x Integrate student profile summary screens

Deliverable:
A complete student services layer with request workflows, payment tracking,
campus location access, and consolidated student record visibility.

---

## Phase 5 – Legislative Records and Structured Reporting

Objective:
Implement the governance records and structured report system for OFFICER users.

Status:
x Not Complete

Scope:
- Resolution management
- AWFP
- President’s Report
- Financial Report
- Auditor’s Report
- Accomplishment Report
- structured reporting rules

Tasks:
x Implement Resolution module
    • create and manage resolution records
    • organize official legislative outputs
    • store status and filing metadata where needed

x Implement structured report categories
    • Annual Work and Financial Plan (AWFP)
    • President’s Report
    • Financial Report
    • Auditor’s Report
    • Accomplishment Report

x Implement structured report templates
    • predefined format per report type
    • guided data entry
    • controlled sections only

x Implement restricted editing rules
    • preserve template structure
    • allow edits only in approved input regions
    • prevent arbitrary layout modification

x Implement dynamic table sections
    • row-based data entry where needed
    • repeatable structured sections

x Implement file attachment support if required
x Implement report submission validation
x Implement report locking after submission if required
x Implement report version tracking if revisions are allowed
x Implement audit logging for report creation and updates
x Develop report-related REST API endpoints

Deliverable:
A governance-compliant records and reporting module using structured templates
instead of unrestricted document editing.

---

## Phase 6 – Analytics, Monitoring, and Decision Support

Objective:
Provide organized summaries and decision-support metrics for officers.

Status:
x Not Complete

Scope:
- Dashboard analytics
- Attendance analytics
- Violation summaries
- Payment summaries
- service workflow monitoring
- historical comparison support

Tasks:
x Implement attendance percentage calculations
x Implement event participation analytics
x Implement violation accumulation summaries
x Implement service-hour monitoring summaries
x Implement payment summaries and balance visibility
x Implement service request monitoring views
x Implement feedback result summaries
x Implement historical comparison reporting where applicable
x Optimize aggregation queries for dashboard use
x Integrate analytics into officer dashboard and report support views

Deliverable:
A data-informed governance dashboard and reporting support layer that improves
visibility, review, and decision-making.

---

## Phase 7 – Mobile Application Integration and Stabilization

Objective:
Refine and align mobile behavior with the finalized backend scope and student workflows.

Status:
x Not Complete

Scope:
- authentication flow
- attendance flow
- service interfaces
- profile views
- reliability and error handling

Tasks:
x Finalize Flutter authentication flow
    • login
    • token storage
    • refresh flow
    • logout handling

x Finalize mobile event and announcement views
x Finalize General Assembly visibility on mobile if required
x Finalize student attendance participation flow
    • session QR scan
    • geolocation capture
    • attendance success / failure feedback
    • retry-safe UX

x Finalize mobile service screens
    • borrow
    • lost & found
    • payment records
    • campus tour
    • profile summary

x Implement secure error handling and retry logic
x Validate edge cases
    • network interruption
    • expired token
    • GPS inaccuracy
    • session closed
    • duplicate sign-in attempt

x Conduct end-to-end integration testing across web, mobile, API, and database layers

Deliverable:
A fully synchronized mobile + backend ecosystem aligned with the current
Campus Connect scope.

---

## Phase 8 – Hardening, Quality Assurance, and Deployment

Objective:
Prepare the system for production-level stability, maintainability, and controlled deployment.

Status:
x Not Complete

Tasks:
x Conduct security audit of authentication, authorization, and protected endpoints
x Review input validation across all modules
x Perform basic penetration testing
x Optimize database indexing and query performance
x Conduct performance testing for concurrent attendance scans
x Validate logging coverage for critical actions
x Implement monitoring and production logging strategy
x Finalize environment-specific configuration
x Prepare production database and backend deployment
x Conduct final cross-module integration testing
x Prepare deployment checklist and rollback plan

Deliverable:
A production-ready system with validated security, reliable performance,
and deployment readiness.

---

## Phase 9 – Future Enhancements

Objective:
Document advanced features that may be added after the current core scope is stable.

Status:
x Not Complete / Future Scope

Possible Enhancements:
x Biometric identity verification for attendance reinforcement
    • face verification
    • liveness challenge
    • secure biometric template handling
    • optional extra attendance-security layer

x Direct third-party payment gateway integration
    • online payment callback handling
    • automatic transaction verification
    • secure reference validation

x Additional automation features
    • advanced workflow notifications
    • deeper analytics visualizations
    • extended report automation
    • more advanced student-engagement features

Deliverable:
A clearly separated enhancement track that extends the system without
distorting the current core implementation scope.

---

## Roadmap Summary

Phase ordering is intentionally structured as:

1. Foundation first
2. Governance and communication core
3. Attendance and accountability core
4. Student service workflows
5. Legislative records and structured reporting
6. Analytics and decision support
7. Mobile integration and stabilization
8. Hardening and deployment
9. Future enhancements

This ordering ensures that Campus Connect is built first as a complete
single-organization governance and service platform before advanced
enhancement features are considered.
