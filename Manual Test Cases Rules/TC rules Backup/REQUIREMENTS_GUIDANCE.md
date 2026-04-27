# REQUIREMENTS_GUIDANCE.md
> Reusable input template for providing requirements to generate test cases.
> Fill in this template and share it (or paste it in chat) when requesting TC generation.
> Store completed files as: `requirements_[module]_v[version].md` inside the module's folder.

---

## Table of Contents

1. [How to Use This Template](#1-how-to-use-this-template)
2. [File Header](#2-file-header)
3. [Environment & Constraints](#3-environment--constraints)
4. [Test Data](#4-test-data)
5. [Out of Scope](#5-out-of-scope)
6. [Functional Requirements](#6-functional-requirements)
7. [Non-Functional Requirements](#7-non-functional-requirements)
8. [Acceptance Criteria](#8-acceptance-criteria)
9. [References](#9-references)

---

## 1. How to Use This Template

**Step 1** — Copy this file into the relevant module folder and rename it:
```
requirements_[module]_v[version].md

Examples:
  requirements_login_v1.md
  requirements_checkout_v2.md
  requirements_payment_api_v1.md
```

**Step 2** — Fill in every section. Do not leave placeholders in the final file.

**Step 3** — Share it by either:
- Opening both this file and `TESTCASE_RULES.md` in the IDE, then requesting TC generation
- Pasting the content directly in chat

**Step 4** — The generated output will be saved as:
```
testcases_[module]_v[version].md
```
in the same module folder.

---

## 2. File Header

```
# Requirements: [Module Name]

| Field       | Value                          |
|-------------|--------------------------------|
| Module      | [Module Name]                  |
| TC Prefix   | [2–5 uppercase letters — e.g. AUTH, CHKOUT, PAY] |
| Author      | [Your Name]                    |
| Date        | YYYY-MM-DD                     |
| Version     | 1.0                            |
| Source      | [Ticket / Story / Spec URL or reference] |
| Status      | Draft / Ready for TC Generation |
```

> **TC Prefix rule:** 2–5 uppercase letters, consistent across the project.
> Define it once here — this becomes the prefix for every TC ID (e.g. `AUTH-001`).

---

## 3. Environment & Constraints

Specify exactly where the feature runs and any version requirements.

```
Environment: Web | Mobile | API | Mixed

Web browsers (if applicable):
  - Chrome 120+
  - Firefox 121+
  - Safari 17+

Mobile (if applicable):
  - iOS 16+
  - Android 12+

API (if applicable):
  - REST / GraphQL
  - Version: v1 / v2
  - Auth method: Bearer token / API key / OAuth

Special constraints:
  - [e.g. Must work in RTL layout]
  - [e.g. Response time must be < 2s]
  - [e.g. Requires VPN access to staging]
```

---

## 4. Test Data

Provide all test accounts, credentials, and data values to be used.
Never use production data. Use sandbox/staging values only.

```
# Accounts
valid_user_email:     [e.g. testuser@demo.com]
valid_user_password:  [e.g. TestPass123!]
locked_user_email:    [e.g. locked@demo.com]
admin_email:          [e.g. admin@demo.com]

# Payment (sandbox only)
card_valid:           4111 1111 1111 1111  exp: 12/28  cvv: 123
card_declined:        4000 0000 0000 0002
card_insufficient:    4000 0000 0000 9995
card_expired:         any card with past expiry

# Other data
[field_name]:         [value]
[field_name]:         [value]
```

> Write `use sandbox defaults` if no specific data is required.

---

## 5. Out of Scope

List behaviors explicitly NOT being tested in this cycle.
This prevents unnecessary TC generation.

```
Out of scope for this requirement file:
- [e.g. Social login (Google / Facebook OAuth)]
- [e.g. Admin panel user management]
- [e.g. Password strength validation (covered in AUTH-v2)]
- [e.g. Mobile native app — Web only this cycle]
```

> If nothing is out of scope, write: `None — all listed requirements are in scope.`

---

## 6. Functional Requirements

List every behavior the system must support.
Use `FR-NNN` IDs. One behavior per line.

```
FR-001: [Actor] can [action] when [condition], resulting in [outcome].
FR-002: System must [behavior] when [trigger].
FR-003: [Field/Element] must [validation rule].
```

### Format guide

| Type | Example |
|------|---------|
| Happy path | `FR-001: User can log in with valid email and password and is redirected to /dashboard.` |
| Validation | `FR-002: Email field must reject input that does not contain "@" and a domain.` |
| Error state | `FR-003: System must display "Account locked" message after 5 consecutive failed login attempts.` |
| Redirect | `FR-004: Clicking "Forgot password" must redirect to /reset-password.` |
| Permission | `FR-005: Guest users must not be able to access /checkout — redirect to /login.` |
| API | `FR-006: POST /api/login must return HTTP 200 and a Bearer token on success.` |
| API error | `FR-007: POST /api/login must return HTTP 401 with body { "error": "Invalid credentials" } on failure.` |

---

## 7. Non-Functional Requirements

Optional. Include only if there are measurable non-functional expectations.

```
NFR-001: [Performance] Page must load within [X] seconds on a 4G connection.
NFR-002: [Security] Login endpoint must not reveal whether the email exists in the system.
NFR-003: [Accessibility] All form fields must have visible labels and ARIA attributes.
NFR-004: [Compatibility] Feature must work on the listed browsers without visual defects.
```

> Leave this section blank or remove it if there are no NFRs for this module.

---

## 8. Acceptance Criteria

Optional. Paste the original AC from your ticket/story here verbatim.
Useful for traceability — links the generated TCs back to the original requirement.

```
Given [context]
When  [action]
Then  [expected outcome]
```

### Example
```
Given the user is on the login page and has a valid account
When  they enter correct email and password and click Sign In
Then  they are redirected to /dashboard and a session token is stored

Given the user enters an incorrect password 5 times in a row
When  they attempt a 6th login
Then  the account is locked and "Account locked. Contact support." is displayed
```

---

## 9. References

Link to any supporting documents, designs, or tickets.

```
| Type        | Link / Reference                              |
|-------------|-----------------------------------------------|
| Ticket      | [e.g. JIRA-1234 / Linear-AUTH-56]             |
| Figma/Design| [URL or file path]                            |
| API Docs    | [URL or file path]                            |
| Previous TC | [e.g. testcases_login_v1.md]                  |
| Other       | [Any other relevant reference]                |
```
