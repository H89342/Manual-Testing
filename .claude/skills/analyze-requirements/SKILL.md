---
name: analyze-requirements
description: Guides structured analysis of requirements (BRD, user stories, specs) and generates a Q&A checklist to resolve ambiguities before writing a single test case. Use when handed a new feature, story, or requirement document to test.
---

# Analyze Requirements — Pre-Test-Case Q&A Skill

## Instructions

When invoked, systematically analyze the provided requirement and produce a structured Q&A output. Do NOT write test cases until all critical questions are answered.

---

### Step 1: Receive & Summarize the Requirement

Ask the user to paste the requirement (user story, BRD excerpt, acceptance criteria, or feature description).

Then produce a one-paragraph plain-language summary:
- what is the feature being built?
- What is the feature/change?
- Who is the primary user?
- What is the expected business outcome?
- Does this new feature/change affect existing features or workflows?

Flag immediately if the requirement is too vague to summarize — that itself is a critical finding.

---

### Step 2: Identify Requirement Type & Scope

Classify what is being tested:
- **Functional** (behavior, workflows, business rules)
- **Non-functional** (performance, security, accessibility, compatibility)
- **Integration** (data flows between systems)
- **UI/UX** (visual, interaction design)
- **API/Contract** (endpoints, payloads, status codes)

Define the in-scope and out-of-scope boundaries explicitly.

---

### Step 3: Generate the Q&A Checklist

For each category below, generate specific questions based on the requirement. Mark each as:
- **[CRITICAL]** — must be answered before any test case is written
- **[IMPORTANT]** — should be answered; affects test design
- **[NICE TO HAVE]** — clarifies edge cases; can proceed without

#### Functional Clarity
- What are the exact acceptance criteria (Definition of Done)?
- What is the expected behavior for each user action?
- Are there business rules or formulas that need validation?
- What happens when the user provides invalid input?
- Are there dependent features or preconditions?

#### Scope & Boundaries
- What is explicitly in scope vs. out of scope for this release?
- Are there feature flags or rollout conditions (partial release)?
- Which user roles/personas are affected?

#### Edge Cases & Negative Paths
- What are the minimum and maximum input values?
- What happens at boundary values (0, null, max length, special characters)?
- What are the expected error messages and codes?
- What happens if a dependent service is unavailable?

#### Non-Functional Requirements
- Are there performance benchmarks (response time, throughput)?
- Are there security requirements (auth, data encryption, PII handling)?
- Must it be accessible (WCAG level)?
- Which browsers/devices/OS versions must be supported?

#### Data & Environment
- What test data is needed, and how will it be created/reset?
- Are there environment-specific configurations (dev/staging/prod differences)?
- Are there third-party integrations that need mocking or real access?

#### Integration & Dependencies
- Which upstream/downstream systems are affected?
- Are there API contracts or schema changes?
- Are there database migrations or data transformations?

#### Regression Risk
- Which existing features could this change break?
- Are there known fragile areas of the system?

---

### Step 4: Map Requirements to Testable Conditions and tracebility requirement to both test case and Q&A

For each confirmed requirement, produce a mapping table:

| Requirement ID | Testable Condition | Priority | Type | Q&A Reference |tracebility to strick mentioned requirements in document/screen/section |
|---|---|---|---|---|---|
| REQ-001 | User can log in with valid credentials | High | Functional | Q&A-001 |It mentions from section 3.1 in page 5 or screen name with key words are "Login Screen"|
| REQ-001 | Login fails with invalid password and shows error | High | Negative | Q&A-002 |It mentions from section 3.2 screen name with key words "shows error when login fails with ..." |
| REQ-002 | Session expires after 30 minutes of inactivity | Medium | Functional | Q&A-003 |It mentions from flow diagram of session management|

---

### Step 5: Output the Q&A Summary Document

Produce a structured summary in this format:

```
## Requirement Q&A Summary
**Feature:** [Name]
**Analyst:** [Name/Date]
**Status:** Pending / Resolved

### Open Questions (CRITICAL)
1. [Question] - Retrieve from flow/requirement — Directed to: [PO/Dev/Design]

### Open Questions (IMPORTANT)
1. [Question] - Retrieve from flow/requirement— Directed to: [PO/Dev/Design]

### Confirmed Answers
1. [Question] → [Answer] — Confirmed by: [Name, Date]

### Assumptions (proceed with caution)
1. [Assumption made due to no response]

### Readiness Decision
[ ] READY to write test cases — all critical questions resolved
[ ] BLOCKED — awaiting answers to critical questions listed above
```

---

### Step 6: Escalation Protocol

If critical questions remain unanswered after a reasonable time:
- Document the assumption made
- Flag the associated test cases as "assumption-dependent"
- Schedule a follow-up review after answers are received
- Never silently assume — always make assumptions visible in the Q&A doc
