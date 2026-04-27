# TESTCASE_RULES.md
> Reusable rules, templates, and standards for writing test cases across any module or project.
> Keep this file at the root of your QA folder. Reference it before writing any new test case.

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
9. [Blank Test Case Template](#9-blank-test-case-template)
10. [Full Example Test Case](#10-full-example-test-case)
11. [Pre-Submit Checklist](#11-pre-submit-checklist)
12. [Anti-Patterns to Avoid](#12-anti-patterns-to-avoid)
13. [Execution Summary Format](#13-execution-summary-format)
14. [Requirement Clarification Log](#14-requirement-clarification-log)
15. [API Test Case Rules](#15-api-test-case-rules)

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
  TESTCASE_RULES.md          ← this file (root reference)
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

> After the Overview block, insert the **Execution Summary** block (see Section 13).
> Order in every file: `Overview` → `Execution Summary` → test cases → `Summary table`.

---

## 2. Mandatory Fields

Every single test case MUST contain all of the following fields. A TC is not complete without them.

| Field | Required | Notes |
|-------|----------|-------|
| TC ID | YES | Format: `ModuleName-001`. Never reuse or skip. |
| Title | YES | Verify <expected result> when <action/condition>|
| Preconditions | YES | At least one bullet. Never leave blank. |
| Steps table | YES | Min 2 steps. Action steps only. Each item on its own line within the cell. |
| Expected Result| YES | Each item on its own line within the cell. |
| Test Data | YES | Fenced code block. Even if just one field. |
| Postconditions | YES | System/DB truth after the test passes. |
| Status | YES | Default: `Not Run`. Fill after execution only. |
| Priority | YES | High / Medium / Low |
| Type | YES | See Section 5 for allowed values |
| Environment | YES | Web / Mobile / API / Mixed |
| Notes | NO | Leave blank if nothing unusual. |

### Excel Export Column Order

When exporting test cases to Excel, columns must follow the same order as the mandatory fields above — left to right:

| Column | A | B | C | D | E | F | G | H | I | J | K | L |
|--------|---|---|---|---|---|---|---|---|---|---|---|---|
| **Field** | TC ID | Title | Preconditions | Steps (Action) | Expected Result | Test Data | Postconditions | Status | Priority | Type | Environment | Notes |

- Do not reorder, hide, or merge columns.
- Column names in the header row must match exactly as listed above.
- Each item within Preconditions, Steps, Expected Result, Postconditions uses a line break inside the cell (`Alt + Enter`). Do not split into multiple rows.

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

Allowed verbs: `Submitting` · `Entering` · `Clicking` · `Navigating` · `Applying` · `Uploading` · `Deleting` · `Loading` · `Triggering` · `Sending` · `Canceling` · `Rejecting` · `Confirming` · `Displaying` · `Showing`  · `Tapping` · `Swiping`    

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
> Always write detailed steps from the beginning of the module/screen
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

| TC ID  | Title                         | Type      | Priority | Status  |
|--------|-------------------------------|-----------|----------|---------|
| **AUTHENTICATION** |       |          |          |         |
| AUTH-001       | [Title]   | [Type]   | High     | Not Run |
| AUTH-002       | [Title]   | [Type]   | Medium   | Not Run |
| **CHECKOUT**   |           |          |          |         |
| CHKOUT-001   | [Title]   | [Type]   | High     | Not Run |
| CHKOUT-002   | [Title]   | [Type]   | Medium   | Not Run |
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

## 9. Blank Test Case Template

> Copy this block in full every time you write a new test case.
> Replace all `[placeholder]` text. Never delete a field — write N/A only if truly not applicable.

```markdown
### ModuleName-NNN: [Verify the expected result of — what is being tested]

**Priority:** High | Medium | Low
**Type:** Functional | Negative | Edge Case | UI | API | Regression | Performance | Security
**Environment:** Web | Mobile | API | Mixed

**Preconditions:**
- [Precondition 1]
- [Precondition 2]

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | [Action the user/system takes] | [Specific expected outcome] |
| 2 | [Next action] | [Next expected outcome] |
| 3 | [Continue as needed] | [Outcome] |

#### Test Data

​```
field_name:  value
field_name:  value
​```

**Postconditions:**
- [System/DB state after test passes — be specific]
- [e.g. Record created with status = X]

**Status:** Not Run
**Notes:** [Optional — known bugs, platform quirks, scope limits. Leave blank if none.]

---
```

---

## 10. Full Example Test Case

> Use this as a reference for what a correctly written TC looks like.

### CHECKOUT-001: Verify submitting checkout form successfully with valid credit card on web

**Priority:** High
**Type:** Functional
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)

**Preconditions:**
- User is logged in with a verified account
- Cart contains at least 1 item
- Shipping address is pre-saved in user profile
- Test environment: Staging with Stripe sandbox enabled

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Navigate to `/cart` | Cart page loads with correct items and total |
| 2 | Click "Proceed to Checkout" | Checkout page renders; billing form is visible |
| 3 | Verify pre-filled shipping address | Correct address is populated from user profile |
| 4 | Select "Credit Card" as payment method | Card input fields appear: number, expiry, CVV |
| 5 | Enter valid card details (see Test Data) | Card type icon (Visa) appears; fields accept input |
| 6 | Click "Place Order" | Button disables immediately; loading spinner appears |
| 7 | Wait for API response (~2s) | Redirected to `/order-confirmation` |
| 8 | Verify confirmation page | Order ID displayed; total matches cart amount |

#### Test Data

```
card_number:  4111 1111 1111 1111
expiry:       12/28
cvv:          123
card_name:    John Demo
email:        testuser@demo.com
```

**Postconditions:**
- Order record created in DB with `status = PAID`
- Inventory decremented for all purchased items
- Confirmation email sent to `testuser@demo.com` within 2 minutes
- Stripe sandbox dashboard shows successful charge

**Status:** Not Run
**Notes:** Run on all 3 browsers. Verify email delivery via Mailtrap sandbox.

---

## 11. Pre-Submit Checklist

> Run through this checklist before committing or sharing any test case file.

### Per test case

- [ ] TC ID is unique and follows `ModuleName-001` format
- [ ] Title follows format: `Verify <expected result> when <action/condition>` o(or `Verify <state/observation>` for non-action tests)
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
- [ ] Execution Summary block (Section 13) is present and up to date after every run
- [ ] Table of Contents lists all TCs
- [ ] Summary table at the bottom is up to date
- [ ] No two modules are mixed in the same file
- [ ] No duplicate TC IDs exist in the file

---

## 12. Anti-Patterns to Avoid

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

## 13. Execution Summary Format

> Every test case file MUST include an **Execution Summary** block immediately after the Overview block.
> Every project MUST maintain a **Project Dashboard** file at `/qa/PROJECT_DASHBOARD.md` that rolls up all individual files.
> Update both after every test execution cycle.

### 13.1 Per-File Execution Summary

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

### 13.2 Project-Wide Rollup Dashboard

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

### 13.3 Update Cadence & Ownership

| Event                        | Who Updates                  | What They Update                                |
|------------------------------|------------------------------|-------------------------------------------------|
| New test case added          | Author                       | Per-file Status Counts (Total, Not Run + 1)     |
| Test case executed           | QA tester                    | Per-file counts + Priority Breakdown            |
| End of test cycle            | QA lead                      | Per-file `Last updated` + full recount          |
| Before release gate review   | QA lead                      | `PROJECT_DASHBOARD.md` rollup + Readiness boxes |

> Rule: If a per-file Execution Summary and its bottom Summary table disagree on counts, the bottom Summary table is the source of truth. Recount and update the Execution Summary.

---

## 14. Requirement Clarification Log

> Use this section whenever a requirement is ambiguous, missing, or conflicts with any source — User Story, description document, Figma screen, or API spec.
> Never guess or assume. Stop writing the affected TC, log the clarification, mark the TC as `PENDING`, and wait for a confirmed answer before proceeding.
> This process applies to all TC types: **UI** and **API**.

---

### 14.1 When to log — reading from User Story / Description (no Figma)

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

### 14.2 When to log — reading from Figma screens

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

### 14.3 When to log — reading from API spec

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

### 14.4 Clarify Requirements sheet — column definitions

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

### 14.5 Export rules — Clarify Requirements

| TC Type | Primary Export | Excel Export |
|---------|---------------|--------------|
| **UI test cases** | Excel — `Clarify Requirements` sheet (always included) | Always exported alongside the TC sheet |
| **API test cases** | Postman — warning block in pre-script + `[PENDING]` request prefix (always included) | Only exported to Excel when the client explicitly requests a combined report |

> Rule: For API TCs, the Clarify Requirements sheet in Excel is **not generated by default**. It is generated only when the client asks for a full Excel export. The Postman pre-script warning block is the primary way to track open API questions during testing.

### 14.6 Rules (applies to all sources and TC types)

- One question per row. Never combine two questions into one entry.
- The TC linked in column B must be set to `PENDING` status until column J shows `Answered` or `Closed`.
- Once answered, update the TC immediately and change Status to `Closed`.
- Never delete a row. Closed entries are permanent audit records.
- If the same conflict appears across multiple TCs, log once and list all TC IDs in column B separated by commas.

### 14.7 TC row highlighting rule

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

### 14.8 Status flow

```
Open  →  Answered  →  Closed
              ↓
        (update TC + Postman request)
```

### Example entry

| Ref # | Related TC ID | Source / Reference | Conflict Description | Question to Client | Priority | Raised By | Raised Date | Answer / Resolution | Status | Resolved Date |
|-------|--------------|-------------------|----------------------|--------------------|----------|-----------|-------------|---------------------|--------|---------------|
| CQ-001 | LOGIN-003 | Figma: Screen / Login Error State | The error banner text on failed login is not defined in Figma. The banner component appears but the copy is placeholder text. | What is the exact error message shown when the user enters invalid credentials? | High | [Name] | YYYY-MM-DD | | Open | |

---

## 15. API Test Case Rules

> Apply these rules to every TC with Type = `API`. API TCs have no UI interaction — steps describe HTTP requests and response validations only.

---

### 15.1 Mandatory API fields (in addition to Section 2)

Every API TC must include the following inside the Steps or Test Data cells:

| Field | Where | Example |
|-------|-------|---------|
| HTTP Method | Step 1 action | `POST`, `GET`, `PUT`, `PATCH`, `DELETE` |
| Endpoint | Step 1 action | `/api/v1/auth/login` |
| Auth type | Preconditions | `Bearer token`, `API Key`, `No auth` |
| Request headers | Test Data | `Content-Type: application/json` |
| Request body | Test Data | Full JSON — never partial |
| Expected status code | Expected Result | `200 OK`, `201 Created`, `400 Bad Request` |
| Expected response fields | Expected Result | Quote exact field names and values |

---

### 15.2 Steps format for API TCs

API steps follow a fixed 3-step pattern. Never collapse into fewer.

```
| # | Action                                      | Expected Result                            |
|---|---------------------------------------------|--------------------------------------------|
| 1 | Send [METHOD] request to [endpoint]         | Request is accepted by the server          |
| 2 | Validate response status code               | Status code = [expected code]              |
| 3 | Validate response body fields               | [field]: [expected value]                  |
```

Add extra rows for headers, schema, or chained validations as needed.

---

### 15.3 Expected result rules for API

Always validate all four of the following — never skip any:

| What to validate | Rule |
|-----------------|------|
| **Status code** | State the exact code and label: `200 OK`, `401 Unauthorized`, `422 Unprocessable Entity` |
| **Response body** | Quote exact field names and expected values: `"status": "PAID"`, `"userId": 123` |
| **Response schema** | State required fields that must be present. Flag any field that must NOT appear (e.g. `"password"` must not be returned) |
| **Response headers** | Validate `Content-Type: application/json` at minimum. Add others if defined in the spec |

---

### 15.4 Auth scenarios — always test all three

For every authenticated endpoint, write separate TCs for:

| Scenario | Expected status |
|----------|----------------|
| Valid token | `200` (or appropriate success code) |
| Missing token (no Authorization header) | `401 Unauthorized` |
| Invalid / expired token | `401 Unauthorized` |

> Rule: Never assume an endpoint is auth-protected without testing it. Always include a no-auth TC.

---

### 15.5 Negative & edge case rules

| Scenario | Rule |
|----------|------|
| Missing required field | Test each required field individually. Never batch-remove multiple fields in one TC. |
| Wrong data type | Send string where integer is expected, null where string is expected |
| Boundary values | Empty string `""`, `0`, `-1`, max integer, 255-char string |
| Duplicate request | Send the same `POST` twice — verify idempotency behaviour |
| Oversized payload | Send payload exceeding the documented limit |
| SQL / injection in fields | Send `'; DROP TABLE users; --` in text fields |

---

### 15.6 Test data rules for API

```json
{
  "email": "testuser@example.com",
  "password": "TestPass123!",
  "user_id": 1042
}
```

- Always use full JSON — include every field even if not under test.
- Never inline test data in the steps — always put it in the Test Data cell.
- Store tokens as named variables: `{{access_token}}` — never paste real tokens.
- Use sandbox/staging endpoints only. Never run API TCs against production.

---

### 15.7 Chained API TCs

When a TC depends on a response value from a previous TC (e.g. an ID returned from a `POST`):

- State the dependency explicitly in Preconditions: `TC API-001 has been executed and returned order_id`.
- Store the chained value in Test Data: `order_id: {{from API-001 response}}`.
- Never hardcode IDs from a previous run — they change between environments.

---

### 15.8 API TC — blank template

```markdown
### API-NNN: [Verify response when ...]

**Priority:** High | Medium | Low
**Type:** API
**Environment:** API (REST v[version], [auth method])

**Preconditions:**
- Valid bearer token is available for test account
- Staging environment is up and accessible
- [Any data precondition — e.g. order with ID exists]

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Send [METHOD] [endpoint] with body in Test Data | Request reaches server; no network error |
| 2 | Validate response status code | [code] [label] |
| 3 | Validate response body | `[field]`: `[expected value]` |
| 4 | Validate response does not expose sensitive fields | `password`, `token` fields are absent from response |

#### Test Data

```json
{
  "field": "value"
}
```

Headers:
```
Authorization: Bearer {{access_token}}
Content-Type:  application/json
```

**Postconditions:**
- [DB/system state after the request — e.g. record created with status = X]
- [Side effects — e.g. email sent, webhook fired]

**Status:** Not Run
**Notes:**
```

---

### 15.9 API anti-patterns

| Anti-Pattern | Why It's Bad | Fix |
|---|---|---|
| Only testing happy path | Auth failures and bad inputs are the most common real-world issues | Always write Negative and Edge Case TCs |
| Partial JSON in test data | Missing fields may trigger unintended defaults | Always include the full request body |
| Hardcoding environment URLs | TCs break when switching environments | Use base URL variables: `{{base_url}}/api/v1/...` |
| Validating status code only | A `200` with wrong body data is still a failure | Always validate status code AND body fields |
| Skipping schema validation | New fields silently added to response can leak sensitive data | Always assert required fields present and sensitive fields absent |
| Chaining TCs without noting the dependency | TC fails in isolation with no explanation | Always state upstream TC dependency in Preconditions |

---

### 15.10 Pre-script rules (Pre-request Script)

A pre-script runs **before** the request is sent. Use it to prepare the environment — never to assert results.

**When to write a pre-script:**
- Setting or refreshing the auth token before the request
- Generating dynamic values (timestamps, UUIDs, random test data)
- Clearing stale environment variables from a previous run
- Setting request-specific variables used in the body or URL

**Rules:**
- Every API TC that requires auth MUST include a pre-script that sets `{{access_token}}` from the environment.
- Never hardcode token values in the pre-script — always read from `pm.environment.get()`.
- Always clear variables that should not carry over between requests: `pm.environment.unset('variable_name')`.
- Keep pre-scripts short — logic only. No assertions.

**Standard pre-script template:**
```javascript
// 1. Set auth token from environment
const token = pm.environment.get("access_token");
pm.request.headers.add({ key: "Authorization", value: "Bearer " + token });

// 2. Generate dynamic values if needed
pm.environment.set("request_timestamp", new Date().toISOString());
pm.environment.set("random_id", Math.random().toString(36).substring(2, 10));

// 3. Clear stale chained variables from previous run
pm.environment.unset("response_device_id");
```

---

### 15.11 Post-script rules (Test Script)

A post-script runs **after** the response is received. Every assertion must be a named `pm.test()` block — never write raw assertions outside a test block.

**Mandatory assertions — always include all four:**

```javascript
// 1. Status code
pm.test("Status is 200 OK", function () {
    pm.response.to.have.status(200);
});

// 2. Response body fields
pm.test("Response contains expected fields", function () {
    const json = pm.response.json();
    pm.expect(json).to.have.property("order_id");
    pm.expect(json.status).to.eql("PAID");
});

// 3. Sensitive fields are absent
pm.test("No sensitive fields exposed", function () {
    const json = pm.response.json();
    pm.expect(json).to.not.have.property("password");
    pm.expect(json).to.not.have.property("secret_key");
});

// 4. Response time
pm.test("Response time is under 2000ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});
```

**Chaining — save values for next request:**
```javascript
// Save response value to environment for use in the next TC
pm.test("Save order_id for chaining", function () {
    const json = pm.response.json();
    pm.environment.set("response_order_id", json.order_id);
});
```

**Rules:**
- Each assertion must be its own named `pm.test()` block. Never combine two assertions in one block.
- Test names must match the Expected Result column in the TC.
- For negative TCs (4xx), assert both the status code AND the error message field.
- Always unset chained variables in the pre-script of the same TC before saving new ones.

---

### 15.12 API TC export rules

#### Primary export — Postman Collection (always)

Every set of API TCs must be exported as a **Postman Collection v2.1 JSON** file. This is the default and required output — not Excel.

> API TCs are **not** written into the Excel TC sheet. The Excel file is for UI test cases only.

**File naming:**
```
postman_[module]_v[version].json

Examples:
  postman_checkout_v1.json
  postman_auth_v1.json
```

**Collection structure:**
```
Collection: [Module Name] API Tests
├── Folder: [Feature Area 1]
│   ├── Request: API-001: [TC Title]           ← clear TC, no open questions
│   ├── Request: [PENDING] API-002: [TC Title]  ← has open CQ — do not run
│   └── Pre-request Script + Tests on each request
└── Folder: [Feature Area 2]
    └── ...
```

**What is generated alongside the Postman collection:**
- Open CQ warning block injected into the pre-request script of every `[PENDING]` request
- Collection-level environment variables pre-defined
- All chaining variables declared at collection level

**Environment variables (always define at collection level):**

| Variable | Description |
|----------|-------------|
| `base_url` | Staging API base URL — e.g. `https://staging.example.com` |
| `access_token` | Bearer token — set by pre-script or manually before running |
| Any chained values | e.g. `response_order_id`, `response_item_id` — populated at runtime |

**Rules:**
- Never hardcode URLs — always use `{{base_url}}`.
- Never hardcode tokens — always use `{{access_token}}`.
- Group requests into folders by phase or feature area.
- Each request name must start with the TC ID: `API-001: Verify ...`
- Requests with open CQs must be prefixed `[PENDING]` and must not be run until the CQ is closed.
- Regenerate and commit the JSON file every time a TC or CQ is added, updated, or closed.

---

#### Secondary export — Excel Clarify Requirements (on request only)

The API Clarify Requirements sheet is **not exported to Excel by default**.

Export to Excel only when:
- The client explicitly requests a combined UI + API clarification report
- A handover document is required for a stakeholder who does not use Postman

When exporting on request:
- Include all API CQ rows in the same `Clarify Requirements` sheet as the UI CQ rows.
- Label the Source / Reference column clearly: `POST /api/v1/...` to distinguish API rows from UI rows.
- Do not create a separate sheet for API clarifications — keep one unified sheet.
