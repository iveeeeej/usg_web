# Agent Development Rules

## Campus Connect – Strict Development Guidelines for AI Agents

This document defines mandatory rules the AI agent must follow when
developing, debugging, or modifying the Campus Connect codebase.
These rules exist to minimize hallucinations, errors, and bugs.

------------------------------------------------------------------------

## Rule 1: Read Before You Write

Before modifying ANY file, the agent MUST read the file first.
The agent must NEVER assume what a file contains.
If the file has not been read in the current session, it must be read again.

------------------------------------------------------------------------

## Rule 2: Reference Documentation First

Before implementing any feature, the agent MUST read and reference
the relevant documentation files in `docs/`.

Mandatory reference chain for any new feature:
1. `09_development_phases.md` – phase scope and deliverables
2. `04_database_design_principles.md` – model design rules
3. `06_api_design_guidelines.md` – endpoint patterns
4. `07_security_and_permissions.md` – permission enforcement
5. `05_backend_structure.md` – where code belongs

The agent must NOT invent requirements that are not in the docs.

------------------------------------------------------------------------

## Rule 3: No Hallucinated Imports, Packages, or Functions

The agent must NEVER reference:
- A Python package that is not installed
- A Django app that does not exist in INSTALLED_APPS
- A model field that does not exist
- A function or class that has not been defined

If unsure whether something exists, the agent must CHECK first.

------------------------------------------------------------------------

## Rule 4: Discuss Before Implementing

Before writing any implementation code, the agent must:
1. Present the proposed approach to the user
2. Explain the models, endpoints, and logic
3. Wait for explicit user confirmation

The agent must NOT jump into code changes without discussion.

------------------------------------------------------------------------

## Rule 5: One Step at a Time

The agent must implement features incrementally:
1. Models first (and migrate)
2. Serializers second
3. Views/endpoints third
4. Business logic/services fourth
5. Test and verify after each step

The agent must NOT implement everything at once.

------------------------------------------------------------------------

## Rule 6: Verify After Every Change

After every code change, the agent must run at minimum:

    python manage.py check

If models were changed:

    python manage.py makemigrations
    python manage.py migrate

If endpoints were added, the agent must verify they are accessible.

The agent must NOT assume code works without verification.

------------------------------------------------------------------------

## Rule 7: Match Existing Code Patterns

The agent must follow patterns already established in the codebase:
- Permission classes follow the pattern in `accounts/permissions.py`
- Views follow the pattern in `accounts/views.py`
- URLs follow the pattern in `config/urls.py`
- Settings follow the pattern in `config/settings/base.py`

The agent must NOT introduce new patterns without explicit discussion.

------------------------------------------------------------------------

## Rule 8: Never Modify Without Explaining

Every file modification must include:
- What is being changed
- Why it is being changed
- What it affects

The agent must NOT silently change files.

------------------------------------------------------------------------

## Rule 9: Record Everything in Documentation

All progress, decisions, and mistakes MUST be recorded in the
documentation file (`00_Foundation_Setup_Documentation.md` for Phase 1,
and the appropriate doc for subsequent phases).

If the agent makes a mistake during development, the mistake MUST be
documented including:
- What the mistake was
- Why it happened
- How it was corrected

------------------------------------------------------------------------

## Rule 10: Respect the Database Design Principles

From `04_database_design_principles.md`:
- UUID primary keys for major entities
- Foreign key constraints enforced
- Audit timestamps (`created_at`, `updated_at`) on editable transactional models; append-only attachment records may use `created_at` only unless updates are expected
- Normalization up to 3NF
- Explicit indexing for frequently queried fields
- Controlled status transitions

The agent must NOT deviate from these principles.

------------------------------------------------------------------------

## Rule 11: Respect the Security Model

From `07_security_and_permissions.md`:
- Every protected endpoint MUST verify authentication AND role
- STUDENT endpoints must verify resource ownership
- All validation is server-side
- Frontend is never trusted

The agent must NOT create unprotected endpoints.

------------------------------------------------------------------------

## Rule 12: Use Environment Variables for Configuration

All configurable values (thresholds, timeouts, secret keys) must be
loaded from environment variables or Django settings.

The agent must NOT hardcode configuration values in source code.

------------------------------------------------------------------------

## Rule 13: Test with Real Data Scenarios

When verifying endpoints, the agent must test with realistic scenarios:
- Valid requests (expected success)
- Invalid requests (expected rejection)
- Edge cases (boundary conditions)
- Permission violations (wrong role accessing endpoint)

------------------------------------------------------------------------

## Rule 14: Keep the User Informed

The agent must:
- Explain what it is about to do before doing it
- Report results after each step
- Ask for clarification when requirements are ambiguous
- Never assume user intent

------------------------------------------------------------------------

## Rule 15: Git-Safe Changes Only

The agent must NOT:
- Delete files without explicit user approval
- Overwrite files without reading them first
- Modify `.env` without informing the user
- Touch `venv/` or any dependency internals

------------------------------------------------------------------------

## Rule 16: Error Recovery Protocol

If the agent encounters an error:
1. STOP immediately
2. Report the exact error message
3. Analyze the root cause
4. Propose a fix
5. Wait for user approval before applying the fix
6. Document the error and fix in the documentation

The agent must NOT silently retry or work around errors.

------------------------------------------------------------------------

## Rule 17: No Over-Engineering

The agent must implement ONLY what is specified in the current phase.

Before implementation begins, the agent must identify the active phase in
`09_development_phases.md` and restate the exact in-scope deliverables for that phase.

Examples:
- if the active phase is Phase 2, focus on governance and communication modules
- if the active phase is Phase 3, focus on attendance and accountability modules

The agent must NOT implement features from later phases.

------------------------------------------------------------------------

## Rule 18: Consistent Naming Conventions

- Django apps: lowercase, singular or plural matching existing pattern
- Models: PascalCase
- Fields: snake_case
- URLs: lowercase with hyphens or slashes
- Serializers: {ModelName}Serializer
- Views: {ModelName}{Action}View or {ModelName}ViewSet
- Permissions: Is{RoleName} or Can{Action}

------------------------------------------------------------------------

## Rule 19: Migration Safety

Before running `makemigrations`:
- Verify the model code is syntactically correct
- Verify all imports exist
- Verify all referenced models exist

After running `migrate`:
- Verify the migration applied without errors
- Check that the database state is consistent

The agent must NEVER manually edit migration files unless absolutely
necessary and explicitly discussed.

------------------------------------------------------------------------

## Rule 20: Document Format Standard

Documentation entries must follow this format:

    ## [Section Number]. [Title]

    [Detailed description of what was done]

    Key changes:
    - [Change 1]
    - [Change 2]

    Verification:
    - [How it was verified]

    Mistakes (if any):
    - [What went wrong]
    - [How it was fixed]
