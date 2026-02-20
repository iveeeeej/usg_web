# Project Timeline & Execution Plan

This document defines the realistic development roadmap
from February to October completion,
with final defense preparation extending to December.

The strategy assumes:

- Development begins in February.
- Limited weekly availability during prelim and midterm periods.
- Proposal presentation in May (with wireframe + prototype required).
- Target: Full feature completion by October.
- Final defense: December.

---

# Development Philosophy

- Build foundational systems first.
- Implement attendance core before biometric enhancement.
- Treat biometric verification as a security layer — not the starting point.
- Integrate mobile features progressively, not all at once.
- Freeze features in October to allow stabilization before defense.

---

# Phase 0 – Foundation Setup
## (Mid-February – Early March)

Objective:
Establish backend infrastructure and authentication core.

Tasks:
- Setup Django project structure
- Configure PostgreSQL
- Enable required extensions (UUID, PostGIS, pgvector if used)
- Implement custom User model
- Add role field (ADMIN / STUDENT)
- Add is_verified and verified_at fields
- Implement JWT authentication
- Setup environment configuration
- Test login endpoint via Postman
- Initialize Flutter project
- Connect Flutter login to backend

Deliverable:
Working authentication system with mobile login integration.

---

# Phase 1 – Attendance Core System
## (March – April)

Objective:
Develop QR-based attendance with geolocation validation (no biometrics yet).

Backend Tasks:
- Implement Event model
- Implement AttendanceSession model
- Implement QR generation logic
- Implement session open/close logic
- Implement attendance recording endpoint
- Enforce:
  - Active session validation
  - Time cutoff enforcement
  - Duplicate attendance prevention
- Integrate PostGIS geofence validation

Mobile Tasks:
- Implement event listing screen
- Integrate QR scanner
- Capture GPS coordinates
- Send attendance payload to backend

Deliverable by end of April:
Fully working QR + Geolocation attendance system.

This alone is already strong enough for proposal demonstration.

---

# Phase 2 – Proposal Preparation
## (May)

Objective:
Prepare working prototype and documentation for proposal defense.

Tasks:
- Finalize UI wireframes (Figma or equivalent)
- Improve Admin dashboard UI
- Create event management interface
- Demonstrate attendance monitoring panel
- Mock verification page (UI only if biometric not fully ready)
- Prepare system architecture presentation
- Prepare ERD and documentation slides

Deliverable:
Clickable prototype + live backend demo (QR + Geolocation).

---

# Phase 3 – Service Modules
## (June)

Objective:
Implement student service workflows.

Tasks:
- Implement BorrowItem model
- Implement BorrowRequest workflow
- Enforce status transitions:
  PENDING → APPROVED → RETURNED / REJECTED
- Implement Lost & Found module
- Implement Payment tracking module
- Link payment to violations (if applicable)
- Create corresponding REST endpoints
- Integrate Flutter UI for service modules

Deliverable:
Fully functional non-biometric system.

---

# Phase 4 – Biometric Identity Verification
## (July)

Objective:
Secure attendance with backend-based face verification.

Backend Tasks:
- Create UserFaceProfile model
- Integrate face detection library
- Implement embedding generation (ML inference only)
- Implement account verification endpoint
- Store embeddings securely
- Implement embedding comparison service
- Add configurable similarity threshold
- Enforce is_verified before attendance

Mobile Tasks:
- Integrate camera capture
- Implement liveness challenge (blink / head movement)
- Securely transmit captured image
- Integrate verification UI flow

Deliverable:
Multi-layer attendance security:
JWT + Role + Geolocation + Face Verification + Liveness.

---

# Phase 5 – Stabilization & Reports
## (August)

Objective:
Strengthen reporting and stabilize biometric system.

Tasks:
- Tune similarity threshold
- Test false positives / false negatives
- Handle edge cases (lighting, GPS errors)
- Implement structured report templates
- Enforce restricted editable fields
- Implement dynamic tables
- Add report submission validation
- Implement audit logging

Deliverable:
Governance-compliant reporting + stable biometric module.

---

# Phase 6 – Analytics & Optimization
## (September)

Objective:
Implement decision-support analytics and optimize performance.

Tasks:
- Attendance percentage calculations
- Violation summaries
- Payment summaries
- Admin dashboard metrics
- Optimize database indexing
- Optimize image processing pipeline
- Conduct integration testing across modules

Deliverable:
Complete analytics layer + performance improvements.

---

# Phase 7 – Feature Freeze & Finalization
## (October)

Objective:
Complete development and lock feature set.

Tasks:
- Full system testing (mobile + backend)
- Biometric stress testing
- Multi-device compatibility testing
- Security audit
- Logging improvements
- Resolve critical bugs
- Finalize documentation

Deliverable:
Fully functional system with all planned features implemented.

Feature development ends here.

---

# Phase 8 – Defense Preparation
## (November – December)

Objective:
Polish, document, and prepare for final defense.

Tasks:
- Prepare system demonstration script
- Prepare technical explanation slides
- Prepare biometric defense arguments
- Conduct mock Q&A sessions
- Refine documentation
- Backup and deployment rehearsal

Deliverable:
Defense-ready project with stable production build.

---

# Risk Management Strategy

Major Risks:
- Biometric library integration complexity
- Embedding threshold tuning
- Geolocation inaccuracies
- Mobile camera inconsistencies

Mitigation:
- Prototype embedding extraction early (March test)
- Avoid feature creep
- Freeze architecture changes early
- Allocate buffer time (September–October)

---

# Feasibility Conclusion

With controlled weekly progress:

- Proposal in May: Achievable
- Full feature completion by October: Realistic
- Defense in December: Comfortable

This timeline provides buffer months before final defense,
reducing risk and allowing refinement.

The key milestone to protect is:
Completion of QR + Geolocation by April.

Biometric phase must not begin without a stable attendance core.