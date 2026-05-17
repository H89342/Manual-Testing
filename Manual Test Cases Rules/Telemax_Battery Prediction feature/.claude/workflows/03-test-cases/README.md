# 03 — Test Cases

Store all test cases and review reports here.

## What goes here:
- Test cases written in `/04-create-tc` → `testcases_[feature-name]_v[version].md` → `testcases_[feature-name]_v[version].xlsx`
- Review reports from `/05-review-tc` → `review-[feature-name]_version-x.md` → `review-[feature-name]_version-x.xlsx`

## Naming convention:
- `testcases_[feature-name]_v[version]` → `testcases_[feature-name]_v[version].xlsx`
- `review-[feature-name]_version-x_[YYYY-MM-DD].md` → `review-[feature-name]_version-x_[YYYY-MM-DD].xlsx`

**Version numbering:** start at `v1`, increment on significant changes (e.g. `v2`, `v3`)
Example: `tc-login_v1.md`, `tc-login_v2.md`


## Test case rules: following the defined rules based on test case type
- [TESTCASE_RULES_SHARED.md](TESTCASE_RULES_SHARED.md)
- [TESTCASE_RULES_UI.md](TESTCASE_RULES_UI.md)
- [TESTCASE_RULES_API.md](TESTCASE_RULES_API.md)

## Status per test case:
Draft → In Review → Approved → Executed → Closed

## Next step:
When review status is APPROVED → run `/06-execute`
