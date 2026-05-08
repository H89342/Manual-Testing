# TESTCASE_RULES_SHARED.md
> Foundation rules for writing test cases across any module or project — UI, Mobile, or API.
> **Extension files:** UI/Mobile → `TESTCASE_RULES_UI.md` · API → `TESTCASE_RULES_API.md`
> Keep this file at the root of your QA folder. Read it before any extension file.

---

## Table of Contents

1. [File Structure Rules](#1-file-structure-rules)
2. [Mandatory Fields](#2-mandatory-fields)
3. [Writing Rules](#3-writing-rules)
4. [Naming & ID Convention](#4-naming--id-convention)
5. [Priority & Type Definitions](#5-priority--type-definitions)
6. [Status Definitions](#6-status-definitions)
7. [Test Data Rules](#7-test-data-rules)
8. [Environment Tags](#8-environment-tags)
9. [Templates & Full Examples](#9-templates--full-examples)
10. [Pre-Submit Checklist](#10-pre-submit-checklist)
11. [Anti-Patterns to Avoid](#11-anti-patterns-to-avoid)
12. [Execution Summary Format](#12-execution-summary-format)
13. [Requirement Clarification Log](#13-requirement-clarification-log)

---

## 1. File Structure Rules

### File naming
```
testcases_[module]_v[version].md

Examples:
  testcases_checkout_v1.md
  testcases_login_v2.md
  testcases_user_profile_v1.md
```

- Always lowercase
- Use underscores, no spaces or hyphens
- Increment version when making breaking structural changes
- One file per module — never mix two modules in one file

### Folder structure
```
/qa
  TESTCASE_RULES_SHARED.md      ← shared foundation (this file)
  TESTCASE_RULES_UI.md          ← UI / mobile extension
  TESTCASE_RULES_API.md         ← API extension
  /checkout
    testcases_checkout_v1.md
  /auth
    testcases_login_v1.md
    testcases_signup_v1.md
  /api
    testcases_payment_api_v1.md
```

### File header (required at top of every test case file)
```
# Test Cases: [Module Name]

## Overview

| Field       | Value                        |
|-------------|------------------------------|
| Author      | Your Name                    |
| Date        | YYYY-MM-DD                   |
| Version     | 1.0                          |
| Module      | [Module Name]                |
| Environment | Web / Mobile / API / Mixed   |
| Status      | In Progress / Complete       |
```

> After the Overview block, insert the **Execution Summary** block (see Section 12).
> Order in every file: `Overview` → `Execution Summary` → test cases → `Summary table`.

---

## 2. Mandatory Fields

Every single test case MUST contain all of the following fields. A TC is not complete without them.

| Field | Required | Notes |
|-------|----------|-------|
| TC ID | YES | Format: `ModuleName-001`. Never reuse or skip. |
| Screen / Section | YES | The screen name, page, or document section this TC maps to (e.g. `Login Page`, `Section 3.2 – Password Reset`, `Checkout – Step 2`). Used for requirement traceability. |
| Title | YES | Verify <expected result> when <action/condition> |
| Preconditions | YES | At least one bullet. Never leave blank. |
| Steps table | YES | Min 2 steps. Action steps only. Each item on its own line within the cell. |
| Expected Result | YES | Each item on its own line within the cell. |
| Test Data | YES | Fenced code block. Even if just one field. |
| Postconditions | YES | System/DB truth after the test passes. |
| Status | YES | Default: `Not Run`. Fill after execution only. |
| Priority | YES | High / Medium / Low |
| Type | YES | See Section 5 for allowed values |
| Environment | YES | Web / Mobile / API / Mixed |
| Notes | NO | Leave blank if nothing unusual. |

### Excel Export Column Order

When exporting test cases to Excel, columns must follow the same order as the mandatory fields above — left to right:

| Column | A | B | C | D | E | F | G | H | I | J | K | L | M |
|--------|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Field** | TC ID | Screen / Section | Title | Preconditions | Steps (Action) | Expected Result | Test Data | Postconditions | Status | Priority | Type | Environment | Notes |

- Do not reorder, hide, or merge columns.
- Column names in the header row must match exactly as listed above.
- Each item within Preconditions, Steps, Expected Result, Postconditions uses a line break inside the cell (`Alt + Enter`). Do not split into multiple rows.

### Excel Cell Formatting

Apply the following formatting to every test case sheet to avoid manual re-formatting after each export.

#### Wrap Text
Enable **Wrap Text** on **all cells** — header row and every data row, every column.
Never leave cells in overflow mode (text spilling into adjacent cells).

#### Vertical Alignment

| Alignment | Columns |
|-----------|---------|
| **Top** | Preconditions (D) · Steps / Action (E) · Expected Result (F) |
| **Center** | TC ID (A) · Screen / Section (B) · Title (C) · Test Data (G) · Postconditions (H) · Status (I) · Priority (J) · Type (K) · Environment (L) · Notes (M) |

> Rule: Top alignment is applied to the three columns that contain multi-line content (bullet lists or numbered steps). All other columns use center alignment so short values do not float to the top of tall rows.

---

## 3. Writing Rules

### Rule 01 — One behaviour per TC
> Each test case tests exactly ONE behaviour or scenario.
> If a title needs "and", split it into two TCs if possible.

```
BAD:  Login-010: Login with valid credentials and verify dashboard loads
GOOD: Login-010: Verify login successfully with valid credentials
      Dashboard-011: Verify dashboard loads after successful login
```

### Rule 02 — Title = action + condition
> Titles must always start with verify followed by the action verb in -ing form or gerund phrase. The condition must be in the title for specific negative/edge cases.

```
BAD:  TC-005: Email field
BAD:  TC-005: Email test
GOOD: TC-005: Verify submitting login unsuccessfully with an empty email field
GOOD: TC-006: Verify submitting checkout unsuccessfully with expired credit card
```

Allowed verbs: `Submitting` · `Entering` · `Clicking` · `Navigating` · `Applying` · `Uploading` · `Deleting` · `Loading` · `Triggering` · `Sending` · `Canceling` · `Rejecting` · `Confirming` · `Displaying` · `Showing` · `Tapping` · `Swiping`

### Rule 03 — Expected results must be specific
> Never write vague expected results. Always quote the exact message, state, or value.

```
BAD:  Error message appears
BAD:  Page loads correctly
GOOD: Shows inline error: "Email is required"
GOOD: Redirected to /dashboard with status 200
GOOD: Order record created with status = PAID in database
```

### Rule 04 — Steps use the table format only
> Always write detailed steps from the beginning of the module/screen.
> Never write steps as prose paragraphs. Always use `| # | Action | Expected Result |`.

```
BAD:
First the user navigates to /login, then enters their email and password,
then clicks Sign In, and then they should see the dashboard.

GOOD:
| # | Action                            | Expected Result                   |
|---|-----------------------------------|-----------------------------------|
| 1 | Navigate to /login                | Login page renders correctly      |
| 2 | Enter valid email and password    | Fields accept input               |
| 3 | Click "Sign In"                   | Redirected to /dashboard          |
```

### Rule 05 — Test data goes in a fenced code block
> Never embed test data inline in prose or in the steps table. Always use a separate code block.

```
BAD:  Use email test@example.com and password SecurePass123
GOOD:
​```
email:     test@example.com
password:  SecurePass123
​```
```

### Rule 06 — Preconditions state every assumption
> Write every setup requirement. Nothing implied. Include browser version, login state, data state.

```
BAD:  User is ready to test
GOOD:
- User is logged out
- Browser: Chrome 120+ with no extensions
- Cart contains exactly 2 items (SKU-001 x1, SKU-002 x1)
- Coupon DEMO20 exists and is active in the system
```

### Rule 07 — Postconditions state system truth
> What must be true in the backend/database after the test passes — not just the UI.

```
BAD:  User sees success message
GOOD:
- Order record created in DB with status = PAID
- Inventory for SKU-001 decremented by 1
- Confirmation email sent within 2 minutes
- Webhook fired to /webhook/payment-success
```

### Rule 08 — Status stays Not Run until executed
> Never pre-fill PASS. A TC that hasn't been run is always Not Run.

```
BAD:  **Status:** PASS  ← written before the test is run
GOOD: **Status:** Not Run
```

### Rule 09 — Separate every TC with a horizontal rule
> Use `---` between every test case. Never let two TCs visually merge.

### Rule 10 — No abbreviations in titles
> Titles must be readable by someone unfamiliar with the project.

```
BAD:  Submit auth form w/ invalid pwd
GOOD: Verify submitting authentication form unsuccessfully with invalid password
```

---

## 4. Naming & ID Convention

### TC ID format
```
ModuleName-NNN     (3 digits, zero-padded)

ModuleName-001  ModuleName-042  ModuleName-100  ModuleName-999
```

- Always 3 digits, zero-padded
- IDs are permanent — deleted TCs leave a gap, never fill it
- IDs are assigned sequentially — never skip numbers

### Module prefix codes (for multi-module projects)
When a project has multiple modules, assign a short prefix code to each module.
These codes go before the hyphen in TC IDs (e.g. `AUTH-001`, `CHKOUT-012`).

```
AUTH, LOGIN, CHKOUT, PAY, ORD
```

- Module code: 2–5 uppercase letters
- Consistent across the whole project — define the prefix list upfront

### Summary table (required at the bottom of every file)
Every test case file must end with a summary table:

```markdown
## Summary

| TC ID      | Screen / Section  | Title     | Type     | Priority | Status  |
|------------|-------------------|-----------|----------|----------|---------|
| **AUTHENTICATION** |             |           |          |          |         |
| AUTH-001   | [Screen/Section]  | [Title]   | [Type]   | High     | Not Run |
| AUTH-002   | [Screen/Section]  | [Title]   | [Type]   | Medium   | Not Run |
| **CHECKOUT** |               |           |          |          |         |
| CHKOUT-001 | [Screen/Section]  | [Title]   | [Type]   | High     | Not Run |
| CHKOUT-002 | [Screen/Section]  | [Title]   | [Type]   | Medium   | Not Run |
```

---

## 5. Priority & Type Definitions

### Priority

| Level | Definition | Examples |
|-------|------------|---------|
| **High** | Core functionality. Blocking if it fails. Ship-stopping. | Login, payment, data save |
| **Medium** | Important but has a workaround. Degrades experience. | Coupon codes, email notifications |
| **Low** | Nice-to-have or cosmetic. Non-blocking. | UI alignment, special characters, large data |

> Rule: At least 30% of TCs in any module should be High priority.

### Type

| Type | Definition |
|------|------------|
| `Functional` | Happy path — valid inputs, expected flow, system works as designed |
| `Negative` | Invalid inputs, error states, rejection flows |
| `Edge Case` | Boundary values, timeouts, race conditions, extreme inputs |
| `UI` | Visual layout, responsiveness, element visibility |
| `API` | Direct endpoint testing — request/response validation |
| `Regression` | Tests that guard against previously fixed bugs reappearing |
| `Performance` | Load time, response time, throughput under stress |
| `Security` | Auth bypass, injection, permission escalation attempts |

---

## 6. Status Definitions

| Status | Meaning | Who Sets It |
|--------|---------|-------------|
| `PENDING` | Awaiting decision on whether to run (with reason in Notes) | QA tester |
| `PASS` | Executed and all expected results met | QA tester |
| `FAIL` | Executed and at least one expected result not met | QA tester |
| `SKIP` | Intentionally not run this cycle (with reason in Notes) | QA lead |
| `BLOCKED` | Cannot be run due to a dependency or environment issue | QA tester |
| `IN PROGRESS` | Currently being executed | QA tester |
| `Not Run` | Written but not yet executed | Author (default) |

> Rule: Always add a reason in Notes when Status is SKIP or BLOCKED or PENDING.

---

## 7. Test Data Rules

### Format
Always use a fenced code block for test data. Use `key: value` pairs.

````markdown
#### Test Data

```
email:        test@example.com
password:     SecurePass123!
card_number:  4111 1111 1111 1111
expiry:       12/28
cvv:          123
```
````

### Test data categories

| Category | Rule |
|----------|------|
| **Valid data** | Use dedicated test accounts, never production data |
| **Invalid data** | State WHY it is invalid in a comment |
| **Boundary data** | State the boundary explicitly (e.g. "max 255 chars") |
| **Sensitive data** | Never use real card numbers, SSNs, or passwords — use test/sandbox values only |
| **API payloads** | Use full JSON, not partial. Include all fields even if not under test. |

### Test card numbers reference (sandbox only)

```
Visa (success):     4111 1111 1111 1111
Mastercard:         5500 0000 0000 0004
Declined:           4000 0000 0000 0002
Insufficient funds: 4000 0000 0000 9995
Expired card:       any card with past expiry date
Wrong CVV:          4111 1111 1111 1111 + CVV 000
```

---

## 8. Environment Tags

Use these exact tags in the Environment field. Be as specific as possible.

| Tag | Meaning |
|-----|---------|
| `Web` | Browser-based — always specify: Chrome 120+ / Firefox 121+ / Safari 17+ |
| `Mobile` | Native app — specify: iOS 16+ / Android 12+ |
| `API` | REST API — specify: v1 / v2, include auth method |
| `Mixed` | Covers more than one environment — list all that apply |

### Examples
```
Environment: Web (Chrome 120+, Firefox 121+)
Environment: Mobile (iOS 17 / Android 13)
Environment: API (REST v1, Bearer token auth)
Environment: Mixed — Web + API
```

---

## 9. Templates & Full Examples

> Blank templates and full worked examples are stored in the extension files — do not duplicate them here.

| TC Type | Template Location |
|---------|------------------|
| UI / Mobile | `TESTCASE_RULES_UI.md` — Section 1 (blank template) and Section 2 (full example) |
| API | `TESTCASE_RULES_API.md` — Section 8 (blank template) |

---

## 10. Pre-Submit Checklist

> Run through this checklist before committing or sharing any test case file.

### Per test case

- [ ] TC ID is unique and follows `ModuleName-001` format
- [ ] Title follows format: `Verify <expected result> when <action/condition>` (or `Verify <state/observation>` for non-action tests)
- [ ] Screen / Section is filled in — identifies the exact screen, page, or document section this TC maps to
- [ ] Preconditions list all assumptions — nothing implied
- [ ] Steps use the table format with at least 2 rows
- [ ] Expected results are specific — exact messages or states quoted
- [ ] Test data is in a fenced code block
- [ ] Postconditions describe DB/system truth, not just UI
- [ ] Priority is set (High / Medium / Low)
- [ ] Type is set from the allowed list
- [ ] Environment is specific (browser version, OS, API version)
- [ ] Status is set to `Not Run`
- [ ] TC ends with `---`

### Per file

- [ ] File is named `testcases_[module]_v[version].md`
- [ ] File header (Overview table) is filled in completely
- [ ] Execution Summary block (Section 12) is present and up to date after every run
- [ ] Table of Contents lists all TCs
- [ ] Summary table at the bottom is up to date
- [ ] No two modules are mixed in the same file
- [ ] No duplicate TC IDs exist in the file

---

## 11. Anti-Patterns to Avoid

These are the most common mistakes. Avoid them.

| Anti-Pattern | Why It's Bad | Fix |
|---|---|---|
| Vague expected results ("error appears") | Tester must guess what "correct" looks like | Quote the exact message or state |
| Prose steps instead of table | Slow to scan, easy to miss steps | Always use `\| # \| Action \| Expected Result \|` |
| Test data embedded in prose | Not copy-paste ready; ambiguous values | Fenced code block, every time |
| Pre-filling Status as PASS | Defeats the purpose of test tracking | Always start with Not Run |
| Multiple behaviours in one TC | Impossible to know which part failed | One behaviour per TC |
| Missing postconditions | Tester only checks UI, misses DB bugs | Always state backend truth |
| "N/A" for preconditions | Almost never truly N/A | Write at least "User is on the home page" |
| Reusing a deleted TC ID | Breaks bug report history | Leave the gap; IDs are permanent |
| Skipping the test data block for "obvious" values | Someone will use wrong data | Always include, even for simple cases |
| Writing "see above" in expected results | Context is lost when TCs are exported | Every TC must be self-contained |

---

## 12. Execution Summary Format

> Every test case file MUST include an **Execution Summary** block immediately after the Overview block.
> Every project MUST maintain a **Project Dashboard** file at `/qa/PROJECT_DASHBOARD.md` that rolls up all individual files.
> Update both after every test execution cycle.

### 12.1 Per-File Execution Summary

> Place this block at the top of each test case file, right after the Overview table.
> Recount after every execution pass. Numbers must match the Summary table at the bottom of the file.

```markdown
## Execution Summary

**Last updated:** YYYY-MM-DD by [Name]
**Test Cycle:** [Sprint / Release / Build number]

#### Status Counts

| Status        | Count | % of Total |
|---------------|-------|------------|
| Total TCs     |   0   | 100%       |
| Pass          |   0   | 0%         |
| Fail          |   0   | 0%         |
| Blocked       |   0   | 0%         |
| Skip          |   0   | 0%         |
| In Progress   |   0   | 0%         |
| Pending       |   0   | 0%         |
| Not Run       |   0   | 0%         |

#### Derived Metrics

| Metric                             | Formula                   | Value   |
|------------------------------------|---------------------------|---------|
| Executed                           | Pass + Fail               | 0 / 0   |
| Execution Progress %               | Executed / Total          | 0%      |
| Pass Rate %                        | Pass / Executed           | 0%      |

#### Priority Breakdown

| Priority   | Total | Pass | Fail | Blocked | Not Run | Pass Rate % |
|------------|-------|------|------|---------|---------|-------------|
| High       |   0   |  0   |  0   |   0     |   0     |     0%      |
| Medium     |   0   |  0   |  0   |   0     |   0     |     0%      |
| Low        |   0   |  0   |  0   |   0     |   0     |     0%      |
| **Total**  |   0   |  0   |  0   |   0     |   0     |     0%      |
```

#### Filled-in example

```markdown
## Execution Summary

**Last updated:** 2026-04-19 by Hanna Lee
**Test Cycle:** Sprint 24 / Release 2.5

#### Status Counts

| Status        | Count | % of Total |
|---------------|-------|------------|
| Total TCs     |  50   | 100%       |
| Pass          |  30   | 60%        |
| Fail          |   5   | 10%        |
| Blocked       |   2   | 4%         |
| Skip          |   1   | 2%         |
| In Progress   |   2   | 4%         |
| Pending       |   0   | 0%         |
| Not Run       |  10   | 20%        |

#### Derived Metrics

| Metric                             | Formula                   | Value        |
|------------------------------------|---------------------------|--------------|
| Executed                           | Pass + Fail               | 35 / 50      |
| Execution Progress %               | Executed / Total          | 70%          |
| Pass Rate %                        | Pass / Executed           | 85.7%        |

#### Priority Breakdown

| Priority   | Total | Pass | Fail | Blocked | Not Run | Pass Rate % |
|------------|-------|------|------|---------|---------|-------------|
| High       |  20   |  18  |  1   |   1     |   0     |   94.7%     |
| Medium     |  20   |  10  |  3   |   1     |   6     |   76.9%     |
| Low        |  10   |   2  |  1   |   0     |   7     |   66.7%     |
| **Total**  |  50   |  30  |  5   |   2     |  13     |   85.7%     |
```

---

### 12.2 Project-Wide Rollup Dashboard

> Store this file at `/qa/PROJECT_DASHBOARD.md`. It rolls up every per-file Execution Summary into one view.
> One row per test case file. Numbers must match the latest Execution Summary inside each file.
> Update after every execution cycle, before the release gate review.

```markdown
# Project Execution Dashboard

**Last updated:** YYYY-MM-DD by [Name]
**Test Cycle:** [Sprint / Release / Build number]
**Release Gate:** [Open / Blocked]

## All Modules — Status Rollup

| Module / File                  | Total | Pass | Fail | Blocked | Skip | In Progress | Pending | Not Run | Execution % | Pass Rate % |
|--------------------------------|-------|------|------|---------|------|-------------|---------|---------|-------------|-------------|
| testcases_login_v1.md          |   0   |  0   |  0   |   0     |  0   |     0       |    0    |   0     |    0%       |    0%       |
| testcases_checkout_v1.md       |   0   |  0   |  0   |   0     |  0   |     0       |    0    |   0     |    0%       |    0%       |
| testcases_payment_api_v1.md    |   0   |  0   |  0   |   0     |  0   |     0       |    0    |   0     |    0%       |    0%       |
| **TOTAL**                      |   0   |  0   |  0   |   0     |  0   |     0       |    0    |   0     |    0%       |    0%       |

## High-Priority Rollup (Release Gate)

> Release ships only when this table is green: all High-priority TCs executed and pass rate ≥ 98%.

| Module / File                  | High Total | High Pass | High Fail | High Blocked | High Pass Rate % |
|--------------------------------|------------|-----------|-----------|--------------|------------------|
| testcases_login_v1.md          |     0      |    0      |    0      |      0       |       0%         |
| testcases_checkout_v1.md       |     0      |    0      |    0      |      0       |       0%         |
| testcases_payment_api_v1.md    |     0      |    0      |    0      |      0       |       0%         |
| **TOTAL**                      |     0      |    0      |    0      |      0       |       0%         |

## Release Readiness Checklist

- [ ] All High-priority TCs executed (no High in Not Run / Pending / In Progress)
- [ ] High-priority pass rate ≥ 98%
- [ ] Zero unresolved High-priority Blocked TCs
- [ ] Every Fail is linked to a logged bug ticket in Notes
- [ ] Overall execution progress ≥ 95%
- [ ] Every SKIP / BLOCKED / PENDING status has a written reason in Notes
```

---

### 12.3 Update Cadence & Ownership

| Event                        | Who Updates                  | What They Update                                |
|------------------------------|------------------------------|-------------------------------------------------|
| New test case added          | Author                       | Per-file Status Counts (Total, Not Run + 1)     |
| Test case executed           | QA tester                    | Per-file counts + Priority Breakdown            |
| End of test cycle            | QA lead                      | Per-file `Last updated` + full recount          |
| Before release gate review   | QA lead                      | `PROJECT_DASHBOARD.md` rollup + Readiness boxes |

> Rule: If a per-file Execution Summary and its bottom Summary table disagree on counts, the bottom Summary table is the source of truth. Recount and update the Execution Summary.

---

## 13. Requirement Clarification Log

> Use this section whenever a requirement is ambiguous, missing, or conflicts with any source — User Story, description document, Figma screen, or API spec.
> Never guess or assume. Stop writing the affected TC, log the clarification, mark the TC as `PENDING`, and wait for a confirmed answer before proceeding.
> This process applies to all TC types: **UI** and **API**.

---

### 13.1 When to log — reading from User Story / Description (no Figma)

Apply when the requirement source is text only: Jira story, Confluence page, PRD, feature brief, or verbal handover — with no accompanying Figma design.

Log an entry when:

| Trigger | Example |
|---------|---------|
| **Incomplete acceptance criteria** | Story says "user can reset password" but acceptance criteria do not define the reset flow, expiry time, or error states |
| **Ambiguous language** | Requirements use "should", "may", "might", or "as appropriate" without defining the exact behaviour |
| **Happy path only** | Story describes the success flow but does not define what happens on failure, invalid input, or edge conditions |
| **Contradicting stories** | Two user stories or two acceptance criteria in the same story define conflicting behaviour for the same feature |
| **Undefined field or value** | A field name is mentioned in the story but its allowed values, format, or constraints are never stated |
| **Unclear scope boundary** | It is ambiguous whether a behaviour is in or out of scope for this story (e.g. "handle errors" — which errors?) |
| **Missing business rule** | A rule is implied but never written (e.g. "user must be verified" — but what makes a user verified?) |
| **No definition of done for edge cases** | Story does not state what the system must do when an unusual but valid input is provided |

---

### 13.2 When to log — reading from Figma screens

Apply when the requirement source includes a Figma design (with or without an accompanying User Story).

Log an entry when:

- Two screens or states contradict each other (e.g. one screen shows a field as mandatory, another shows it as optional)
- Expected behaviour on a failure path is shown as a screen state but the triggering condition is not defined
- A field label, error message, or copy text is shown as a placeholder and never finalised
- A business rule is implied by the design but never stated (e.g. what happens after N failed attempts)
- A flow has no defined exit, fallback, or back-navigation state
- A screen shows a component (button, banner, badge) but does not define when it appears or disappears
- Figma annotation contradicts the User Story description for the same feature

---

### 13.3 When to log — reading from API spec

Apply when the requirement source is an API specification: Swagger / OpenAPI, Postman collection, wiki endpoint documentation, or verbal API brief.

Log an entry when:

| Trigger | Example |
|---------|---------|
| **Undocumented status code** | Spec defines `200` and `404` but does not define `500`, rate limit, or timeout responses |
| **Unclear required vs optional fields** | Spec lists `quantity` in the request body without stating whether it is required or optional |
| **Missing error response schema** | Success response body is defined but error response body fields and types are not |
| **Conflicting documentation** | Swagger says a field is `string`, but the Postman example shows an `integer` |
| **Undefined side effects** | Spec does not state whether a `POST /order/confirm` triggers an email, a webhook, or a DB write |
| **Unclear auth requirement** | Spec does not state whether an endpoint requires a Bearer token or is publicly accessible |
| **Ambiguous idempotency** | Unclear whether sending the same `POST` twice creates a duplicate record or returns the existing one |
| **Missing pagination rules** | `GET` endpoint returns a list but page size, max results, and cursor behaviour are not defined |
| **Chaining value not confirmed** | The field name returned by endpoint A (needed by endpoint B) is not confirmed in the spec |

---

### 13.4 Clarify Requirements sheet — column definitions

One sheet covers all three sources: User Story, Figma, and API spec. Use the **Source / Reference** column to distinguish origin.

| Column | Field | Description |
|--------|-------|-------------|
| A | Ref # | Unique ID. Format: `CQ-001`. Sequential, never reuse. |
| B | Related TC ID | TC ID blocked by this question (e.g. `LOGIN-003` or `API-002`). Write `General` if not tied to a specific TC. |
| C | Source / Reference | Where the conflict was found. User Story: `Story US-042`. Figma: `Screen / Login Page`. API: `POST /api/v1/auth/login`. |
| D | Conflict Description | Describe the conflict or ambiguity clearly. Quote field names, status codes, acceptance criteria, or screen labels exactly. |
| E | Question to Client | The specific question to ask. One question per row. Must be answerable with a clear decision. |
| F | Priority | `High` — blocks TC writing. `Medium` — TC can be partially written. `Low` — cosmetic or low-risk assumption. |
| G | Raised By | Name of the person who logged the question. |
| H | Raised Date | Date the question was logged. Format: `YYYY-MM-DD`. |
| I | Answer / Resolution | The confirmed answer from the client or BA. Leave blank until answered. |
| J | Status | `Open` — waiting for answer. `Answered` — reply received, update TC. `Closed` — TC updated and verified. |
| K | Resolved Date | Date the answer was received and confirmed. Format: `YYYY-MM-DD`. |

### 13.5 Export rules

| TC Type | Primary Export | Excel CQ Sheet |
|---------|---------------|--------------|
| **UI test cases** | Excel — `Clarify Requirements` sheet (always included) | Always exported alongside the TC sheet |
| **API test cases** | Postman — warning block in pre-script + `[PENDING]` request prefix | Only exported to Excel when the client explicitly requests a combined report |

> Rule: For API TCs, the Clarify Requirements sheet in Excel is **not generated by default**. It is generated only when the client asks for a full Excel export. The Postman pre-script warning block is the primary way to track open API questions during testing.

### 13.6 Rules (applies to all sources and TC types)

- One question per row. Never combine two questions into one entry.
- The TC linked in column B must be set to `PENDING` status until column J shows `Answered` or `Closed`.
- Once answered, update the TC immediately and change Status to `Closed`.
- Never delete a row. Closed entries are permanent audit records.
- If the same conflict appears across multiple TCs, log once and list all TC IDs in column B separated by commas.

### 13.7 TC row highlighting rule

Any TC row — whether UI or API — that has an open clarification question must be visually highlighted.

| Highlight Color | Meaning |
|-----------------|---------|
| Orange (`#FFC000`) | TC has at least one `Open` question in Clarify Requirements — do not execute |
| No highlight (default) | TC is clear — no open questions |

**For UI TCs (Excel):**
- Fill the entire TC row with orange (`#FFC000`) when its TC ID appears in column B of any `Open` CQ row.
- Add the linked CQ reference (e.g. `Blocked by CQ-001`) in the TC's Notes cell (column L).
- Remove the highlight and update Notes when the CQ Status changes to `Closed`.

**For API TCs (Postman):**
- Add a comment block at the top of the pre-request script of the affected request:
```javascript
// ⚠ OPEN CLARIFICATION — CQ-007
// Question: [paste the question from the CQ sheet]
// Status: Open — do not run this request until resolved.
// Ref: Clarify Requirements sheet → CQ-007
```
- The Postman request name must be prefixed with `[PENDING]` until resolved: `[PENDING] API-002: Verify ...`
- Remove the comment and prefix once the CQ is closed.

### 13.8 Status flow

```
Open  →  Answered  →  Closed
              ↓
        (update TC + Postman request)
```

### Example entry

| Ref # | Related TC ID | Source / Reference | Conflict Description | Question to Client | Priority | Raised By | Raised Date | Answer / Resolution | Status | Resolved Date |
|-------|--------------|-------------------|----------------------|--------------------|----------|-----------|-------------|---------------------|--------|---------------|
| CQ-001 | LOGIN-003 | Figma: Screen / Login Error State | The error banner text on failed login is not defined in Figma. The banner component appears but the copy is placeholder text. | What is the exact error message shown when the user enters invalid credentials? | High | [Name] | YYYY-MM-DD | | Open | |
