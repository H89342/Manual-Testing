---
name: execute-tests
description: Guides structured test execution including pre-execution setup, running manual and automated tests, defect logging, progress tracking, blocker handling, and producing a test execution summary report. Use when starting or managing a test execution cycle.
---

# Execute Tests — Test Execution Skill

## Instructions

When invoked, guide the user through a complete test execution cycle from setup to sign-off. Adapt steps based on whether execution is manual, automated, or hybrid.

---

### Step 1: Pre-Execution Checklist

Do NOT begin execution until all critical items are verified. Work through this checklist:

#### Environment
- [ ] Test environment is deployed with the correct build version
- [ ] Build version matches the version under test (record: `Build: vX.Y.Z, Date: YYYY-MM-DD`)
- [ ] Environment is stable (no ongoing deployments or maintenance)
- [ ] All required services and integrations are running (verify health endpoints)
- [ ] Access credentials for the environment are valid and available
- [ ] Test environment data is in the expected initial state (seeded/reset if needed)

#### Test Readiness
- [ ] All test cases to be executed are in "Ready" status (reviewed and approved)
- [ ] Test cases are assigned to the correct tester
- [ ] Test execution session is created in the test management tool (JIRA/TestRail/Xray)
- [ ] Regression scope is defined and test set is finalized

#### Test Data
- [ ] Required test data is created and verified
- [ ] Sensitive data is anonymized per policy
- [ ] Data dependencies between test cases are resolved
- [ ] Rollback/reset procedure for test data is documented

#### Automation (if applicable)
- [ ] Automation suite passes in CI on the build to be tested
- [ ] Test runner configuration points to the correct environment
- [ ] Flaky tests are quarantined and excluded from the current run
- [ ] Test reports and artifacts directory is writable

---

### Step 2: Execute Manual Tests

Follow this discipline for each test case:

1. **Read the full test case before starting** — understand preconditions and expected results
2. **Set up preconditions exactly** — do not skip or approximate setup steps
3. **Execute one step at a time** — do not rush; observe system state after each step
4. **Compare actual vs. expected at every step** — do not wait until the end
5. **Capture evidence** — screenshot, video, or log for every step that has an expected result
6. **Record the result immediately** — PASS / FAIL / BLOCKED — do not batch-update later
7. **If a step fails:** stop execution of that test case, log a defect, then decide whether to continue to the next test case or stop the cycle

#### Result Status Definitions
| Status | When to use |
|---|---|
| PASS | Actual result matches expected result exactly |
| FAIL | Actual result differs from expected result |
| BLOCKED | Cannot execute — environment issue, missing data, or dependency failure |
| SKIPPED | Out of scope for this cycle (document reason) |
| IN PROGRESS | Partially executed (session interrupted) |

---

### Step 3: Execute Automated Tests

1. Confirm the correct branch/tag is checked out and environment config is set
2. Run the suite: `[insert project-specific run command]`
3. Monitor execution — watch for early failures that might indicate environment issues
4. After completion, review the report:
   - Separate genuine failures from infrastructure/flaky failures
   - Re-run flaky tests once to confirm; if still failing, treat as real failure
5. For each automated failure:
   - Verify it is a real product defect (not a test script bug or environment issue)
   - If test script bug: fix the script, re-run, do not log as product defect
   - If product defect: log a defect (Step 4)

---

### Step 4: Log Defects — Required Fields

Every defect must include:

```
Title: [Component] Short description of what is wrong (not "it doesn't work")
Severity: Critical / High / Medium / Low
Priority: P1 / P2 / P3 / P4
Environment: [Build version, OS, browser/device]
Test Case ID: [TC-XXX]

Steps to Reproduce:
1. [Exact step]
2. [Exact step]
3. [Exact step]

Expected Result:
[What should happen per the requirement]

Actual Result:
[What actually happened — be specific, include exact error messages]

Evidence:
- Screenshot: [attach]
- Video: [attach if needed]
- Logs: [attach relevant log snippet]

Frequency: Always / Intermittent (N/M times)
Workaround: [Yes — describe it / No]
```

#### Severity Guidelines
| Severity | Definition |
|---|---|
| Critical | System crash, data loss, security breach, complete feature unavailable |
| High | Core functionality broken, no workaround |
| Medium | Feature partially broken, workaround exists |
| Low | Cosmetic, minor UX issue, typo |

---

### Step 5: Track Execution Progress

Update progress in real time. At minimum, track daily:

| Metric | Value |
|---|---|
| Total test cases in scope | N |
| Executed | N |
| Passed | N |
| Failed | N |
| Blocked | N |
| Not run | N |
| Pass rate | N% |
| Defects logged (by severity) | Critical: N, High: N, Medium: N, Low: N |

Raise a flag immediately if:
- Pass rate drops below agreed threshold (typically 80%)
- Any Critical or P1 defect is found
- More than 20% of test cases are BLOCKED

---

### Step 6: Handle Blockers

When a test case is BLOCKED:

1. Document the blocker clearly: what is missing, what is broken, who owns it
2. Escalate immediately — do not wait for end-of-day
3. Reprioritize execution: move to unblocked test cases
4. Log the blocker as a risk in the daily status update
5. Retest when the blocker is resolved — mark as BLOCKED→PASS/FAIL

---

### Step 7: Produce the Test Execution Summary Report

At the end of the execution cycle, deliver this report:

```
## Test Execution Summary Report
**Feature / Release:** [Name]
**Tester(s):** [Names]
**Execution Period:** [Start Date] – [End Date]
**Build Version:** [vX.Y.Z]
**Environment:** [Staging / UAT / etc.]

### Execution Results
| Status | Count | % |
|---|---|---|
| PASS | N | N% |
| FAIL | N | N% |
| BLOCKED | N | N% |
| SKIPPED | N | N% |
| **Total** | **N** | **100%** |

### Defect Summary
| Severity | Open | Fixed & Retested | Deferred |
|---|---|---|---|
| Critical | N | N | N |
| High | N | N | N |
| Medium | N | N | N |
| Low | N | N | N |

### Outstanding Risks
- [List any open Critical/High defects, known gaps, or deferred items]

### Blocked Test Cases
- TC-XXX: Blocked by [issue], owner: [Name], ETA: [Date]

### Sign-Off Recommendation
[ ] PASS — all critical and high defects resolved; ready for release
[ ] CONDITIONAL PASS — known risks accepted by [Stakeholder Name]; proceed with monitoring
[ ] FAIL — critical/high defects unresolved; do not release

**Sign-off:** [Tester Name] | [Date]
```
