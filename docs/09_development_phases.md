# Development Phases

The development roadmap follows a layered implementation strategy.
Each phase builds on the previous one, ensuring architectural stability,
security enforcement, and controlled feature expansion.

---

## Phase 1 – Foundation & Core Infrastructure

Objective:
Establish the backend architecture and identity system.

- Setup Django project structure
- Configure PostgreSQL database
- Enable required extensions (UUID, PostGIS, pgvector if used)
- Implement custom User model
- Implement role system (ADMIN / STUDENT)
- Implement JWT authentication
- Configure Django admin panel
- Setup environment configuration (dev / production)
- Establish base API structure
- Implement basic logging configuration

Deliverable:
Working authentication system with database connectivity.

---

## Phase 2 – Governance Core (Attendance Foundation)

Objective:
Build the core event and attendance system without biometrics.

- Implement Events module
- Implement AttendanceSession model
- Implement QR session generation
- Implement geolocation validation using PostGIS
- Implement time cutoff enforcement
- Implement duplicate attendance prevention
- Implement violation auto-assignment logic
- Implement Feedback system
- Develop corresponding REST API endpoints
- Integrate Flutter event listing
- Integrate QR scanning capability in mobile app
- Integrate geolocation capture from mobile

Deliverable:
Fully functional attendance system (QR + Geolocation).

---

## Phase 3 – Biometric Identity Verification Layer

Objective:
Secure attendance with backend-based face verification.

- Create UserFaceProfile model
- Add is_verified and verified_at fields to User
- Implement account verification endpoint
- Integrate backend face detection library
- Implement face embedding generation (ML inference only)
- Implement randomized liveness challenge flow
- Implement server-side embedding comparison
- Implement configurable similarity threshold
- Enforce is_verified requirement before attendance
- Integrate Flutter camera capture for verification
- Securely transmit captured image to backend
- Integrate biometric validation into attendance workflow

Deliverable:
Multi-layer attendance security:
JWT + Role + Geolocation + Biometric + Liveness.

---

## Phase 4 – Service Workflows

Objective:
Implement non-attendance service modules.

- Borrow item management
- Borrow request workflow (PENDING → APPROVED → RETURNED/REJECTED)
- Lost & Found module
- Payment tracking (manual recording first)
- Payment status transitions
- Implement corresponding REST endpoints
- Integrate Flutter service interfaces

Deliverable:
Complete student service functionality.

---

## Phase 5 – Reports & Structured Templates

Objective:
Implement controlled reporting system for ADMIN users.

- Structured report forms (AWFP, President, Financial, etc.)
- Enforced report format templates
- Restricted editable fields
- Dynamic tables (auto-generated sections)
- File attachment support (if required)
- Report submission validation
- Report locking after submission (if required)
- Report version tracking (if revisions allowed)
- Audit logging for report creation and updates
- Implement report-related API endpoints

Deliverable:
Governance-compliant reporting module.

---

## Phase 6 – Analytics & Data Insights

Objective:
Provide decision-support metrics.

- Attendance percentage calculations
- Violation accumulation summaries
- Payment summaries
- Historical comparison reports
- Aggregation query optimization
- Admin dashboard analytics integration

Deliverable:
Data-driven governance dashboard.

---

## Phase 7 – Mobile Application Stabilization

Objective:
Refine and align mobile features with backend security model.

- Finalize Flutter authentication flow
- Finalize account verification UI/UX
- Finalize biometric attendance capture flow
- Implement secure error handling and retry logic
- Optimize image upload size and compression
- Validate edge cases (network drop, failed match, GPS inaccuracy)
- Conduct integration testing across all modules

Deliverable:
Fully synchronized mobile + backend ecosystem.

---

## Phase 8 – Hardening, Security Audit & Deployment

Objective:
Prepare system for production-level stability.

- Conduct security audit
- Validate biometric threshold tuning
- Perform penetration testing (basic level)
- Optimize database indexing
- Performance testing for concurrent attendance scans
- Implement structured logging and monitoring
- Configure production environment
- Deploy backend and database
- Final integration testing

Deliverable:
Production-ready system.