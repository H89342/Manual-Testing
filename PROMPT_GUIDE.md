# Prompt Guide — SDET Workflow

Copy-paste prompts for every task. Replace all `[PLACEHOLDER]` values before sending.
Works in both **Claude Code** (slash commands) and **Claude.ai** (paste the full prompt).

---

## How to use

- **Claude Code** — paste any prompt directly in chat. The skills, rules, and CLAUDE.md load automatically.
- **Claude.ai** — paste the prompt inside your Project (skills and rules are already uploaded).
- Replace every `[PLACEHOLDER]` — never leave brackets in the prompt.
- For combined prompts, Claude will pause at Q&A and wait for your answers before continuing.

---

## Context Header — paste this at the top of every new conversation

```
Project: [Telemax / Test case omrom / your-project-folder]
Author: [Your name]
Date: [YYYY-MM-DD]
Rules: Apply CLAUDE.md, TESTCASE_RULES_SHARED.md, and the relevant extension file (UI or API).
```

---

## Part 1 — Individual Task Prompts

---

### 1. Analyze Requirements

```
Project: [Project-Folder]
Task: Analyze requirements
Feature: [Feature name]

Apply the analyze-requirements skill.

Requirement:
[paste requirement / user story / BRD excerpt / screen description here]

Produce:
1. Plain-language summary — what is being built, who uses it, business goal, impact on existing features
2. Requirement type — Functional / Non-functional / Integration / UI-UX / API
3. In-scope vs out-of-scope boundaries
4. Testability issues — vague criteria, missing error states, undefined business rules
5. Requirement-to-testable-condition mapping table with traceability (section / screen / keyword)
6. Risk assessment — high-risk and low-risk areas

Save as: [Project-Folder]/analysis-[feature-name]_v1.md
```

---

### 2. Generate Q&A Checklist

```
Project: [Project-Folder]
Task: Generate Q&A checklist
Feature: [Feature name]

Apply the analyze-requirements skill — Q&A section.

[Paste the requirement or analysis from the previous step]

Generate questions in each category:
- Functional clarity, scope & boundaries, edge cases, non-functional requirements,
  test data, integration & dependencies, regression risk

Mark each: [CRITICAL] / [IMPORTANT] / [NICE TO HAVE]
For each question include: who to ask (PO/Dev/Design), where it is referenced (section/screen), why it matters for testing.

End with a Readiness Decision block:
[ ] READY — all CRITICAL questions answered
[ ] BLOCKED — waiting on CRITICAL answers

Save as: [Project-Folder]/qa-[feature-name]_v1.md
```

---

### 3. Write UI Test Cases

```
Project: [Project-Folder]
Task: Write UI test cases
Module: [Module name — e.g. Login, Checkout, User Profile]
TC ID prefix: [ModuleName] (e.g. LOGIN, CHKOUT)
Start TC IDs from: [001 or continue from NNN]
Environment: [Web (Chrome 120+ / Firefox 121+ / Safari 17+) / Mobile (iOS / Android)]

All Q&A CRITICAL questions are resolved. Confirmed answers:
[paste confirmed answers, or write "see [Project-Folder]/qa-[feature]_v1.md"]

Requirement / Analysis:
[paste requirement or reference the analysis file]

Follow strictly:
- TESTCASE_RULES_SHARED.md — all sections, especially §2 (mandatory fields), §3 (writing rules), §4 (TC ID format), §10 (pre-submit checklist), §13 (Clarify Requirements log)
- TESTCASE_RULES_UI.md — template §1, UI checklist §3

Coverage required:
- [ ] Happy path (positive, valid inputs)
- [ ] Negative paths (invalid inputs, error states, rejection flows)
- [ ] Boundary values (min, max, just-inside, just-outside)
- [ ] Edge cases (empty, null, special characters, max length)
- [ ] All user roles: [list roles e.g. Admin, Customer, Guest]

Output automatically per CLAUDE.md:
1. Markdown — full test cases using TESTCASE_RULES_UI.md template
2. Excel-ready table — 14 columns: TC ID | Screen/Section | Requirement Summary | Title | Preconditions | Steps (Action) | Expected Result | Test Data | Postconditions | Status | Priority | Type | Environment | Notes
3. Clarify Requirements table — for any TC marked PENDING

Save as: [Project-Folder]/testcases_[module]_v1.md
```

---

### 4. Write API Test Cases

```
Project: [Project-Folder]
Task: Write API test cases
Module: [Module name — e.g. Auth API, Payment API]
TC ID prefix: [ModuleName] (e.g. AUTH, PAY)
Endpoint(s): [e.g. POST /api/v1/auth/login, GET /api/v1/orders/{id}]
Auth type: [Bearer token / API Key / No auth]

All Q&A CRITICAL questions are resolved.

API Spec / Contract:
[paste Swagger excerpt, endpoint description, or request/response examples]

Follow strictly:
- TESTCASE_RULES_SHARED.md — §2 (mandatory fields), §4 (TC ID format)
- TESTCASE_RULES_API.md — §1 (mandatory API fields), §2 (steps format), §3 (expected result rules), §4 (auth scenarios — always test all 3), §5 (negative & edge cases), §10 (pre-script), §11 (post-script), §12 (export rules)

Coverage required per TESTCASE_RULES_API.md §4:
- [ ] Valid token — success path
- [ ] Missing token — 401
- [ ] Invalid/expired token — 401
- [ ] Each negative case (missing fields, wrong types, boundary values)

Output automatically per CLAUDE.md:
1. Markdown — full test cases using TESTCASE_RULES_API.md template §8
2. Postman Collection JSON — per TESTCASE_RULES_API.md §12

Save as: [Project-Folder]/testcases_[module]_api_v1.md
         [Project-Folder]/postman_[module]_v1.json
```

---

### 5. Review Test Cases

```
Project: [Project-Folder]
Task: Review test cases
Module: [Module name]
Reviewer: [Your name]

Apply the review-test-cases skill and TESTCASE_RULES_SHARED.md §10 pre-submit checklist.

Test cases to review:
[paste test cases here, or write "see [Project-Folder]/testcases_[module]_v1.md"]

Associated requirement (for traceability check):
[paste requirement or reference file]

Produce:
1. Per-test-case check — PASS / WARN / FAIL per criterion
2. Review report — summary score table per category
3. Critical Issues — must fix before execution (list specific TC ID and exact fix)
4. Minor Issues — should fix
5. Coverage gaps — missing scenarios
6. Overall verdict: APPROVED / APPROVED WITH CHANGES / REJECTED

Save as: [Project-Folder]/review-[module]_v1_[YYYY-MM-DD].md
```

---

### 6. Execute Tests

```
Project: [Project-Folder]
Task: Execute tests
Module: [Module name]
Build: v[X.Y.Z]
Environment: [Staging / UAT]
Date: [YYYY-MM-DD]
Test cases: APPROVED — [Project-Folder]/testcases_[module]_v1.md

Apply the execute-tests skill.

1. Run the pre-execution checklist — confirm all items before we start
2. I will report results one test case at a time — update the execution log as I go
3. Track the Execution Summary per TESTCASE_RULES_SHARED.md §12 (Status Counts, Derived Metrics, Priority Breakdown)
4. Flag immediately if:
   - Pass rate drops below 80%
   - Any Critical or P1 defect is found
   - More than 20% of TCs are BLOCKED

For each FAIL I report — produce the defect log template so I can fill it in.

Save execution log as: [Project-Folder]/execution-[module]_[YYYY-MM-DD].md
Save summary report as: [Project-Folder]/report-[module]_[YYYY-MM-DD].md
```

---

### 7. Report a Bug

```
Project: [Project-Folder]
Task: Log a defect
Test Case: [ModuleName-NNN]
Build: v[X.Y.Z]
Environment: [Staging / UAT]
Date: [YYYY-MM-DD]

What failed:
[describe exactly what you observed — include error messages, UI state, and what you did]

Help me produce a complete defect report. Ask for any missing fields.

Required fields:
- Title: [Component] — short description of what is wrong (not "it doesn't work")
- Severity: Critical / High / Medium / Low
- Priority: P1 / P2 / P3 / P4
- Steps to reproduce (exact, numbered, reproducible)
- Expected result (reference the requirement)
- Actual result (exact error message, codes, UI state)
- Evidence: screenshot / video / logs
- Frequency: Always / Intermittent (N/M times)
- Workaround: Yes (describe) / No

Save as: [Project-Folder]/bug-[NNN]-[short-title].md
```

---

### 8. Convert to Automation Script

```
Project: [Project-Folder]
Task: Convert manual test case to automation script
Framework: [Playwright / Selenium / Cypress / pytest / Postman-Newman]
Language: [TypeScript / Python / JavaScript / Java]

Test case to automate:
[paste the manual test case — must be PASS status and marked Automation Candidate: Yes]

Follow TESTCASE_RULES_SHARED.md and CLAUDE.md rules.

Rules:
- Use Page Object Model for UI tests
- Link back to manual TC ID in comment: // [ModuleName-NNN]
- Parameterize test data — no magic strings in test body
- Use stable locators: data-testid > aria-label > ID > CSS (no positional XPath)
- One test = one scenario

Output:
1. Automation script (ready to run locally)
2. Pre-checklist: locators stable, data externalized, assertions specific, test independent

Save as: [Project-Folder]/auto_[module]_[scenario].[ext]
```

---

## Part 2 — Combined Task Prompts

---

### A. Analyze + Q&A (pre-TC preparation)

```
Project: [Project-Folder]
Task: Analyze requirement and generate Q&A checklist
Feature: [Feature name]

Apply the analyze-requirements skill for both steps.

Requirement:
[paste full requirement here]

Step 1 — Analyze:
Produce analysis, testability issues, requirement mapping table with traceability, risk assessment.

Step 2 — Q&A checklist:
Generate questions marked [CRITICAL] / [IMPORTANT] / [NICE TO HAVE].
Include who to ask, where referenced, and why it matters.
End with Readiness Decision.

PAUSE after the Q&A — I will provide answers before we proceed to test cases.

Save:
- [Project-Folder]/analysis-[feature]_v1.md
- [Project-Folder]/qa-[feature]_v1.md
```

---

### B. Write + Self-Review Test Cases

```
Project: [Project-Folder]
Task: Write test cases then immediately self-review them
Module: [Module name]
TC Type: UI / API
TC ID prefix: [ModuleName]
Environment: [Web / Mobile / API]

All Q&A CRITICAL questions resolved. Confirmed answers:
[paste answers]

Requirement:
[paste requirement or analysis]

Step 1 — Write test cases:
Follow TESTCASE_RULES_SHARED.md + TESTCASE_RULES_UI.md (or API).
Output markdown + Excel-ready table (or Postman JSON) per CLAUDE.md automatically.

Step 2 — Self-review:
Apply review-test-cases skill + TESTCASE_RULES_SHARED.md §10.
Produce review report with all critical issues flagged.
Verdict: APPROVED / APPROVED WITH CHANGES / REJECTED.

Save:
- [Project-Folder]/testcases_[module]_v1.md
- [Project-Folder]/review-[module]_v1_[YYYY-MM-DD].md
```

---

### C. Full TC Creation Workflow (Analyze → Q&A → Write)

```
Project: [Project-Folder]
Task: Full test case creation — analyze, Q&A, write
Module: [Module name]
TC Type: UI / API
TC ID prefix: [ModuleName]
Environment: [Web / Mobile / API]

Requirement:
[paste full requirement here]

Run in sequence — PAUSE at Step 2 for my Q&A answers:

Step 1 — Analyze requirement (analyze-requirements skill):
Summary, type, scope, testability issues, requirement mapping, risk assessment.

Step 2 — Q&A checklist — PAUSE HERE:
Generate all questions [CRITICAL] / [IMPORTANT] / [NICE TO HAVE].
Wait for my answers. Do NOT proceed to Step 3 until I confirm: "Q&A resolved, proceed."

Step 3 — Write test cases:
Follow TESTCASE_RULES_SHARED.md + TESTCASE_RULES_UI.md (or API).
Output markdown + Excel table (or Postman JSON) per CLAUDE.md automatically.

Save:
- [Project-Folder]/analysis-[feature]_v1.md
- [Project-Folder]/qa-[feature]_v1.md
- [Project-Folder]/testcases_[module]_v1.md
```

---

### D. Full Cycle (Requirement → Approved & Ready to Execute)

```
Project: [Project-Folder]
Task: Full SDET workflow — requirement to approved test cases
Module: [Module name]
TC Type: UI / API
TC ID prefix: [ModuleName]
Environment: [Web / Mobile / API]
Author: [Your name]
Date: [YYYY-MM-DD]

Requirement:
[paste full requirement here]

Run all 5 steps in sequence. Apply CLAUDE.md, TESTCASE_RULES_SHARED.md, and the relevant extension file.

Step 1 — Intake & Analyze (analyze-requirements skill):
Plain-language summary, type, scope, testability issues, mapping table with traceability, risk assessment.

Step 2 — Q&A checklist — PAUSE HERE:
Generate questions [CRITICAL] / [IMPORTANT] / [NICE TO HAVE].
Wait for my answers before continuing.

Step 3 — Write test cases:
Use TESTCASE_RULES_SHARED.md + TESTCASE_RULES_UI.md (or API).
Output markdown + Excel-ready table (or Postman JSON) automatically.
Include Clarify Requirements table for any PENDING TCs.

Step 4 — Self-review:
Apply review-test-cases skill + TESTCASE_RULES_SHARED.md §10.
Produce review report. List all critical issues. Give verdict.

Step 5 — Pre-execution readiness summary:
Checklist of what must be ready before execution starts.
Environment, build, test data, assignments.

Save all artifacts to: [Project-Folder]/
- analysis-[feature]_v1.md
- qa-[feature]_v1.md
- testcases_[module]_v1.md
- review-[module]_v1_[YYYY-MM-DD].md
```

---

## Quick Reference

| Task | Use prompt | Claude Code shortcut |
|---|---|---|
| Analyze requirement | Prompt 1 | `/02-analyze` |
| Generate Q&A | Prompt 2 | `/03-qa` |
| Write UI test cases | Prompt 3 | `/04-create-tc` |
| Write API test cases | Prompt 4 | `/04-create-tc` |
| Review test cases | Prompt 5 | `/05-review-tc` |
| Execute tests | Prompt 6 | `/06-execute` |
| Report bug | Prompt 7 | `/07-report-bug` |
| Automate a TC | Prompt 8 | `/08-automate` |
| Analyze + Q&A | Combined A | `/02-analyze` then `/03-qa` |
| Write + Self-review | Combined B | `/04-create-tc` then `/05-review-tc` |
| Analyze → Q&A → Write | Combined C | `/02-analyze` `/03-qa` `/04-create-tc` |
| Full cycle | Combined D | `/01-read-requirements` through `/05-review-tc` |
