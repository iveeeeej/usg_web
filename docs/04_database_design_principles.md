# Database Design Principles

## 1. Design Philosophy

- Strong relational integrity
- Foreign key constraints enforced
- No duplicated data
- Use UUIDs where needed
- Soft delete where required
- Audit timestamps on all models

---

## 2. Core Entities

User
Organization
Role
Event
AttendanceSession
AttendanceRecord
Violation
Payment
BorrowRequest
BorrowItem
Announcement
DiscussionThread
Report
Feedback
CampusLocation

---

## 3. Example Relationships

User
    → belongs to Organization
    → has Role

Event
    → created by Admin
    → has AttendanceSession
    → has Feedback

AttendanceRecord
    → linked to Event
    → linked to Student

Violation
    → linked to Student
    → linked to Event

Payment
    → linked to Student
    → linked to Violation (optional)

BorrowRequest
    → linked to Student
    → linked to BorrowItem
