# TESTCASE_RULES_API.md
> API test case rules — mandatory fields, steps format, Postman scripting, and export conventions.
> **Read `TESTCASE_RULES_SHARED.md` first.** This file adds API-specific content only.
> Apply these rules to every TC with Type = `API`. API TCs have no UI interaction — steps describe HTTP requests and response validations only.

---

## Table of Contents

1. [Mandatory API Fields](#1-mandatory-api-fields)
2. [Steps Format for API TCs](#2-steps-format-for-api-tcs)
3. [Expected Result Rules for API](#3-expected-result-rules-for-api)
4. [Auth Scenarios — Always Test All Three](#4-auth-scenarios--always-test-all-three)
5. [Negative & Edge Case Rules](#5-negative--edge-case-rules)
6. [Test Data Rules for API](#6-test-data-rules-for-api)
7. [Chained API TCs](#7-chained-api-tcs)
8. [Blank API Template](#8-blank-api-template)
9. [API Anti-Patterns](#9-api-anti-patterns)
10. [Pre-Script Rules (Pre-request Script)](#10-pre-script-rules-pre-request-script)
11. [Post-Script Rules (Test Script)](#11-post-script-rules-test-script)
12. [API TC Export Rules](#12-api-tc-export-rules)

---

## 1. Mandatory API Fields

Every API TC must include the following inside the Steps or Test Data cells — in addition to the mandatory fields in TESTCASE_RULES_SHARED.md §2.

| Field | Where | Example |
|-------|-------|---------|
| HTTP Method | Step 1 action | `POST`, `GET`, `PUT`, `PATCH`, `DELETE` |
| Endpoint | Step 1 action | `/api/v1/auth/login` |
| Requirement reference | Request description / Notes | `US-123`, `API Spec v2 §4.2`, `Jira STORY-456`, `Figma API contract` |
| Auth type | Preconditions | `Bearer token`, `API Key`, `No auth` |
| Request headers | Test Data | `Content-Type: application/json` |
| Request body | Test Data | Full JSON — never partial |
| Expected status code | Expected Result | `200 OK`, `201 Created`, `400 Bad Request` |
| Expected response fields | Expected Result | Quote exact field names and values |

> Requirement traceability: Every API TC must include a requirement reference in the request metadata. Since API TCs are exported as Postman collections rather than Excel, this traceability must appear in the request description, Notes field, or pre-request script comment.

## 2. Steps Format for API TCs

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

## 3. Expected Result Rules for API

Always validate all four of the following — never skip any:

| What to validate | Rule |
|-----------------|------|
| **Status code** | State the exact code and label: `200 OK`, `401 Unauthorized`, `422 Unprocessable Entity` |
| **Response body** | Quote exact field names and expected values: `"status": "PAID"`, `"userId": 123` |
| **Response schema** | State required fields that must be present. Flag any field that must NOT appear (e.g. `"password"` must not be returned) |
| **Response headers** | Validate `Content-Type: application/json` at minimum. Add others if defined in the spec |

---

## 4. Auth Scenarios — Always Test All Three

For every authenticated endpoint, write separate TCs for:

| Scenario | Expected status |
|----------|----------------|
| Valid token | `200` (or appropriate success code) |
| Missing token (no Authorization header) | `401 Unauthorized` |
| Invalid / expired token | `401 Unauthorized` |

> Rule: Never assume an endpoint is auth-protected without testing it. Always include a no-auth TC.

---

## 5. Negative & Edge Case Rules

| Scenario | Rule |
|----------|------|
| Missing required field | Test each required field individually. Never batch-remove multiple fields in one TC. |
| Wrong data type | Send string where integer is expected, null where string is expected |
| Boundary values | Empty string `""`, `0`, `-1`, max integer, 255-char string |
| Duplicate request | Send the same `POST` twice — verify idempotency behaviour |
| Oversized payload | Send payload exceeding the documented limit |
| SQL / injection in fields | Send `'; DROP TABLE users; --` in text fields |

---

## 6. Test Data Rules for API

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

## 7. Chained API TCs

When a TC depends on a response value from a previous TC (e.g. an ID returned from a `POST`):

- State the dependency explicitly in Preconditions: `TC API-001 has been executed and returned order_id`.
- Store the chained value in Test Data: `order_id: {{from API-001 response}}`.
- Never hardcode IDs from a previous run — they change between environments.

---

## 8. Blank API Template

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

​```json
{
  "field": "value"
}
​```

Headers:
​```
Authorization: Bearer {{access_token}}
Content-Type:  application/json
​```

**Postconditions:**
- [DB/system state after the request — e.g. record created with status = X]
- [Side effects — e.g. email sent, webhook fired]

**Status:** Not Run
**Notes:**

---
```

---

## 9. API Anti-Patterns

| Anti-Pattern | Why It's Bad | Fix |
|---|---|---|
| Only testing happy path | Auth failures and bad inputs are the most common real-world issues | Always write Negative and Edge Case TCs |
| Partial JSON in test data | Missing fields may trigger unintended defaults | Always include the full request body |
| Hardcoding environment URLs | TCs break when switching environments | Use base URL variables: `{{base_url}}/api/v1/...` |
| Validating status code only | A `200` with wrong body data is still a failure | Always validate status code AND body fields |
| Skipping schema validation | New fields silently added to response can leak sensitive data | Always assert required fields present and sensitive fields absent |
| Chaining TCs without noting the dependency | TC fails in isolation with no explanation | Always state upstream TC dependency in Preconditions |

---

## 10. Pre-Script Rules (Pre-request Script)

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
// REQUIREMENT REFERENCE: [US-123 | API Spec v2 §4.2 | Jira STORY-456]
// Business context: [Why this endpoint matters, what business flow it supports, and why the test exists]

// 1. Set auth token from environment
const token = pm.environment.get("access_token");
pm.request.headers.add({ key: "Authorization", value: "Bearer " + token });

// 2. Generate dynamic values if needed
pm.environment.set("request_timestamp", new Date().toISOString());
pm.environment.set("random_id", Math.random().toString(36).substring(2, 10));

// 3. Clear stale chained variables from previous run
pm.environment.unset("response_order_id");
```

> Reviewer guidance: The pre-script must include a short requirement reference plus a brief business context comment. This helps reviewers verify the intent without guessing or relying on AI-generated assumptions.

**Open CQ warning block** — inject into the pre-script of every PENDING request:
```javascript
// ⚠ OPEN CLARIFICATION — CQ-001
// Question: [paste the question from the Clarify Requirements sheet]
// Status: Open — do not run this request until resolved.
// Ref: Clarify Requirements sheet → CQ-001
```

---

## 11. Post-Script Rules (Test Script)

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

## 12. API TC Export Rules

### Primary export — Postman Collection (always)

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
- Open CQ warning block injected into the pre-request script of every `[PENDING]` request (see Section 10)
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
- Every request must include a requirement reference in the request description or Notes: `US-123`, `API Spec v2 §4.2`, `Jira STORY-456`, or equivalent.
- Use the request description to summarize the business intent and trace it back to the requirement source.
- Always export and deliver the Postman collection JSON file with the API TC package so the user can import it immediately. This avoids needing a second request if the API test case was created without explicit export instructions.
- Requests with open CQs must be prefixed `[PENDING]` and must not be run until the CQ is closed.
- Regenerate and commit the JSON file every time a TC or CQ is added, updated, or closed.

---

### Secondary export — Excel Clarify Requirements (on request only)

The API Clarify Requirements sheet is **not exported to Excel by default**.

Export to Excel only when:
- The client explicitly requests a combined UI + API clarification report
- A handover document is required for a stakeholder who does not use Postman

When exporting on request:
- Include all API CQ rows in the same `Clarify Requirements` sheet as the UI CQ rows.
- Label the Source / Reference column clearly: `POST /api/v1/...` to distinguish API rows from UI rows.
- Do not create a separate sheet for API clarifications — keep one unified sheet.
