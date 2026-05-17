---
name: review-test-cases
description: Performs a structured, checklist-driven review of test cases for completeness, clarity, coverage, and traceability. Use when asked to review someone's test cases, audit a test suite, or self-review before submission.
---

# Review Test Cases — Structured Review Skill

## Instructions

When invoked, apply a systematic review against the provided test cases. Output a scored review report with specific, actionable findings.

---

### Step 1: Collect Input

Ask for (or accept from context):
- The test cases to review (paste, file, or test management tool export)
- The associated requirements or user stories (for traceability check)
- The review scope: full suite, single feature, or specific test IDs

---

### Step 2: Apply the Review Checklist

Evaluate every test case against each criterion. Mark each as:
- **PASS** — criterion met
- **FAIL** — criterion not met (provide specific fix)
- **WARN** — partially met or minor improvement needed

#### 2.1 Structure & Format
- [ ] Has a unique Test Case ID
- [ ] Has a clear, descriptive title (not "Test login" — say "Verify user can log in with valid credentials")
- [ ] Preconditions are explicitly stated (not assumed)
- [ ] Test steps are numbered and sequential
- [ ] Each step has one action only (no compound steps like "Enter username and click submit")
- [ ] Expected result is defined for every step that produces observable output
- [ ] Test data is specified (not "enter some data" — specify exact values)
- [ ] Priority/severity is assigned
- [ ] Test type is labeled (Smoke, Regression, Functional, Negative, etc.)
- [ ] traceability link to requirement/user story is included and accuarated and can be search in the requirement document/screen/section with key words

#### 2.2 Clarity & Readability
- [ ] Steps are unambiguous — a different tester can execute without asking questions
- [ ] Expected results describe the system state, not the tester's action
- [ ] No vague language ("verify it works", "check the page loads correctly")
- [ ] Acronyms and domain terms are defined or linked to a glossary

#### 2.3 Coverage
- [ ] Happy path (positive scenario) is covered
- [ ] Negative paths are covered (invalid input, error conditions)
- [ ] Boundary values are tested (min, max, just-inside, just-outside)
- [ ] Edge cases are addressed (empty input, null, special characters, max length)
- [ ] All user roles/personas that interact with the feature are tested
- [ ] Non-functional aspects are covered where required (performance, accessibility, security)

#### 2.4 Traceability
- [ ] Each test case links to at least one requirement ID or user story
- [ ] Every acceptance criterion has at least one corresponding test case
- [ ] No orphan test cases (test cases with no requirement link)
- [ ] No uncovered requirements (requirements with no test cases)

#### 2.5 Expected Results
- [ ] Expected result is specific and verifiable (not "success message appears" — say "Toast message 'Login successful' appears within 2 seconds")
- [ ] Expected result reflects what the system should do, not what the tester hopes
- [ ] Error messages are quoted exactly where known
- [ ] Database/backend state changes are verified where applicable

#### 2.6 Test Data
- [ ] Test data is realistic and representative
- [ ] Both valid and invalid data variants are defined
- [ ] Sensitive data (PII, credentials) is anonymized or uses placeholder conventions
- [ ] Test data dependencies (setup/teardown) are documented

#### 2.7 Reusability & Maintenance
- [ ] Common preconditions are extracted to shared setup steps
- [ ] No copy-paste duplication — shared steps reference a common procedure
- [ ] Test case can be executed independently (no hidden dependency on execution order)
- [ ] Automation candidates are tagged

---

### Step 3: Coverage Gap Analysis

After reviewing individual test cases, assess the overall suite:

1. List all requirements/acceptance criteria
2. Map which test cases cover each
3. Identify gaps:
   - Requirements with no test coverage
   - Over-tested low-risk areas vs. under-tested high-risk areas
   - Missing negative/edge case coverage

---

### Step 4: Produce the Review Report

Output in this format:

```
## Test Case Review Report
**Feature:** [Name]
**Reviewer:** [Name/Date]
**Total Test Cases Reviewed:** [N]

### Summary Score
| Category | Pass | Warn | Fail |
|---|---|---|---|
| Structure & Format | N | N | N |
| Clarity | N | N | N |
| Coverage | N | N | N |
| Traceability | N | N | N |
| Expected Results | N | N | N |
| Test Data | N | N | N |
| Reusability | N | N | N |

**Overall Quality:** APPROVED / APPROVED WITH CHANGES / REJECTED

---

### Critical Issues (must fix before execution)
- TC-001: Expected result on Step 3 is missing. Add: "System displays error message 'Invalid email format'."
- TC-005: No link to any requirement. Add traceability to REQ-012.

### Minor Issues (should fix)
- TC-003: Step 2 combines two actions. Split into separate steps.

### Coverage Gaps
- REQ-008 (password reset flow) has no negative test cases.
- No boundary value test for the "age" field (min=18, max=120).

### Suggestions
- TC-007 through TC-012 share the same precondition — extract to a shared setup step.
- TC-015 is a strong automation candidate (stable, repeatable, high regression risk).
```

---

### Step 5: Reviewer Sign-Off Protocol

- Do not approve test cases that have CRITICAL issues
- For WARN items, note them but allow execution to proceed if risk is accepted
- After fixes are applied, request a re-review of changed test cases only
- Record the review decision in the test management tool with reviewer name and date
