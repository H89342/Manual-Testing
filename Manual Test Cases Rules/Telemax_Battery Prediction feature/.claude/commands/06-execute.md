# Step 6 — Execute Tests

You are acting as an expert SDET managing a test execution cycle. Apply the full `execute-tests` skill.

## Pre-condition check:
- Confirm test cases are APPROVED from Step 5 (`/05-review-tc`)
- If not approved → stop and redirect

## Your job in this step:

### Pre-Execution Checklist
Walk the user through verifying:
- [ ] Correct build version deployed — record: `Build: vX.Y.Z | Date: YYYY-MM-DD`
- [ ] Environment stable (no active deployments)
- [ ] All services/integrations running
- [ ] Test data ready and in expected initial state
- [ ] Test cases assigned and in "Ready" status
- [ ] Execution session created in test management tool

### During Execution — guide the user to:
1. Read the full test case before starting
2. Set up preconditions exactly
3. Execute one step at a time, observe state at each step
4. Compare actual vs expected at EVERY step — not at the end
5. Capture evidence (screenshot/video/log) for every step with an expected result
6. Record result immediately: PASS / FAIL / BLOCKED / SKIPPED

### Track Progress in real time:
| Metric | Count |
|---|---|
| Total in scope | |
| Passed | |
| Failed | |
| Blocked | |
| Not run | |
| Pass rate | % |

### Flag immediately if:
- Pass rate drops below 80%
- Any Critical or P1 defect found
- More than 20% test cases BLOCKED

### For each FAIL → run `/07-report-bug` immediately

### Output — Execution Log:
Save running execution log to: `[Project-Folder]/execution-[feature]_[YYYY-MM-DD].md`

### End of cycle → produce Test Execution Summary Report and save to `[Project-Folder]/report-[feature]_[YYYY-MM-DD].md`
