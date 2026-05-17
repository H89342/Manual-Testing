# 03 — Test Cases (Reference Only)

> **This folder does not store test case artifacts.**
> Test case files and review reports save directly inside the project folder, per `CLAUDE.md` save rule.
> Exception: Rule files (`TESTCASE_RULES_*.md`) stay here permanently as shared reference.

---

## Where artifacts are saved

| Artifact | Save to |
|---|---|
| Test cases (markdown) | `[Project-Folder]/testcases_[module]_v[N].md` |
| Test cases (Excel) | `[Project-Folder]/testcases_[module]_v[N].xlsx` |
| Review report (markdown) | `[Project-Folder]/review-[module]_v[N]_[YYYY-MM-DD].md` |
| Review report (Excel) | `[Project-Folder]/review-[module]_v[N]_[YYYY-MM-DD].xlsx` |
| API test cases (Postman) | `[Project-Folder]/postman_[module]_v[N].json` |

**Examples:**
```
Telemax/testcases_battery-prediction_v1.md
Telemax/testcases_battery-prediction_v1.xlsx
Telemax/review-battery-prediction_v1_2026-05-17.md
Telemax/postman_battery-prediction-api_v1.json
```

---

## What stays in this folder (tooling only)

| File | Purpose |
|---|---|
| `TESTCASE_RULES_SHARED.md` | Foundation rules for all TC types |
| `TESTCASE_RULES_UI.md` | UI / mobile extension rules |
| `TESTCASE_RULES_API.md` | API extension rules |
| `README.md` | This file |

---

## Naming convention

| File | Format |
|---|---|
| Test cases | `testcases_[module]_v[N].md / .xlsx` |
| Review report | `review-[module]_v[N]_[YYYY-MM-DD].md / .xlsx` |
| Postman collection | `postman_[module]_v[N].json` |

**Version numbering:** start at `v1`, increment on significant structural changes (`v2`, `v3`).

---

## Test case rules — always apply

- [TESTCASE_RULES_SHARED.md](TESTCASE_RULES_SHARED.md) — foundation rules for all test cases
- [TESTCASE_RULES_UI.md](TESTCASE_RULES_UI.md) — UI / mobile test cases
- [TESTCASE_RULES_API.md](TESTCASE_RULES_API.md) — API test cases

---

## Status lifecycle

`Draft` → `In Review` → `Approved` → `Executed` → `Closed`

---

## Next step

When review status is `APPROVED` → run `/06-execute`
