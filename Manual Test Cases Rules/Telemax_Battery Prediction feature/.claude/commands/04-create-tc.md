# Step 4 — Create Test Cases

You are acting as an expert SDET writing test cases. Do NOT start until all CRITICAL Q&A questions from Step 3 are resolved.

## Pre-condition check:
- Ask the user to confirm: "Are all CRITICAL Q&A questions answered?" 
- If NO → stop and redirect to `/03-qa`
- If YES → proceed

## Your job in this step:

1. **Use the requirement mapping from Step 2** as the source of truth for what to cover.

2. **Write test cases** following this structure for every test case:

following the defined rules based on test case rules
- [TESTCASE_RULES_SHARED.md](TESTCASE_RULES_SHARED.md)
- [TESTCASE_RULES_UI.md](TESTCASE_RULES_UI.md)
- [TESTCASE_RULES_API.md](TESTCASE_RULES_API.md)


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

4. Save test cases to: `[Project-Folder]/testcases_[feature-name]_v1.md`

5. **Output both formats automatically** — see `CLAUDE.md` output format rule:
   - UI TCs → markdown + Excel-ready table (14 columns per TESTCASE_RULES_SHARED §2) + Clarify Requirements table if any PENDING TCs
   - API TCs → markdown + Postman Collection JSON

6. **Decide next step**: Run `/05-review-tc` before execution.
