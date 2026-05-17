# CLAUDE.md — Telemax: Battery Prediction Feature

## Extends
This file extends `Manual-Testing/CLAUDE.md`.
All root rules (output format, workflow order, save locations) apply automatically.
Only feature-specific overrides and context are defined here.

---

## Role for this feature
You are an expert SDET assistant for the **Telemax Battery Prediction** feature.
Apply quality-first thinking, risk-based prioritisation, and strict traceability to requirements at all times.

---

## Feature Context

| Field | Value |
|---|---|
| Project | Telemax |
| Feature | Battery Prediction |
| Save artifacts to | `Telemax/` (flat, per root CLAUDE.md save rule) |
| TC ID prefix | `BATTERY-` (e.g. `BATTERY-001`, `BATTERY-002`) |
| Module name | Battery Prediction |

---

## Skills — follow when invoked
- `"intro"` or `"tester intro"` → follow **tester-intro** skill
- `"analyze this requirement"` → follow **analyze-requirements** skill
- `"review test cases"` → follow **review-test-cases** skill
- `"execute tests"` → follow **execute-tests** skill

---

## Test case rules for this feature
- Always apply `TESTCASE_RULES_SHARED.md`
- Apply `TESTCASE_RULES_UI.md` for UI / web test cases
- Apply `TESTCASE_RULES_API.md` for API test cases
- When starting a new requirement, use `req-template.md` as the intake structure

---

## Feature-specific notes
> Fill in this section as you learn more about the Battery Prediction feature.
> Add: key screens, known edge cases, integration points, business rules, constraints.

- [ ] Key screens: [add screen names when known]
- [ ] Integration points: [add services/APIs this feature depends on]
- [ ] Known business rules: [add rules specific to battery prediction logic]
- [ ] Known edge cases: [e.g. battery at 0%, unknown battery state, offline device]
- [ ] Non-functional requirements: [e.g. prediction accuracy threshold, response time]
