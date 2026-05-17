# Step 4 — Create Test Cases

You are acting as an expert SDET writing test cases. Do NOT start until all CRITICAL Q&A questions from Step 3 are resolved.

## Pre-condition check:
- Ask the user to confirm: "Are all CRITICAL Q&A questions answered?" 
- If NO → stop and redirect to `/03-qa`
- If YES → proceed

## Your job in this step:

1. **Use the requirement mapping from Step 2** as the source of truth for what to cover.

2. **Write test cases** following this structure for every test case:

```
## Test Case: TC-[NNN]
**Title:** [Action verb] + [what] + [condition] — e.g., "Verify user can log in with valid credentials"
**Feature:** [Feature name]
**Requirement ID:** [REQ-XXX] — traced to: [section/screen/keyword in requirement]
**Type:** Functional / Negative / Boundary / Integration / Non-functional
**Priority:** High / Medium / Low
**Preconditions:**
- [exact setup required]

**Test Steps:**
| Step | Action | Expected Result |
|---|---|---|
| 1 | [one action only] | [specific observable outcome] |
| 2 | [one action only] | [specific observable outcome] |

**Test Data:**
- [exact values, not "some data"]

**Post-conditions:**
- [system state after test]

**Automation Candidate:** Yes / No
**Notes:** [any assumption-dependent items from Q&A]
```

3. **Coverage checklist** — ensure you have written:
   - [ ] Happy path (positive)
   - [ ] Negative paths (invalid input, errors)
   - [ ] Boundary values (min, max, just-inside, just-outside)
   - [ ] Edge cases (null, empty, special characters)
   - [ ] Each user role that interacts with the feature
   - [ ] Non-functional cases where required

4. Save test cases to: `.claude/workflows/03-test-cases/tc-[feature-name].md`

5. **Decide next step**: Run `/05-review-tc` before execution.
