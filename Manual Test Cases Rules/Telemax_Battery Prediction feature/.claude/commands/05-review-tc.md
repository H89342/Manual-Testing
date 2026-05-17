# Step 5 — Review Test Cases

You are acting as an expert SDET peer-reviewing test cases before execution. Apply the full `review-test-cases` skill checklist.

## Your job in this step:

1. Ask the user to provide the test cases to review (paste or reference the file from `[Project-Folder]/`).

2. **Apply the review checklist** to every test case:

#### Structure & Format
- [ ] Unique Test Case ID
- [ ] Descriptive title (verb + what + condition)
- [ ] Preconditions explicitly stated
- [ ] Steps numbered and sequential
- [ ] One action per step
- [ ] Expected result for every observable step
- [ ] Exact test data specified
- [ ] Priority assigned
- [ ] Test type labeled
- [ ] Traceability link to requirement — searchable by section/screen/keyword

#### Clarity
- [ ] Steps unambiguous (another tester can execute without asking)
- [ ] Expected results describe system state, not tester action
- [ ] No vague language ("verify it works", "check it loads")

#### Coverage
- [ ] Happy path covered
- [ ] Negative paths covered
- [ ] Boundary values covered
- [ ] Edge cases covered
- [ ] All affected user roles covered

#### Expected Results
- [ ] Specific and verifiable (not "success message" — say exact message text)
- [ ] Error messages quoted exactly

3. **Produce the Review Report**:

```
## Test Case Review Report
**Feature:** [name] | **Reviewer:** [name] | **Date:** [today]
**Total reviewed:** [N]

### Summary
| Category | Pass | Warn | Fail |
|---|---|---|---|
| Structure | | | |
| Clarity | | | |
| Coverage | | | |
| Traceability | | | |
| Expected Results | | | |

**Overall:** APPROVED / APPROVED WITH CHANGES / REJECTED

### Critical Issues (fix before execution)
- TC-XXX: [specific issue and fix]

### Minor Issues
- TC-XXX: [issue]

### Coverage Gaps
- [missing coverage]
```

4. Save review report to: `[Project-Folder]/review-[feature-name]_v1_[YYYY-MM-DD].md`

5. **Decide next step**:
   - If APPROVED → run `/06-execute`
   - If REJECTED → fix and re-run `/05-review-tc`
