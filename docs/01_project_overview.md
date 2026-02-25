# Campus Connect
## University of Student e-Governance and Services

---

## 1. Project Description

Campus Connect is a web and mobile-based e-governance platform designed to centralize and automate administrative, communication, and service processes of the University Student Government (USG) of USTP-Oroquieta.

The system replaces fragmented and manual processes with a structured digital workflow system.

This system is designed specifically for ONE USG organization and is not multi-tenant.

The backend follows an API-first architecture secured with JWT authentication.

---

## 2. Core Objectives

- Centralize communication and announcements
- Automate attendance and violation tracking
- Provide structured reporting templates
- Enable digital service workflows (borrow, payment, lost & found)
- Improve accountability through data logging
- Provide analytics for decision-making
- Integrate secure web (OFFICER) + mobile (STUDENT) interfaces

---

## 3. User Roles

The system has ONLY TWO primary roles:

### 1. OFFICER

USG Officers who manage and operate the system.

Capabilities:
- Create and manage events
- Open and close attendance sessions
- Monitor violations
- Approve borrow requests
- Publish announcements
- Manage structured reports
- Monitor payments
- View analytics

Each OFFICER has a `position` field (organizational designation).

Examples:
- PRESIDENT
- VICE_PRESIDENT
- GENERAL_SECRETARY
- TREASURER
- AUDITOR
- PIO
- IT_REPRESENTATIVE
- BTLED_REPRESENTATIVE
- BFPT_REPRESENTATIVE

Position is informational only.

All OFFICER accounts have full access to all administrative modules regardless of position.

---

### 2. STUDENT

Regular students who interact with the system.

Capabilities:
- View events and announcements
- Scan QR for attendance
- Submit borrow requests
- View violations and service hours
- Submit feedback
- View payment records
- View profile summary

---

## 4. Governance Model

This system supports a single-organization governance model.

There is no system-level Super Admin.

Django `is_superuser` exists only for development and backend administration.

Application-level authority is strictly controlled by:

- role = OFFICER
- role = STUDENT

Authorization is enforced via JWT-secured REST endpoints.