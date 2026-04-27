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

---

## 2. Mandatory Fields

Every single test case MUST contain all of the following fields. A TC is not complete without them.

| Field | Required | Notes |
|-------|----------|-------|
| TC ID | YES | Format: `ModuleName-001`. Never reuse or skip. |
| Title | YES | Verify <expected result> when <action/condition>|
| Preconditions | YES | At least one bullet. Never leave blank. |
| Steps table | YES | Min 2 rows. Format: `# \| Action \| Expected Result` |
| Test Data | YES | Fenced code block. Even if just one field. |
| Postconditions | YES | System/DB truth after the test passes. |
| Status | YES | Default: `Not Run`. Fill after execution only. |
| Priority | YES | High / Medium / Low |
| Type | YES | See Section 5 for allowed values |
| Environment | YES | Web / Mobile / API / Mixed |
| Notes | NO | Leave blank if nothing unusual. |

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
```
