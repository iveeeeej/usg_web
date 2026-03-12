# Campus Connect
## University Student e-Governance and Services Platform

---

## 1. Project Overview

Campus Connect is a web and mobile-based e-governance and student services platform designed to centralize, organize, and digitize the core operational processes of the University Student Government (USG) of USTP-Oroquieta.

The system is intended to replace fragmented, manual, and paper-based workflows with a structured digital environment where officers and students can interact through a unified platform. It supports governance activities, communication, attendance monitoring, accountability tracking, service requests, official reporting, and consolidated student records.

Campus Connect is designed specifically for **one USG organization only**. It does **not** follow a multi-tenant architecture and is **not** intended to serve multiple independent organizations under separate system instances. All modules, records, workflows, and user access are contained within a single USG operational environment.

The platform follows a **web + mobile** model:
- the **web system** is primarily used by **OFFICERS** for management, monitoring, and administrative tasks
- the **mobile application** is primarily used by **STUDENTS** for participation, access to services, viewing records, and receiving updates

The backend follows an **API-first architecture** secured with **JWT authentication**, allowing both platforms to operate under one centralized backend and database.

---

## 2. Core Purpose

Campus Connect exists to improve the efficiency, transparency, and consistency of student governance operations by providing a single digital platform for communication, monitoring, service handling, and structured reporting.

The system is intended to solve common administrative issues such as:
- scattered announcements and communication channels
- manual attendance and delayed violation tracking
- disconnected service request processes
- difficulty monitoring student compliance and participation
- inefficient preparation of official USG reports
- limited visibility into records, summaries, and organizational performance

By consolidating these workflows into one platform, Campus Connect supports a more organized and accountable student governance process.

---

## 3. Core Objectives

Campus Connect is built to achieve the following objectives:

- Centralize USG communication, announcements, and student-facing updates
- Digitize attendance monitoring and accountability-related workflows
- Support structured and trackable service workflows for students
- Provide organized access to official USG reports and records
- Improve transparency through data logging, status tracking, and consolidated summaries
- Support officer decision-making through reports, monitoring tools, and analytics
- Deliver a secure and connected experience across the officer web platform and student mobile application

---

## 4. Platform Scope and Boundaries

Campus Connect operates under the following scope and system boundaries:

### 4.1 Single-Organization Scope
The system supports **one USG organization only**. It is not designed as a platform for multiple separate organizations, multiple institution-wide tenants, or parallel independent governance systems.

### 4.2 Internal Audience Targeting
Although the system is single-organization in scope, certain activities such as meetings, announcements, or events may be targeted to specific internal audiences or participant groups when needed. This does not change the overall single-organization model.

### 4.3 Current Core Scope
The current core scope of Campus Connect includes:
- governance and communication tools
- attendance and accountability workflows
- student service request features
- official records and structured reporting
- consolidated student summaries and monitoring

### 4.4 Excluded from Current Core Scope
The following are **not part of the current core scope** of the system:
- biometric identity verification as a required attendance mechanism
- full real-time online payment gateway automation as a required initial implementation feature
- multi-organization shared calendar architecture
- multi-tenant organization management

### 4.5 Future Enhancement Direction
Some advanced features may be explored in later development phases, but they are not part of the official present-scope definition of the system. These include biometric attendance reinforcement and direct third-party payment gateway integration.

---

## 5. User Roles and Access Model

Campus Connect uses only **two primary application roles**:

- `OFFICER`
- `STUDENT`

These are the only application-level roles recognized by the system.

### 5.1 OFFICER

OFFICER accounts are used by authorized USG officers who manage, operate, monitor, and maintain the system’s administrative workflows.

OFFICER responsibilities include:
- creating and managing events
- opening and closing attendance sessions
- monitoring attendance results and participation summaries
- reviewing violations and service-hour records
- approving or rejecting service-related requests
- publishing announcements and discussion-related updates
- managing official records and structured reports
- monitoring payment entries and request statuses
- viewing dashboards, summaries, and analytics

Each OFFICER account contains a `position` field representing the officer’s organizational designation.

Examples of positions may include:
- PRESIDENT
- VICE_PRESIDENT
- GENERAL_SECRETARY
- TREASURER
- AUDITOR
- PIO
- IT_REPRESENTATIVE
- BTLED_REPRESENTATIVE
- BFPT_REPRESENTATIVE

The `position` field is **informational only** and is used for organizational reference. It is **not** used as a separate authorization layer.

All OFFICER accounts have access to the same officer-level administrative modules under the current system design.

### 5.2 STUDENT

STUDENT accounts are used by regular students who interact with the system through the mobile application and student-facing platform features.

STUDENT activities include:
- viewing announcements and organizational updates
- viewing upcoming events and meeting-related information
- participating in attendance sessions
- submitting service-related requests
- viewing personal violations and service-hour obligations
- submitting event-related feedback
- viewing payment-related records
- accessing their profile summary and consolidated records

### 5.3 Access Model Rule

Authorization is based strictly on the application role assigned to the user:
- `role = OFFICER`
- `role = STUDENT`

There is no separate application-level super-admin role inside the business logic of Campus Connect.

---

## 6. Governance Model

Campus Connect supports a **single-organization governance model**.

There is no dedicated application-level **Super Admin** role within the functional design of the system. Administrative control inside the application is limited to the OFFICER role.

Django’s built-in `is_superuser` and other development or framework-level administrative privileges may still exist for backend maintenance, development, and deployment purposes, but those are **not part of the official application governance model**.

Application-level authority is enforced through:
- JWT-secured authentication
- role-based access control
- protected REST API endpoints
- separation of officer and student responsibilities

---

## 7. Core Functional Modules

The system includes the following major functional domains.

### 7.1 Governance and Communication

This domain supports the coordination, visibility, and communication functions of the USG.

It includes:
- **Dashboard** for officer monitoring and quick visibility of key system information
- **Events** for creating, scheduling, and managing organizational activities
- **General Assembly** for organizing formal student meetings and attendance-linked assembly sessions
- **Announcements** for publishing official updates and notices
- **Discussion Forum** for structured in-system communication and interaction
- **Notifications / System Alerts** for informing users about important updates, outcomes, and activity-related changes

This module group ensures that governance communication is centralized within the system rather than scattered across disconnected channels.

### 7.2 Attendance and Accountability

This domain supports student participation monitoring, compliance handling, and event-related accountability.

It includes:
- **Attendance** for recording participation during events or official sessions
- **Violation Tracking** for monitoring missed obligations and accountability outcomes
- **Service-Hour Monitoring** for tracking obligations associated with violations where applicable
- **Feedback Submission** for collecting student responses after events
- **Attendance and Event Summaries** for officer review and decision-making

Attendance in Campus Connect follows this high-level rule:

- the student must be authenticated in the mobile application
- the student must join an active attendance session
- attendance is validated through **session QR scanning**
- location is validated through **geolocation**
- the system enforces attendance timing rules such as open/close windows and cutoff logic
- duplicate or invalid sign-ins must be prevented by the system

This means the system uses:
- **authenticated account identity**
- **active event/session QR validation**
- **location verification**

The system does **not** define school-ID QR scanning as the final core attendance model.

### 7.3 Student Services

This domain supports student-facing operational and request-based services.

It includes:
- **Borrow Requests** for requesting organizational items or resources
- **Lost and Found** for managing lost-item and found-item related records
- **Payment Tracking** for monitoring required contributions and violation-related payments
- **Campus Tour** for guided access to campus-related location or orientation information

The student services layer is intended to reduce manual follow-up and provide clearer request visibility for both officers and students.

### 7.4 Official Records and Structured Reporting

This domain supports the preparation, organization, and maintenance of official USG records.

It includes:
- **Resolution Management**
- **Annual Work and Financial Plan (AWFP)**
- **President’s Report**
- **Financial Report**
- **Auditor’s Report**
- **Accomplishment Reports**
- other structured organizational records as defined by the USG workflow

These records are intended to follow a **structured-template approach**, not unrestricted free-form document editing. The system is meant to support formal consistency, guided content entry, and organized digital storage of governance outputs.

### 7.5 Student Profile and Consolidated Records

This domain provides students with a summary view of their relevant records and standing inside the system.

It includes a consolidated profile summary that may contain:
- basic account and profile information
- attendance-related summaries
- violation and service-hour summaries
- payment-related summaries
- request and transaction status summaries
- other relevant student-facing record overviews

This allows students to view their standing in one place instead of checking separate processes manually.

### 7.6 Reports, Monitoring, and Analytics

This domain supports officer-side review, monitoring, and organizational decision-making.

It includes:
- dashboard summaries
- attendance summaries
- event participation summaries
- violation monitoring
- payment monitoring
- service request tracking
- feedback results
- analytics that support officer assessment of engagement, compliance, and activity outcomes

The purpose of this domain is to improve visibility, accountability, and data-informed decision-making.

---

## 8. High-Level Workflow Principles

Campus Connect follows several high-level workflow rules:

### 8.1 Centralized Communication
Official communication should be distributed through system-managed announcements, discussion tools, and alerts to reduce fragmented communication practices.

### 8.2 Structured Attendance Flow
Attendance must be tied to authenticated student access, active attendance sessions, QR-based session validation, and location verification.

### 8.3 Accountability Tracking
Attendance results may affect student accountability workflows, including violation records or required service-hour monitoring where applicable.

### 8.4 Service Request Transparency
Student service-related actions such as borrow requests and other request-based workflows should have clear statuses and review paths.

### 8.5 Structured Official Documentation
Reports and official records should follow guided and structured formats to maintain consistency and reduce disorder in documentation.

### 8.6 Consolidated Student Visibility
Students should be able to view important personal records and summaries in one place rather than relying on separate manual follow-ups.

### 8.7 Officer Monitoring and Decision Support
Officer-facing modules should provide enough organized information for monitoring operations and supporting decisions through summaries and analytics.

---

## 9. Payment Implementation Direction

Campus Connect includes a payment-related module, but its implementation is defined in stages.

### 9.1 Current Direction
The system supports **digital payment tracking and recording** of:
- required student contributions
- violation-related payments
- payment-related status visibility

This means the system can store, monitor, and display payment records even if payment verification or entry is initially handled through tracked or manually confirmed workflows.

### 9.2 Later Enhancement Direction
Direct integration with a third-party payment gateway or online payment service may be added in a later phase. This is considered an enhancement rather than a required condition for the initial system scope.

This approach allows the platform to support payment visibility and accountability without making external gateway integration a blocker for the first complete version of the system.

---

## 10. Future Enhancements

The following features may be explored in future development phases but are **not part of the current core scope**:

- **Biometric identity verification** as an additional attendance-security layer
- **Direct third-party payment gateway integration**
- other advanced automation features that extend beyond the initial core implementation

Biometric verification, if implemented in the future, should be treated as an enhancement to strengthen attendance authenticity rather than as the foundation of the current attendance model.

Similarly, full payment gateway integration should be considered an advanced automation layer that builds on top of the initial payment tracking workflow.

---

## 11. Summary

Campus Connect is a centralized e-governance and student services platform for a single USG organization. It is designed to connect officer-side management and student-side participation through one secured system.

The platform focuses on governance communication, attendance and accountability, student services, structured records, reporting, and consolidated monitoring.

Its official application model uses only two roles — `OFFICER` and `STUDENT` — with officer position stored only for reference. Attendance is defined through authenticated access, session QR validation, and geolocation. Payment is supported through tracked digital records first, while advanced automation such as biometric verification and direct gateway integration remains part of future enhancement planning.