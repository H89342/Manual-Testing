# 04 — Execution (Reference Only)

> **This folder does not store execution artifacts.**
> Execution results are saved directly inside the project folder, per `CLAUDE.md` save rule.

---

## Where execution artifacts are saved

All files save **flat** inside the project folder at the repo root:

| Artifact | Save to |
|---|---|
| Execution log (live, per session) | `[Project-Folder]/execution-[feature]_[YYYY-MM-DD].md` |
| Test Execution Summary Report | `[Project-Folder]/report-[feature]_[YYYY-MM-DD].md` |
| Defect reports (for each FAIL) | `[Project-Folder]/bug-[NNN]-[short-title].md` |

**Examples:**
```
Telemax/execution-battery-prediction_2026-05-17.md
Telemax/report-battery-prediction_2026-05-17.md
Telemax/bug-001-battery-level-not-updating.md
```

---

## Naming convention

| File | Format |
|---|---|
| Execution log | `execution-[feature-name]_[YYYY-MM-DD].md` |
| Summary report | `report-[feature-name]_[YYYY-MM-DD].md` |

---

## What each file contains

**Execution log** (`execution-[feature]_[YYYY-MM-DD].md`)
- Build version and environment
- Live result per TC: PASS / FAIL / BLOCKED / SKIPPED
- Running pass rate
- Blockers raised

**Summary report** (`report-[feature]_[YYYY-MM-DD].md`)
- Execution Summary per `TESTCASE_RULES_SHARED.md §12`
- Defect summary by severity
- Outstanding risks
- Sign-off recommendation: PASS / CONDITIONAL PASS / FAIL

---

## Trigger

Run `/06-execute` to start a guided execution cycle.
For each FAIL → run `/07-report-bug` immediately.
