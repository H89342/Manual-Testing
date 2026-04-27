# TESTCASE_RULES — Index
> QA rule set split into three files for independent maintenance and scalability.
> Start here, then open the file that matches your TC type.

---

## How to use

| Writing… | Read first | Then read |
|----------|-----------|-----------|
| UI / Web / Mobile test cases | `TESTCASE_RULES_SHARED.md` | `TESTCASE_RULES_UI.md` |
| API test cases | `TESTCASE_RULES_SHARED.md` | `TESTCASE_RULES_API.md` |
| Both in the same project | `TESTCASE_RULES_SHARED.md` | Both extension files |

---

## Files

| File | Purpose | Covers |
|------|---------|--------|
| [`TESTCASE_RULES_SHARED.md`](TESTCASE_RULES_SHARED.md) | Foundation rules — all TC types | File structure, mandatory fields, writing rules, naming, priority/status/type definitions, test data, environment tags, pre-submit checklist, anti-patterns, execution summary, requirement clarification log (§1–13) |
| [`TESTCASE_RULES_UI.md`](TESTCASE_RULES_UI.md) | UI / Mobile extension | Blank TC template, full worked example, mobile gesture vocabulary, UI-specific checklist additions |
| [`TESTCASE_RULES_API.md`](TESTCASE_RULES_API.md) | API extension | Mandatory API fields, steps format, auth scenarios, negative/edge rules, Postman pre/post-scripts, blank API template, API anti-patterns, export rules |

---

## Update guidance

| Changing… | Edit only |
|-----------|-----------|
| Status definitions, priority levels, naming conventions, execution summary format | `TESTCASE_RULES_SHARED.md` |
| Requirement clarification log (CQ process, columns, status flow) | `TESTCASE_RULES_SHARED.md` |
| UI/mobile blank template, worked example, mobile gesture terms | `TESTCASE_RULES_UI.md` |
| Postman scripting conventions, API TC format, API export rules | `TESTCASE_RULES_API.md` |

> Never copy a rule into two files. One rule lives in one file. Cross-reference the other file by name if needed.
